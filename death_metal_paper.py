import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# This analysis visualizes the data from the study:
# Olsen, K. N., Thompson, W. F., & Giblin, I. (2018).
# Listener expertise enhances intelligibility of vocalizations in death metal music.
# *Music Perception, 35(5), 527-539.* DOI: [10.1525/mp.2018.35.5.527](https://doi.org/10.1525/mp.2018.35.5.527)
#
# The plot compares word recognition accuracy between fans and non-fans of death metal
# for individual words extracted from Cannibal Corpse lyrics (the song is called "Hammer Smashed Face").
#
# The findings support the hypothesis that genre familiarity improves intelligibility,
# even in extreme vocal conditions.

# Data from TABLE 3 in the paper - Word recognition accuracy for individual words
words_data = {
    "Word": ["Continues", "You", "Suffer", "Being", "Coming", "Kill", "Inside", "Feel", "Cortex", "Crushing",
             "Die", "Something", "Like", "Pulverized", "Tissue", "Cranial", "It's", "Cold", "Contents", "Bidding", "I", "Me", "Out", "Killing"],
    "Fans Accuracy (%)": [96.88, 96.88, 90.63, 87.50, 87.50, 87.50, 84.38, 81.25, 78.13, 78.13,
                          78.13, 75.00, 37.50, 43.75, 50.00, 15.63, 71.88, 62.50, 53.13, 43.75, 40.63, 40.63, 21.88, 78.13],
    "Non-Fans Accuracy (%)": [90.63, 75.00, 87.50, 68.75, 90.63, 53.13, 59.38, 59.38, 68.75, 78.13,
                              68.75, 65.63, 46.88, 40.63, 31.25, 3.13, 46.88, 40.63, 40.63, 12.50, 28.13, 18.75, 12.50, 56.25]
}

df_words = pd.DataFrame(words_data)

# Sort words by descending accuracy (average of fans and non-fans)
df_words["Avg Accuracy"] = (df_words["Fans Accuracy (%)"] + df_words["Non-Fans Accuracy (%)"]) / 2
df_words = df_words.sort_values(by="Avg Accuracy", ascending=False)

# A scatter plot to compare word recognition accuracy between fans and non-fans
plt.figure(figsize=(12, 6))
sns.scatterplot(x="Word", y="Fans Accuracy (%)", data=df_words, label="Fans", color="blue", s=100)
sns.scatterplot(x="Word", y="Non-Fans Accuracy (%)", data=df_words, label="Non-Fans", color="red", s=100)

plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.title("Word Recognition Accuracy: Fans vs. Non-Fans (Sorted by Accuracy)")
plt.ylabel("Word Recognition Accuracy (%)")
plt.xlabel("Words (Sorted by Avg Accuracy)")
plt.legend()
plt.grid(True)
plt.show(block=False)
plt.pause(1000)

# Discussion of results:
# - Fans generally recognize words better than non-fans.
# - The results suggest that exposure to death metal improves perception of its distorted vocals.
# - Future research could examine whether long-term exposure to extreme metal affects broader speech perception skills.
