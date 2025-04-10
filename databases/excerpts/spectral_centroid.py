import pandas as pd
import librosa
import numpy as np
import os

###############################################
# paths
DB_PATH = "excerpts_database.tsv"
AUDIO_FOLDER = "excerpts_audio"
EXPORT_PATH = "spectral_centroid_results.tsv"
# loading database of excerpts
df = pd.read_csv(DB_PATH, sep="\t", encoding="cp1252")
# I will be just changing these paths and run the script on other databases as well
###############################################

# using librosa to compute spectral centroid and duration of each excerpt excluding 2 seconds of silence
def analyze_audio(mp3_path):
    try:
        y, sr = librosa.load(mp3_path, sr=None)

        padding = sr
        if len(y) < 2 * padding:
            return np.nan, 0
        y_trimmed = y[padding:-padding]
        duration_ms = len(y_trimmed) / sr * 1000
        centroid = librosa.feature.spectral_centroid(y=y_trimmed, sr=sr)
        return np.mean(centroid), duration_ms

    except Exception as e:
        print(f"File error {mp3_path}: {e}")
        return np.nan, 0
results = []
for idx, row in df.iterrows():
    mp3_filename = os.path.basename(row["MP3_Path"])
    mp3_path = os.path.join(AUDIO_FOLDER, mp3_filename)

    centroid, duration_ms = analyze_audio(mp3_path)

    results.append({
        "Excerpt_ID": row["Excerpt_ID"],
        "Technique": row["Technique"],
        "Artist": row["Artist"],
        "Album": row["Album"],
        "Song": row["Song"],
        "Spectral_Centroid": centroid,
        "Duration_ms": round(duration_ms, 2)
    })

# printing results to console
centroid_df = pd.DataFrame(results)
centroid_df.sort_values(by="Excerpt_ID", inplace=True)

print("\n=== Spectral Centroid of each excerpt ===")
print(centroid_df.to_string(index=False))

print("\n=== Mean Spectral Centroid per technique ===")
print(centroid_df.groupby('Technique')['Spectral_Centroid'].mean())

# export to csv
centroid_df.to_csv(EXPORT_PATH, sep="\t", index=False, encoding="utf-8")
print(f"\nResults are saved to {EXPORT_PATH}")