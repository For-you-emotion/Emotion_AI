from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from dto import Request 
from db import get_db
from feedback import saveData, feedback

import logging, os, sys

app = FastAPI()

@app.get("/")
def read_root() :
    return {'Hello Emotion!'}

@app.post("/wavTest")
async def getWavFile(file: UploadFile = File(...)) :
    logging.info(f"작업 : {sys.path}")
    logging.info(".wav 파일 주고받기 테스트")

    if not file.filename.endswith('.wav') :
        raise HTTPException(status_code = 400, detail = ".wav 파일 형식이 다릅니다!")
    
    filePath = os.path.join("wavFiles", file.filename)

    with open(filePath, "wb") as buffer :
        buffer.write(await file.read())

    logging.info(f"정상적으로 파일을 받아 저장하였습니다! : {file.filename}")

    return FileResponse(filePath, media_type = 'audio/wav', filename = file.filename)


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
