from gtts import gTTS
from pydub import AudioSegment
from fastapi import HTTPException

import speech_recognition as sr
import os, logging, subprocess

# Recognizer 생성
rcg = sr.Recognizer()

def changeSpeed(sound: AudioSegment, speed: float) -> AudioSegment:
    new_frame_rate = int(sound.frame_rate * speed)
    return sound._spawn(sound.raw_data, overrides={"frame_rate": new_frame_rate}).set_frame_rate(sound.frame_rate)

def convert(input_path: str, output_path: str):
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-acodec", "pcm_s16le", "-ar", "16000", output_path
    ], check=True)

# 음성 -> 텍스트
def stt(reqPath: str) :
    outputPath = os.path.join("wavFiles", "output.wav")
    convert(reqPath, outputPath)

    with sr.AudioFile(outputPath) as source:
        audio = rcg.record(source)  # 전체 파일을 읽어들임

    try:
        text = rcg.recognize_google(audio, language='ko')
        logging.info("인식된 음성 : " + text)
        return text
    except sr.UnknownValueError :
        raise HTTPException(status_code = 400, detail = "음성을 인식할 수 없습니다!")
    except sr.RequestError as e :
        raise HTTPException(status_code = 500, detail = "Google API 요청 실패 : {e}")

# 텍스트 -> 음성
def tts(msg: str, fileName: str) :
    tts = gTTS(text = msg, lang = "ko")
    
    mp3Path = os.path.join("wavFiles", fileName + ".mp3")
    wavPath = os.path.join("wavFiles", fileName + ".wav")

    tts.save(mp3Path)

    sound = AudioSegment.from_mp3(mp3Path)
    sound = changeSpeed(sound, 1.5)
    sound = sound.set_frame_rate(8000).set_channels(1).set_sample_width(1)
    sound.export(wavPath, format = "wav")