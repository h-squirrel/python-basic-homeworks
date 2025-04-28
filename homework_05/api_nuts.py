from fastapi import APIRouter, Form, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from nuts.control import NutsList

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/add_nut")
async def add_nut(name:str = Form(), image: HttpUrl=Form(), desc: str=Form(), w_min: int=Form(), w_max: int=Form()):
    res = NutsList.add_nut(name, image, desc, w_min, w_max)
    if res is None:
        return {'message': "Новый орех успешно добавлен в коллекцию!"}
    else:
        return {'message': f"При добавлении возникла ошибка: {res}"}

@router.delete("/del_nut")
async def del_nut(nut_name: str):
    try:
        NutsList.del_nut_by_name(nut_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Орех с таким названием не найден")
    else:
        return {'message': "Орех удалён из коллекции("}

@router.post("/change_nut")
async def change_nut(name: str, img: HttpUrl, desc: str, w_min: int, w_max: int):
    try:
        NutsList.change_nut_by_name(name, img, desc, w_min, w_max)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Орех с таким названием не найден")
    else:
        return {'message': "Карточка ореха обновлена"}