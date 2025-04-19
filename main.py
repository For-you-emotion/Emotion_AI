from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dto import Request, Message
from db import get_db
from feedback import saveData, findData, feedback
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
async def getWav(text: str) :
    try :
        return await find(text)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

# wav 파일 이름으로 감정 반환
@app.get("/feelings/{num}")
async def getFeelings(num: str, db: AsyncSession = Depends(get_db)) :
    try :
        return await findDate(num, db)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

# 파일 이름으로 wav 삭제
@app.delete("/{text}")
async def deleteWav(text: str) :
    if await delete(text) is True :
        return Message(message = "삭제 성공!")
    else :
        return Message(message = "삭제 실패...")

@app.post("/feedback/{hwId}/{beadNum}")
async def callFeedbackAI(
        hwId: str, beadNum: int, file: UploadFile = File(...), 
        db: AsyncSession = Depends(get_db)
    ) :
    try :
        fileName = await save(file)

        # result = feedback(request)
        
        await saveData(hwId, beadNum, fileName, db)

        return fileName
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))
