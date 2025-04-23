# Emotion AI Server
사용자 음성 기반 AI 감정 분석 및 피드백 제공 구술, Emotion

<br>

## Tech Stack
**Dev** : ```Python(version : 3.13.0)```  ```FastAPI``` ```MySQL``` <br>

**OS** : ```Linux``` <br>

**Build** : ```uvicorn``` -> ```Docker + Docker compose```

<br>

## How to Run
```shell
> git clone https://github.com/wwwxsv19/Emotion_AI.git 
```
```shell
> docker build -f Emotion_AI/Dockerfile -t emotion .
```
```shell
> docker compose up --build -d
```
