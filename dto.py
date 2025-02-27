from pydantic import BaseModel

class Request(BaseModel) :
    hwId : str
    beadNum : int
    memory : str
    feelings : list[str]