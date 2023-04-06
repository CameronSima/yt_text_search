import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from staticfiles import SPAStaticFiles
from service.search import search_video, search_channel
from service.logger import log
from service.pubsub import parse_notification
from service.utils import clean_video_id
import template_helpers as helpers

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
api_app = FastAPI()


api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_app.state.limiter = limiter
api_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@ api_app.get("/search_video")
@limiter.limit("10/minute")
def get_search_video(video_id: str, text: str, request: Request):
    video_id = clean_video_id(video_id)
    log(f"Searching video {video_id} for {text}")
    results = search_video(video_id, text)
    return results.json()


@api_app.get("/search_channel")
@limiter.limit("20/minute")
def get_search_channel_data(channel_name: str, text: str, request: Request):

    # strip @ from channel name
    if channel_name[0] == '@':
        channel_name = channel_name[1:]

    log(f"Searching channel {channel_name} for {text}")
    results = map(json.dumps, search_channel(channel_name, text))
    return EventSourceResponse(results)


@api_app.post("/yt_sub")
async def sub_callback(request: Request):
    data = await request.json()
    log(f"Received sub callback {data}")
    parsed = parse_notification(data)
    log(f"Parsed sub callback {parsed}")
    return {"status": "ok"}


@ api_app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/api", api_app, name="api")
app.mount(
    "/", SPAStaticFiles(directory="frontend/build", html=True), name="app")
