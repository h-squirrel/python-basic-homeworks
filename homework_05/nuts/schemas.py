from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated


class Nut(BaseModel):
    name: Annotated[str, Field(...)]
    img_src: Annotated[HttpUrl, Field(...)]
    description: Annotated[str, Field(None, max_length=500)]
    weight_one_nut_min: Annotated[int, Field(None, gt=0)]
    weight_one_nut_max: Annotated[int, Field(None, gt=0)]
