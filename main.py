from fastapi import FastAPI, HTTPException

from dto import Request 
from feedback import feedback

app = FastAPI()

@app.get("/")
def read_root() :
    return {'Hello Emotion!'}

@app.post("/feedback")
def callFeedbackAI(request : Request) :
    try :
        result = feedback(request.memory, request.feelings)
        return {
            "result" : result 
        }
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))