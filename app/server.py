from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.urls.router import router as urls_router

app = FastAPI(title='Mini Link API', version='0.1.0')
templates = Jinja2Templates(directory='app/templates')

app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name='index.html')


app.include_router(urls_router)
