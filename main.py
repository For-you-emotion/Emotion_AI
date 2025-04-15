from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dto import Request 
from db import get_db
from feedback import saveData, feedback
from wav import save, find, delete

import logging, os, sys

app = FastAPI()

@app.get("/")
def read_root() :
    return {"Hello Emotion!"}

# wav 저장 후 그대로 반환
@app.post("/wavTest")
async def saveWav(file: UploadFile = File(...)) :
    try :
        return await save(file)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

# 파일 이름으로 wav 반환
@app.get("/{text}")
async def getWav(text: str): 
    try :
        return await find(text)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

@app.delete("/{text}")
async def deleteWav(text: str) :
    await delete(text)

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
