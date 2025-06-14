# Metal Music Research  
**A Deep Dive into the Aesthetics, Perception, and Complexity of Metal Music**

## About this Project  
This repository contains the source code and supporting materials for our research on extreme metal vocal perception. Our research investigates the perceptual differences between metal fans and non-fans with respect to extreme metal vocal techniques. We focus on the intelligibility and cognitive processing of vocal expressions such as growling and screaming, comparing their performance when rendered in both their original form and with additional pitch contours ("vocalized" versions). Stimuli are constructed from lesser-known, uncharted metal releases using Spotify's popularity metrics, ensuring that the excerpts are as unfamiliar as possible to experimental participants. The study explores the influence of listening expertise on the decoding of extreme vocal sounds and aims to shed light on the cognitive mechanisms involved in music perception.
The final experimental stimuli are derived from real metal recordings and then re-recorded in five different vocal conditions.

## Research Context  
This work will be presented at the **18th International Conference on Music Perception and Cognition** in July 2025. The research contributes to ongoing discussions in the field by providing empirical data on the role of familiarity in the cognitive processing of aggressive vocal styles in metal music. Our current research focuses on understanding the unique characteristics of extreme metal vocals. Key components of our study include:

- **Stimuli Selection and Rationale:**  
  We extract source excerpts from lesser-known, studio-recorded albums by authentic and well-known metal bands. The selection is based on Spotify popularity metrics—specifically targeting recordings with low stream counts and popularity scores that have never appeared on major charts (e.g., Billboard Metal, UK Rock & Metal). Whether or not the album serving as material for our stimuli set has ever appeared in the above-mentioned charts is checked manually. Additionally, live releases are excluded via name-based filtering to prevent skewing the data. Releases and songs marked as "Remastered", "Re-issue", "Reissue", "Demo" and "Edition" are excluded as well. 

- **Stimuli Extraction Procedure:**  
  To capture the "core" of a vocal performance, we skip the first 30% of each track (which often contains intros or ambient passages) and extract a vocal phrase fragment of approximately 10–12 syllables. This method ensures that the excerpt represents a complete vocal phrase, adhering to the physiological constraints on breath and vocal production.
- **Recording Protocol:**  
  Professional metal vocalists are recruited to re-record the selected excerpts in five different vocal conditions. These re-recorded stimuli form the basis of our perceptual experiment, where participants are asked to "sing back" the excerpts.

# Databases

This repository includes several curated datasets used in the study of extreme metal vocal techniques. Each dataset is provided with its own `.tsv` file and a dedicated `README.md` containing detailed descriptions of its structure, collection process, and file organization.

### Available Databases:

- **METALVOX Stimuli Set (Extended Conditions)**  
  Recordings from 5 vocalists performing fragments in six conditions (3 techniques × 2 melodic contexts). Includes detailed time-aligned annotations and audio mappings.  
  📄 See `databases/metal_vox/README.md` for structure and usage.

- **Triple Twelve Stimuli Set**  
  Recordings from 12 vocalists performing 12 identical and 12 unique fragments across three vocal techniques (Clean, Screaming, Growling) and two conditions (with/without melody).  
  📄 See `databases/triple_twelve/README.md` for metadata and protocol.

- **Excerpts Database**  
  A curated collection of vocal excerpts extracted from lesser-known extreme metal tracks.  
  This database serves as the **core source** for all other stimulus sets in this project: each recording in the Triple Twelve, METALVOX and EMVT datasets is a re-recorded version of an excerpt selected from this database.  
  Includes metadata such as vocal technique, artist, album, track popularity, timecodes, rhythmic and melodic transcriptions, spectral centroid values, and more.  
  📄 See `databases/excerpts/README.md` for full details.

- **EMVT Database**  
  An upcoming large-scale dataset containing over **1000 vocal fragments** covering a wide range of extreme metal vocal techniques and vocal effects.  
  This database aims to provide extended coverage of diverse vocal effects (e.g., pig squeals, banshee screams, zombie growls), hybrid styles, and rare vocal gestures, collected from studio recordings and annotated live sessions.  
  The database is currently under construction and will be released in future versions of this repository.  
  📄 Documentation and metadata will be available in `databases/EMVT_database/README.md` once finalized.

Each dataset is accompanied by audio files located in the corresponding `audio/` folder and is referenced by its metadata table. These resources are designed to support reproducibility and transparency in research on metal vocal perception.

# Spotify Tools
## Spotify {UN}Popularity Analyzer  
The **Spotify 'UN'Popularity Analyzer 0.3** is a Python-based GUI application developed as part of our research. It serves to build a database of musical fragments and evaluate popularity metrics using the Spotify API. The tool provides:

- **Search Bar:**  
  Supports pressing Enter or clicking the "Search" button to trigger an artist search.

- **Artist Matches List:**  
  Displays up to five artist matches for the entered query.

- **Artist Discography:**  
  Lists albums (excluding live albums and tracks via name-based filtering, as required for our research).

- **Resizable Charts:**  
  Charts automatically fill the entire allocated space in the GUI, displaying overall album popularity as well as track popularity for the selected album.

- **Raw Data Window:**  
  Provides a scrollable view of the quantitative data (in JSON format) from the Spotify API. You can call this function from **File** menu.

- **File Menu:**  
  Includes an "Export Unpopularity..." function that exports the artist's 1,2,3,4,5 least popular (or all) albums and up to three least popular tracks per album, along with local time zone information and the data source ("Spotify API"). Is is also possible to **delete items manually** from the discography list in the app before exporting (click on an item and press *delete*). This export function is a key component for creating our stimuli set. 

## Timecode Selector
The **Timecode Selector** is a Python-based GUI tool designed to randomly select a timecode excerpt from a song for our research on metal music.  
***# I also need to describe the functions of this tiny app as well? hm, okay***  
It is used to choose a segment from a musical example based on user-specified parameters like **Total Duration Input**, **Skip Percentage** and **Required Excerpt Length**.

# Spectral Centroid.py
The `spectral_centroid.py` script is designed to compute the **Spectral Centroid** of each excerpt in the **Excerpts Database**.  
It takes each `.mp3` excerpt from the **MP3_Path** column, calculates the average **Spectral Centroid** (in Hz), and exports the results.

### How it works
- Reads the database file: `databases/excerpts/excerpts_database.tsv`.
- Loads each audio excerpt from the corresponding path in `databases/excerpts/excerpts_audio/`.
- Computes the mean **Spectral Centroid** using the [Librosa](https://librosa.org/) library.
- Saves the results, including: *Excerpt ID, Technique, Artist, Album, Song, Spectral Centroid*, to a `.tsv` file: `databases/excerpts/spectral_centroid_results.tsv`.
- Prints the results and mean Spectral Centroid per technique to the terminal.
___
In addition to the conference project, this repository will also serve as a central hub for materials related to other ongoing research initiatives on metal music. Please check back regularly for updates, as this README and the repository content will be continuously revised to reflect new findings and developments.