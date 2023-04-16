import json
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from youtube_transcript_api._errors import TranscriptsDisabled
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from youtube_transcript_api import YouTubeTranscriptApi
from service.search import search_video, search_channel, get_videos_from_channel
from service import logger
from service import pubsub
from service.pubsub import parse_notification
from service.utils import clean_video_id, clean_channel_name
from service.youtube_api import search_channels
from init_db import init_db
from db.models.video import Video, create_from_yt_api, yt_video_to_video


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://yttextsearch-production.up.railway.app",
    "https://yt-text-search.vercel.app"
]


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

init_db(app)

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
    logger.info({"video_id": video_id, "text": text})
    try:
        results = search_video(video_id, text)
        return results.json()
    except TranscriptsDisabled:
        logger.error(str(e))
        return HTTPException(detail="Transcripts are disabled for this video", status_code=403)
    except Exception as e:
        logger.error(str(e))
        return HTTPException(detail=str(e), status_code=500)


@app.get("/search_channel")
@limiter.limit("20/minute")
async def get_search_channel_data(channel_name: str, text: str, request: Request):
    channel_name = clean_channel_name(channel_name)

    logger.info(f"Searching channel {channel_name} for {text}")
    results = map(json.dumps, search_channel(channel_name, text))
    return EventSourceResponse(results)


@app.get("/channel/videos")
@limiter.limit("20/minute")
async def get_channel_videos(channel_id: str, request: Request):
    logger.info(f"Getting videos for channel {channel_id}")

    db_videos = await Video.filter(yt_channel_id=channel_id)
    # print("db videos")
    # print(db_videos)
    # api_videos = [yt_video_to_video(video) async for video in get_videos_from_channel(channel_id)]
    # print("api videos")
    # print(api_videos)
    # unsaved_videos = [video for video in api_videos if video not in db_videos]
    # print("unsaved videos")
    # print(unsaved_videos)

    # return api_videos
    return db_videos


@app.get("/channel/search")
@limiter.limit("20/minute")
@cache(expire=60 * 60 * 24)
def get_search_channel_data(channel_name: str, request: Request):
    channel_name = clean_channel_name(channel_name)
    logger.info(f"Searching channels {channel_name}")
    results = search_channels(channel_name)
    return results


@app.post("/channel/subscribe/")
@limiter.limit("20/minute")
async def subscribe_channel(channel_id: str, request: Request):
    response_code = await pubsub.subscribe(channel_id)
    return response_code

# Youtube PubSub hooks


@app.get("/youtube/on_sub")
async def get_sub_callback(request: Request):
    params = request.query_params
    hub_topic = params.get("hub.topic")
    hub_challenge = params.get("hub.challenge")
    hub_mode = params.get("hub.mode")
    hub_lease_seconds = params.get("hub.lease_seconds")

    print({"hub_topic": hub_topic, "hub_challenge": hub_challenge,
          "hub_mode": hub_mode, "hub_lease_seconds": hub_lease_seconds})
    return Response(content=hub_challenge, media_type="text/plain", status_code=200)


@app.post("/youtube/on_sub")
async def post_sub_callback(request: Request):
    data = await request.body()
    parsed = parse_notification(data)
    logger.info(parsed)

    if not await Video.exists(title=parsed["title"]):
        try:
            segments = YouTubeTranscriptApi.get_transcript(
                parsed["yt_video_id"])
        except Exception as e:
            segments = []
            logger.error(str(e))

    await Video.create(**parsed, text_segments=segments)
    return {"status": "ok"}


@ app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
