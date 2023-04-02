from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from service.search import search_video
from service.logger import log
from service.pubsub import parse_notification
import template_helpers as helpers

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="static"))
templates = Jinja2Templates(directory="templates")
render = templates.TemplateResponse


@ app.get("/")
def read_root(request: Request):
    return render("home.jinja2", {"request": request, "id": id})


@ app.get("/search_video")
@limiter.limit("10/minute")
def get_search_video(video_id: str, text: str, request: Request):
    log(f"Searching video {video_id} for {text}")

    if video_id.find('watch?v=') != -1:
        video_id = video_id.split('watch?v=')[1]

    context = {
        "request": request,
        "result": search_video(video_id, text),
        "helpers": helpers
    }
    return render("video_results.jinja2", context)


@app.post("/api/yt_sub")
async def sub_callback(request: Request):
    data = await request.json()
    log(f"Received sub callback {data}")
    parsed = parse_notification(data)
    log(f"Parsed sub callback {parsed}")
    return {"status": "ok"}


@ app.get("/health")
def health():
    return {"status": "ok"}
