# Metal Music Research  
**A Deep Dive into the Aesthetics, Perception, and Complexity of Metal Music**

## About this Project  
This repository contains the source code and supporting materials for our research on extreme metal vocal perception. Our research investigates the perceptual differences between metal fans and non-fans with respect to extreme metal vocal techniques. We focus on the intelligibility and cognitive processing of vocal expressions such as growling and screaming, comparing their performance when rendered in both their original form and with additional pitch contours ("vocalized" versions). Stimuli are constructed from lesser-known, uncharted metal releases using Spotify's popularity metrics, ensuring that the excerpts are as unfamiliar as possible to experimental participants. The study explores the influence of listening expertise on the decoding of extreme vocal sounds and aims to shed light on the cognitive mechanisms involved in music perception.
 The final experimental stimuli are derived from real metal recordings and then re-recorded in five different vocal conditions.
- **"Extra"** folder contains everything outside our research. It mostly contains the visualizations of other metal-related papers' findings.

## Research Context  
This work will be presented at the **18th International Conference on Music Perception and Cognition** in July 2025. The research contributes to ongoing discussions in the field by providing empirical data on the role of familiarity in the cognitive processing of aggressive vocal styles in metal music. Our current research focuses on understanding the unique characteristics of extreme metal vocals. Key components of our study include:

- **Stimuli Selection and Rationale:**  
  We extract source excerpts from lesser-known, studio-recorded albums by authentic and well-known metal bands. The selection is based on Spotify popularity metrics—specifically targeting recordings with low stream counts and popularity scores that have never appeared on major charts (e.g., Billboard Metal, UK Rock & Metal). Whether or not the album serving as material for our stimuli set has ever appeared in the above-mentioned charts is checked manually. Additionally, live releases are excluded via name-based filtering to prevent skewing the data. Releases and songs marked as "Remastered", "Re-issue", "Reissue", "Demo" and "Edition" are excluded as well. 

- **Stimuli Extraction Procedure:**  
  To capture the "core" of a vocal performance, we skip the first 30% of each track (which often contains intros or ambient passages) and extract a vocal phrase fragment of approximately 10–12 syllables. This method ensures that the excerpt represents a complete vocal phrase, adhering to the physiological constraints on breath and vocal production.
- **Recording Protocol:**  
  Professional metal vocalists are recruited to re-record the selected excerpts in five different vocal conditions. These re-recorded stimuli form the basis of our perceptual experiment, where participants are asked to "sing back" the excerpts.
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

# Databases
## Excerpts Database

This database contains examples of extreme vocal techniques in metal music and serves as the basis for constructing our stimulus set. It was created through the following steps:

- We conducted an exploration of Reddit discussions and metal-focused platforms such as **Loudwire** to identify the top artists associated with three specific extreme vocal techniques. Artists were selected based on community mentions, rankings, and discussions highlighting the most prominent performers of each technique.
- Using the **Spotify {UN}Popularity Analyzer** tool, we exported the discographies of these artists, focusing exclusively on studio albums. Releases labeled *live*, *remastered*, *re-issue*, *bonus*, *deluxe*, *demo*, or *edition* were excluded from the dataset.
- For each album, we listened to the **three least popular tracks** on Spotify. Instrumental tracks, those shorter than 59 seconds, instrumental tracks, or those not featuring the target vocal technique were excluded and replaced by the next least popular track on the same album.
- A time segment was selected from each qualifying track using the **Timecode Selector** app. If the suggested excerpt did not contain the target technique, a manual check was performed within a ±25 second range around the suggested timecode.
- The final excerpt was then cut and exported using the Audacity audio editor. One second of silence was added both at the beginning and the end of each excerpt.

### Unpopularity Exports

Unpopularity exports are `.txt` files generated using the **Spotify {UN}Popularity Analyzer**. These files contain data on the least popular releases of a selected artist, retrieved via the Spotify API.

Each export includes:
- The artist's name and the local timestamp of the export
- The **three least popular studio albums** (or more/less depending on the setting)
- For each album, **up to three least popular tracks**, sorted by Spotify's internal popularity metric
- Manual annotations regarding track/album exclusions and stream count data

Albums and tracks labeled as *live*, *remastered*, *re-issue*, *demo*, *edition*, or *bonus* are excluded from exports to maintain consistency and avoid duplicates.

Additionally:
- The **most popular track** and its **stream count** are manually added to each file based on Spotify web data
- Stream counts for selected tracks are also retrieved manually from Spotify’s website, as this data is not available through the API


___
In addition to the conference project, this repository will also serve as a central hub for materials related to other ongoing research initiatives on metal music. Please check back regularly for updates, as this README and the repository content will be continuously revised to reflect new findings and developments.