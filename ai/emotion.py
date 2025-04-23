from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

import numpy as np
import pandas as pd
import librosa
import joblib
import os


def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)


def train_and_save_model(data_csv_path="dataset/emotion_bssm.csv", audio_dir="dataset/audio", model_path="ai/emotion_model.pkl"):
    df = pd.read_csv(data_csv_path)

    features = []
    labels = []

    for index, row in df.iterrows():
        file_path = os.path.join(audio_dir, row["파일 이름"])

        if os.path.exists(file_path):
            feature = extract_features(file_path)
            features.append(feature)
            labels.append(row["감정"])
        else:
            print(f"파일 없음: {file_path}")

    X = np.array(features)
    y = np.array(labels)

    print("특징 추출 완료")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("데이터 분할 완료")

    model = SVC(kernel='linear')
    model.fit(X_train, y_train)
    print("모델 학습 완료")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"모델 정확도: {accuracy:.2f}")

    joblib.dump(model, model_path)
    print(f"모델 저장 완료: {model_path}")


def load_model(model_path="ai/emotion_model.pkl"):
    return joblib.load(model_path)


def predict_emotion(model, audio_path: str) -> str:
    feature = extract_features(audio_path)
    prediction = model.predict([feature])[0]
    return prediction