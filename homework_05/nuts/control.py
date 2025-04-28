from fastapi import HTTPException
from pydantic import HttpUrl

from nuts.default_nuts_list import default_nuts_list
from nuts.schemas import Nut

class NutsList:
    nuts = []

    @classmethod
    def add_nut(cls, name: str, img_src: HttpUrl, description: str, w_min: int, w_max: int) -> str or None:
        try:
            nut = Nut(name=name, img_src=img_src, description=description, weight_one_nut_min=w_min, weight_one_nut_max=w_max)
        except Exception as e:
            return str(e)
        else:
            cls.nuts.append(nut)
            return None

    @classmethod
    def default_list_set(cls):
        for nut in default_nuts_list:
            cls.add_nut(nut["name"], nut["img_src"], nut["description"], nut["weight_one_nut_min"], nut["weight_one_nut_max"])

    @classmethod
    def get_all_list(cls) -> list[Nut]:
        return cls.nuts

    @classmethod
    def get_idx_nut(cls, name: str) -> int or None:
        for idx, nut in enumerate(cls.nuts):
            if nut.name == name:
                return idx

    @classmethod
    def get_nut_by_name(cls, name: str) -> Nut or None:
        idx = cls.get_idx_nut(name)
        if idx is None:
            raise HTTPException(status_code=404, detail="Орех с таким названием не найден")
        return cls.nuts[idx]

    @classmethod
    def del_nut_by_name(cls, name: str) -> None:
        idx = cls.get_idx_nut(name)
        if idx is None:
            raise HTTPException(status_code=404, detail="Орех с таким названием не найден")
        del cls.nuts[idx]

    @classmethod
    def change_nut_by_name(cls, name: str, img_src: HttpUrl, desc: str, w_min: int, w_max: int) -> None:
        idx = cls.get_idx_nut(name)
        if idx is None:
            raise HTTPException(status_code=404, detail="Орех с таким названием не найден")
        cls.nuts[idx].img_src = img_src
        cls.nuts[idx].description = desc
        cls.nuts[idx].weight_one_nut_min = w_min
        cls.nuts[idx].weight_one_nut_max = w_max