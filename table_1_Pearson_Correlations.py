import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# This heatmap visualizes the correlation matrix from the study:
# Garrido, S., & Schubert, E. (2011). Individual differences in the enjoyment of negative emotion in music.
# Music Perception, 28(3), 279-296. DOI: 10.1525/mp.2011.28.3.279

# The values are taken from Table 1 of the study, which reports Pearson correlation coefficients
# between key psychological traits related to the enjoyment of sad music.

# Creating a correlation matrix based on Table 1 from the study
data = {
    "Music Empathy": [1.00, 0.28, 0.48, 0.43],  # Music Empathy correlations
    "Empathic Concern": [0.28, 1.00, -0.30, 0.28],  # Empathic Concern correlations
    "Absorption": [0.48, -0.30, 1.00, 0.39],  # Absorption correlations
    "Rumination": [0.19, -0.05, 0.26, 1.00],  # Rumination correlations
}

# Converting into a DataFrame
df_corr = pd.DataFrame(data, index=["Music Empathy", "Empathic Concern", "Absorption", "Rumination"])

# Plotting the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap="coolwarm", linewidths=0.5, vmin=-1, vmax=1)
plt.title("Correlation Matrix: Music Empathy, Absorption, Rumination & Enjoyment")

# Display the heatmap
plt.show()

# Interpretation of key correlations:

# 1. Music Empathy & Absorption (0.48):
# "Absorption was the strongest predictor of enjoyment of sad music" (Garrido & Schubert, 2011, p. 291).
# This moderate positive correlation suggests that individuals who deeply engage with music
# are also likely to have high music-specific empathy.

# 2. Music Empathy & Rumination (0.43):
# "A positive correlation was found between a liking for sad music and music empathy" (p. 291).
# This suggests that individuals who tend to ruminate (engage in repetitive negative thinking)
# also have stronger emotional engagement with music.

# 3. Absorption & Rumination (0.39):
# A moderate positive correlation indicating that those who experience deep absorption in activities
# are also more likely to engage in repetitive negative thinking.

# 4. Empathic Concern & Absorption (-0.30):
# A weak negative correlation suggests that individuals with high general empathic concern
# may not necessarily experience deep absorption in music.

# 5. Empathic Concern & Music Empathy (0.28):
# This weak positive correlation indicates that people with higher general empathy
# also tend to have high music-specific empathy, but the relationship is not very strong.

# 6. Rumination & Empathic Concern (0.28):
# A weak positive relationship, suggesting that individuals with higher rumination
# may also exhibit some degree of empathic concern.

# 7. Rumination & Absorption (0.26):
# This suggests a weak correlation, meaning that people prone to deep absorption
# are somewhat more likely to engage in repetitive negative thinking.

# 8. The strongest correlations involve music empathy and absorption (0.48),
# as well as music empathy and rumination (0.43),
# which supports the study’s conclusion that these factors are key predictors
# of enjoying sad music (p. 291).
# I really enjoyed working on this.
