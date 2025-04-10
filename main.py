from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dto import Request 
from db import get_db
from feedback import saveData, feedback
from wav import save, find

import logging, os, sys

app = FastAPI()

@app.get("/")
def read_root() :
    return {'Hello Emotion!'}

@app.post("/wavTest")
async def saveWav(file: UploadFile = File(...)) :
    try :
        return save(file)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

@app.get("/{text}")
def getWav(text: str): 
    try :
        return find(text)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

@app.post("/feedback")
async def callFeedbackAI(request: Request, db: AsyncSession = Depends(get_db)) :
    logging.info("피드백 요청 전, 데이터를 DB 에 저장합니다...")
    await saveData(request, db)
    
    try :
        result = feedback(request)
        return {
            "result" : result 
        }
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))
