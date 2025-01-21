from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() :
    return {'Hello Emotion!'}


'''
How To Run Server : > uvicorn main:app --reload

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs