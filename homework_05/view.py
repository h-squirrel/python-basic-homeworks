from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from view_nuts import router as nuts_view_router

router = APIRouter()
router.include_router(nuts_view_router, prefix="/collection", tags=['nuts_view'])

templates = Jinja2Templates(directory="./templates")

@router.get("/home/", response_class=HTMLResponse)
async def home_info(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, 'title': 'Главная'})

@router.get("/about/", response_class=HTMLResponse)
async def developer_info(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, 'title': 'О разработчице'})