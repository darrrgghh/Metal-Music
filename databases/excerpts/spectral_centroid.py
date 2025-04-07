import pandas as pd
import librosa
import numpy as np
import os

###############################################
# paths
DB_PATH = "excerpts_database.tsv"
AUDIO_FOLDER = "databases/excerpts/excerpts_audio/"
EXPORT_PATH = "databases/excerpts/spectral_centroid_results.tsv"
# loading database of excerpts
df = pd.read_csv(DB_PATH, sep="\t", encoding="cp1252")

# I will be just changing these paths and run the script on other databases as well
###############################################

# using librosa to compute spectral centroid of each excerpt
def compute_spectral_centroid(mp3_path):
    try:
        y, sr = librosa.load(mp3_path, sr=None)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        return np.mean(centroid)
    except Exception as e:
        print(f"File error {mp3_path}: {e}")
        return np.nan
results = []
for idx, row in df.iterrows():
    mp3_filename = os.path.basename(row["MP3_Path"])
    mp3_path = os.path.join(AUDIO_FOLDER, mp3_filename)
    centroid = compute_spectral_centroid(mp3_path)
    results.append({
        "Excerpt_ID": row["Excerpt_ID"],
        "Technique": row["Technique"],
        "Artist": row["Artist"],
        "Album": row["Album"],
        "Song": row["Song"],
        "Spectral_Centroid": centroid
    })
# into the dataframe
centroid_df = pd.DataFrame(results)

# order by Excerpt_ID
centroid_df.sort_values(by="Excerpt_ID", inplace=True)
print("\n=== Spectral Centroid of each excerpt ===")
print(centroid_df.to_string(index=False))

# printing means as well
group_means = centroid_df.groupby('Technique')['Spectral_Centroid'].mean()
print("\n=== Mean Spectral Centroid per technique ===")
print(group_means)

# export as csv
# centroid_df.to_csv(EXPORT_PATH, sep="\t", index=False, encoding="utf-8")
# print(f"\nResults saved to{EXPORT_PATH}")