import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time


# This analysis visualizes the data from the study:
# Olsen, K. N., Thompson, W. F., & Giblin, I. (2018).
# Listener expertise enhances intelligibility of vocalizations in death metal music.
# *Music Perception, 35(5), 527-539.* DOI: [10.1525/mp.2018.35.5.527](https://doi.org/10.1525/mp.2018.35.5.527)
#
# The first plot compares word recognition accuracy between fans and non-fans of death metal
# for individual words extracted from Cannibal Corpse lyrics (the song is called "Hammer Smashed Face").
#
# The second plot visualizes the average recognition accuracy for metal-related and neutral words,
# showing differences in perception between fans and non-fans.
#
# The findings support the hypothesis that genre familiarity improves intelligibility,
# even in extreme vocal conditions.

# Data from TABLE 3 in the paper - Word recognition accuracy for individual words
words_data = {
    "Word": ["Continues", "You", "Suffer", "Being", "Coming", "Kill", "Inside", "Feel", "Cortex", "Crushing",
             "Die", "Something", "Like", "Pulverized", "Tissue", "Cranial"],
    "Fans Accuracy (%)": [96.88, 96.88, 90.63, 87.50, 87.50, 87.50, 84.38, 81.25, 78.13, 78.13,
                          78.13, 75.00, 37.50, 43.75, 50.00, 15.63],
    "Non-Fans Accuracy (%)": [90.63, 75.00, 87.50, 68.75, 90.63, 53.13, 59.38, 59.38, 68.75, 78.13,
                              68.75, 65.63, 46.88, 40.63, 31.25, 3.13],
    # Context labels from TABLE 2 in the paper (Context-Congruent = Metal-related, Context-Neutral = Not Metal-related)
    "Context": ["Neutral", "Neutral", "Metal", "Neutral", "Metal", "Metal", "Metal", "Metal", "Metal", "Metal",
                "Metal", "Neutral", "Neutral", "Metal", "Neutral", "Metal"]
}

df_words = pd.DataFrame(words_data)

# A scatter plot to compare word recognition accuracy between fans and non-fans
plt.figure(figsize=(12, 6))
sns.scatterplot(x="Word", y="Fans Accuracy (%)", data=df_words, label="Fans", color="blue", s=100)
sns.scatterplot(x="Word", y="Non-Fans Accuracy (%)", data=df_words, label="Non-Fans", color="red", s=100)

plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.title("Word Recognition Accuracy: Fans vs. Non-Fans")
plt.ylabel("Word Recognition Accuracy (%)")
plt.xlabel("Words")
plt.legend()
plt.grid(True)
plt.show(block=False)  # Show without blocking execution

# Additional question: Do fans recognize metal-related words better than non-metal words?
metal_words = df_words[df_words["Context"] == "Metal"]
neutral_words = df_words[df_words["Context"] == "Neutral"]

avg_metal_fans = metal_words["Fans Accuracy (%)"].mean()
avg_metal_nonfans = metal_words["Non-Fans Accuracy (%)"].mean()
avg_neutral_fans = neutral_words["Fans Accuracy (%)"].mean()
avg_neutral_nonfans = neutral_words["Non-Fans Accuracy (%)"].mean()

print("\nAverage Word Recognition Accuracy by Context:")
print(f"Fans (Metal words): {avg_metal_fans:.2f}%")
print(f"Non-Fans (Metal words): {avg_metal_nonfans:.2f}%")
print(f"Fans (Neutral words): {avg_neutral_fans:.2f}%")
print(f"Non-Fans (Neutral words): {avg_neutral_nonfans:.2f}%")

# Visualizing the results: Metal vs. Neutral words recognition accuracy
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Metal words recognition accuracy
sns.barplot(x=["Fans", "Non-Fans"], y=[avg_metal_fans, avg_metal_nonfans], ax=axes[0], palette="coolwarm")
axes[0].set_title("Recognition Accuracy - Metal Words")
axes[0].set_ylim(50, 80)
axes[0].set_ylabel("Accuracy (%)")

# Neutral words recognition accuracy
sns.barplot(x=["Fans", "Non-Fans"], y=[avg_neutral_fans, avg_neutral_nonfans], ax=axes[1], palette="coolwarm")
axes[1].set_title("Recognition Accuracy - Neutral Words")
axes[1].set_ylabel("Accuracy (%)")
plt.show(block=False)
plt.pause(1000)

# Discussion of results:
# - Fans generally recognize words better than non-fans, regardless of context.
# - However, the gap in recognition accuracy is more pronounced for metal-related words.
# - This supports the hypothesis that exposure to death metal improves perception of its distorted vocals.
# - Neutral words are still recognized well, indicating that fan expertise does not only apply to metal words.
# - Future research could examine whether long-term exposure to extreme metal affects broader speech perception skills.
