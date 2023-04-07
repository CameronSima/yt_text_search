import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from service.search import search_video, search_channel
from service.logger import log
from service.pubsub import parse_notification
from service.utils import clean_video_id


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://yttextsearch-production.up.railway.app",
    "https://yt-text-search.vercel.app"
]

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@ app.get("/search_video")
@limiter.limit("20/minute")
def get_search_video(video_id: str, text: str, request: Request):
    video_id = clean_video_id(video_id)
    log(f"Searching video {video_id} for {text}")
    results = search_video(video_id, text)
    return results.json()


@app.get("/search_channel")
@limiter.limit("20/minute")
def get_search_channel_data(channel_name: str, text: str, request: Request):

    # strip @ from channel name
    if channel_name[0] == '@':
        channel_name = channel_name[1:]

    log(f"Searching channel {channel_name} for {text}")
    results = map(json.dumps, search_channel(channel_name, text))
    return EventSourceResponse(results)


@app.get("/yt_sub")
async def yt_sub(request: Request):
    params = request.query_params
    hub_topic = params.get("hub.topic")
    hub_challenge = params.get("hub.challenge")
    hub_mode = params.get("hub.mode")
    hub_lease_seconds = params.get("hub.lease_seconds")

    print({"hub_topic": hub_topic, "hub_challenge": hub_challenge,
          "hub_mode": hub_mode, "hub_lease_seconds": hub_lease_seconds})
    return hub_challenge


@app.post("/yt_sub")
async def sub_callback(request: Request):
    data = await request.json()
    log(f"Received sub callback {data}")
    parsed = parse_notification(data)
    log(f"Parsed sub callback {parsed}")
    return {"status": "ok"}


@ app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/api", app, name="api")
