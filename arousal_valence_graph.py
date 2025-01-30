# This plot visualizes the relationship between arousal and valence in music.
# The numbers are hypothetical; they represent my understanding of this relationship.
# Feel free to modify it—add more genres, adjust the values, or experiment with different placements.

import numpy as np
import matplotlib.pyplot as plt

# Define the coordinates for different music genres on the arousal-valence plane
music_styles = {
    "Sad Ambient": (-0.7, -0.7),  # Low arousal, low valence
    "Lounge/Jazz": (-0.7, 0.7),   # Low arousal, high valence
    "Happy Pop": (0.7, 0.7),      # High arousal, high valence
    "Extreme Metal (Fans)": (0.8, 0.6),   # High arousal, high valence (for fans)
    "Extreme Metal (Non-fans)": (0.8, -0.6),  # High arousal, low valence (for non-fans)
}

# Create the plot
fig, ax = plt.subplots(figsize=(8, 8))

# Draw the axes
ax.axhline(0, color='black', linewidth=1)  # Horizontal line for valence
ax.axvline(0, color='black', linewidth=1)  # Vertical line for arousal

# Plot each music genre with its respective coordinates
for genre, (arousal, valence) in music_styles.items():
    ax.scatter(arousal, valence, label=genre, s=100)
    ax.text(arousal + 0.05, valence + 0.05, genre, fontsize=10, verticalalignment='center')

# Labels and title
ax.set_xlabel("Arousal (Excitement Level)", fontsize=12)
ax.set_ylabel("Valence (Positive/Negative Emotion)", fontsize=12)
ax.set_title("Music Genres on the Arousal-Valence Plane", fontsize=14)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)

# Grid and legend
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend(loc="lower right", fontsize=9)

# Show the plot
plt.show()
