from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from nuts.control import NutsList

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

@router.get("/nuts", response_class=HTMLResponse)
async def show_nuts_list(request: Request):
    if 0 == len(NutsList.nuts):
        NutsList.default_list_set()
    nuts = NutsList.get_all_list()
    context = { "request": request, "nuts": nuts, "title": "Коллекция" }
    return templates.TemplateResponse("nuts.html", context)

@router.get("/nuts/{nut_name}", response_class=HTMLResponse)
async def show_nut_detail(request: Request, nut_name: str):
    nut = NutsList.get_nut_by_name(nut_name)
    context = \
        {
            "request": request,
            "nut_obj": nut,
            'title': nut_name
        }
    return templates.TemplateResponse("nut_item.html", context)
