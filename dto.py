from pydantic import BaseModel

class Request(BaseModel) :
    memory : str
    feelings : list[str]