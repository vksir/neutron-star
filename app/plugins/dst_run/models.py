from typing import Dict
from pydantic import BaseModel


class Players(BaseModel):
    __root__: Dict[int, str]
