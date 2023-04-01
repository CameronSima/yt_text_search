from typing import Union
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from service.search import search_video
import template_helpers as helpers


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
render = templates.TemplateResponse


@app.get("/")
def read_root(request: Request):
    return render("home.jinja2", {"request": request, "id": id})


@app.get("/search_video")
def get_search_video(video_id: str, text: str, request: Request):

    if video_id.find('watch?v=') != -1:
        video_id = video_id.split('watch?v=')[1]

    result = search_video(video_id, text)
    return render("video_results.jinja2", {
        "request": request,
        "result": result,
        "helpers": helpers
    })
