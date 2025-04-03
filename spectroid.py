import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Paths ===
DB_PATH = "databases/excerpts/excerpts_database.tsv"

# === Load Data ===
df = pd.read_csv(DB_PATH, sep="\t", encoding="cp1252")

# === Filter only techniques of interest ===
df = df[df["Technique"].isin(["Growling", "Screaming", "Clean"])]
df = df.dropna(subset=["Spectral_Centroid"])

# === Print descriptive statistics ===
group_stats = df.groupby('Technique')['Spectral_Centroid'].agg(['mean', 'std', 'count', 'min', 'max'])
print("\n=== Spectral Centroid Statistics ===")
print(group_stats)

# === Plot Boxplot ===
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="Technique", y="Spectral_Centroid", palette="Set2")
plt.title("Spectral Centroid by Technique")
plt.ylabel("Spectral Centroid (Hz)")
plt.xlabel("Technique")
plt.grid(True)
plt.show()
#plt.savefig("databases/excerpts/spectral_centroid_boxplot.png", dpi=300)

# === Plot Histogram ===
plt.figure(figsize=(9, 6))
sns.histplot(data=df, x="Spectral_Centroid", hue="Technique", bins=20, kde=True, palette="Set2", alpha=0.7)
plt.title("Histogram of Spectral Centroid")
plt.xlabel("Spectral Centroid (Hz)")
plt.ylabel("Count")
plt.grid(True)
plt.show()
#plt.savefig("databases/excerpts/spectral_centroid_histogram.png", dpi=300)
