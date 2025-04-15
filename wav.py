from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse

import logging, os

async def save(file: UploadFile) :
    logging.info(".wav 파일 주고받기 테스트")

    if not file.filename.endswith('.wav') :
        raise HTTPException(status_code = 400, detail = ".wav 파일 형식이 다릅니다!")

    filePath = os.path.join("wavFiles", file.filename)

    if os.path.exists(filePath) :
        raise HTTPException(status_code = 409, detail = "동일한 이름의 .wav 파일이 존재합니다!")

    with open(filePath, "wb") as buffer :
        buffer.write(await file.read())

    logging.info(f"정상적으로 파일을 받아 저장하였습니다! : {file.filename}") 

    return FileResponse(filePath, media_type = "audio/wav", filename = file.filename)

async def find(text: str) :
    logging.info(".wav 파일 이름으로 가져 오기")
    
    filePath = os.path.join("wavFiles", str(text) + ".wav")

    if not os.path.exists(filePath) :
        raise HTTPException(status_code = 404, detail = "존재하지 않는 .wav 파일입니다!")
    
    return FileResponse(filePath, media_type = "audio/wav", filename = text)

async def delete(text: str) :
    logging.info(".wav 파일 이름으로 삭제하기")

    filePath = os.path.join("wavFiles", str(text) + ".wav")

    if not os.path.exists(filePath) :
        logging.info("이미 존재하지 않는 .wav 파일입니다")