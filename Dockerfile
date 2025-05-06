FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y flac && \
    apt-get clean

WORKDIR /app

COPY emotion/dataset /app/dataset
COPY emotion/Emotion_AI/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY emotion/Emotion_AI/. .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000