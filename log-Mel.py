import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

input_folder = 'databases/excerpts/excerpts_audio'
output_root = r'C:\Users\linlo\OneDrive\Desktop\log-Mel'  # "r" для корректной обработки обратных слэшей
os.makedirs(output_root, exist_ok=True)

# Параметры спектрограммы
sr = 48000
n_fft = 1024
hop_length = 256
n_mels = 128
fmin = 20
fmax = 8000

# Обработка всех mp3 файлов
for file in os.listdir(input_folder):
    if file.endswith('.mp3'):
        filename = file[:-4]  # Убираем ".mp3"
        file_path = os.path.join(input_folder, file)

        print(f"Обработка файла: {file_path}")

        # Загрузка аудио
        y, sr_actual = librosa.load(file_path, sr=sr)

        # Mel-спектрограмма
        S = librosa.feature.melspectrogram(y=y, sr=sr_actual, n_fft=n_fft,
                                           hop_length=hop_length, n_mels=n_mels,
                                           fmin=fmin, fmax=fmax)
        log_S = librosa.power_to_db(S, ref=np.max)

        # Создание подпапки
        output_subfolder = os.path.join(output_root, filename)
        os.makedirs(output_subfolder, exist_ok=True)
        # Построение графика
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(log_S, sr=sr_actual, hop_length=hop_length,
                                 x_axis='time', y_axis='mel', fmax=fmax)
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Log-Mel Spectrogram: {filename}')
        plt.tight_layout()
        # Сохранение PNG
        out_path = os.path.join(output_subfolder, f'{filename}_logmel.png')
        plt.savefig(out_path)
        plt.close()