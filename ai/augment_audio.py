import os
import numpy as np
import librosa
import soundfile as sf

def add_noise(data, noise_level=0.005):
    noise = np.random.randn(len(data))
    return np.clip(data + noise_level * noise, -1, 1)


def time_stretch(data, rate=0.8):
    return librosa.effects.time_stretch(data, rate)


def pitch_shift(data, sr, n_steps):
    return librosa.effects.pitch_shift(data, sr, n_steps)


def change_volume(data, volume_factor=0.5):
    return data * volume_factor


def augment_and_save(file_path, sr, data, augmentation_function, augmentation_name):
    _, filename = os.path.split(file_path)
    new_filename = filename.replace('.wav', f'_{augmentation_name}.wav')
    new_file_path = os.path.join('../../dataset/augmented_audio', new_filename)

    if augmentation_name == 'pitch_shift':
        augmented_data = augmentation_function(data, sr, n_steps=4)
    else:
        augmented_data = augmentation_function(data) if augmentation_function != change_volume else augmentation_function(data, volume_factor=0.5)

    sf.write(new_file_path, augmented_data, sr)
    print(f"✅ 저장됨: {new_file_path}")


def process_folder(folder_path, target_sr=16000):
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(subdir, file)
                data, sr = librosa.load(file_path, sr=target_sr)
                augmentations = [
                    (add_noise, 'noisy'),
                    (time_stretch, 'stretch'),
                    (pitch_shift, 'pitch_shift'),
                    (change_volume, 'volume')
                ]
                for augmentation_function, augmentation_name in augmentations:
                    augment_and_save(file_path, sr, data, augmentation_function, augmentation_name)


if __name__ == "__main__":
    audio_folder = '../../dataset/audio'
    output_folder = '../../dataset/augmented_audio'
    os.makedirs(output_folder, exist_ok=True)

    print("🎧 오디오 증강 시작...")
    process_folder(audio_folder)
    print("✅ 오디오 증강 완료!")
