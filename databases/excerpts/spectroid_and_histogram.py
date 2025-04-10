import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB = "excerpts_database.tsv"
df = pd.read_csv(DB, sep="\t", encoding="cp1252")
df = df[df["Technique"].isin(["Growling", "Screaming", "Clean"])]
df = df.dropna(subset=["Spectral_Centroid"])

# descriptive statistics
group_stats = df.groupby('Technique')['Spectral_Centroid'].agg(['mean', 'std', 'count', 'min', 'max'])
print("\n=== Spectral Centroid Statistics ===")
print(group_stats)

# boxplot
plt.figure(figsize=(9, 6))
sns.boxplot(data=df, x="Technique", y="Spectral_Centroid", palette="Set2")
plt.title("Spectral Centroid by Technique")
plt.ylabel("Spectral Centroid (Hz)")
plt.xlabel("Technique")
plt.grid(True)
plt.show()
plt.savefig("spectral_centroid_boxplot.png", dpi=300)

# histogram
plt.figure(figsize=(9, 6))
sns.histplot(data=df, x="Spectral_Centroid", hue="Technique", bins=20, kde=True, palette="Set2", alpha=0.7)
plt.title("Histogram of Spectral Centroid")
plt.xlabel("Spectral Centroid (Hz)")
plt.ylabel("Count")
plt.grid(True)
plt.show()
plt.savefig("spectral_centroid_histogram.png", dpi=300)