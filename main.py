from fastapi import FastAPI, HTTPException

from dto import Request 
from feedback import feedback

app = FastAPI()

@app.get("/")
def read_root() :
    return {'Hello Emotion!'}

@app.post("/feedback")
async def callFeedbackAI(request: Request) :
    try :
        result = await feedback(request)
        return {
            "result" : result 
        }
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))
