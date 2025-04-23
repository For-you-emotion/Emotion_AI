from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from db import get_db
from feedback import saveData, findData, feedback, detect
from wav import save, find
from trans import tts, stt
from ai.emotion import train_and_save_model, load_model, predict_emotion

import logging, os, sys

app = FastAPI()

# 모델 불러오기 ( 없을 경우 생성 )
if not os.path.exists("ai/emotion_model.pkl"):
    train_and_save_model(model_path = "ai/emotion_model.pkl")
model = load_model()

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

# Main 기능 : 음성 데이터로부터 AI 감정 분석 후 AI 피드백 반환
@app.post("/wavTest")
async def callDetectAI(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)) :
    try :
        reqPath = await save(file)
        reqPath = os.path.join("wavFiles", reqPath + ".wav")

        logging.info("wav to text 변환")
        memory = stt(reqPath)
        
        logging.info("AI를 통해 감정 판별!")
        feelings = predict_emotion(model, reqPath)        
        feelings = detect(memory, feelings)

        fileName = datetime.now().strftime("%y%m%d%H%M%S") 

        result = feedback(memory, feelings)
        await saveData(fileName, "hwIdTest", 1, memory, feelings, result, db)
        tts(result, fileName)
        
        return fileName
    except HTTPException as httpEx :
        raise httpEx
    except Exception as e :
        raise HTTPException(status_code = 500, detail = str(e))