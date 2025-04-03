import pandas as pd
from scipy.stats import f_oneway, ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd

DB = "excerpts_database.tsv"
df = pd.read_csv(DB, sep="\t", encoding="cp1252")
df = df[df["Spectral_Centroid"].notna()]  # remove NaNs if any

growling = df[df["Technique"] == "Growling"]["Spectral_Centroid"]
screaming = df[df["Technique"] == "Screaming"]["Spectral_Centroid"]
clean = df[df["Technique"] == "Clean"]["Spectral_Centroid"]
print("\n=== Descriptive Statistics ===")
desc = df.groupby("Technique")["Spectral_Centroid"].describe()
print(desc)

# ANOVA
print("\n=== ANOVA ===")
f_stat, p_value = f_oneway(growling, screaming, clean)
print(f"F = {f_stat:.3f}, p = {p_value:.3f}")

# t-test: Growling vs Screaming
print("\n=== T-test (Growling vs Screaming) ===")
t_stat, p_value = ttest_ind(growling, screaming)
print(f"t = {t_stat:.3f}, p = {p_value:.3f}")

# Post-hoc Tukey HSD
print("\n=== Tukey HSD Post-hoc Test ===")
result = pairwise_tukeyhsd(endog=df["Spectral_Centroid"],
                           groups=df["Technique"],
                           alpha=0.05)
print(result)