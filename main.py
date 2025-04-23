from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from feedback import saveData, findData, feedback
from wav import save, find

import logging, os, sys

app = FastAPI()

# 파일 이름으로 wav 반환
@app.get("/wav/{num}")
async def getWav(num: str) :
    try :
        return await find(num)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))

# wav 파일 이름으로 감정 반환
@app.get("/feelings/{num}")
async def getFeelings(num: str, db: AsyncSession = Depends(get_db)) :
    try :
        return await findData(num, db)
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))