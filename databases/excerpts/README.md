## Excerpts Database

This database contains examples of extreme vocal techniques in metal music and serves as the basis for constructing our stimulus set. It was created through the following steps:

- We conducted an exploration of Reddit discussions and metal-focused platforms such as **Loudwire** to identify the top artists associated with three specific extreme vocal techniques. Artists were selected based on community mentions, rankings, and discussions highlighting the most prominent performers of each technique.
- Using the **Spotify {UN}Popularity Analyzer** tool, we exported the discographies of these artists, focusing exclusively on studio albums. Releases labeled *live*, *remastered*, *reissue*, *re-issue*, *edition*, *deluxe*, *demo*, *edition*, *compilation*, *remix* and *remixed* were excluded from the dataset.
- For each album, we listened to the **three least popular tracks** on Spotify. Instrumental tracks, those shorter than 59 seconds, instrumental tracks, or those not featuring the target vocal technique were excluded and replaced by the next least popular track on the same album.
- A time segment was selected from each qualifying track using the **Timecode Selector** app. If the suggested excerpt did not contain the target technique, a manual check was performed within a ±25 second range around the suggested timecode.
- The final excerpt was then cut and exported using the Audacity audio editor. One second of silence was added both at the beginning and the end of each excerpt.

Each excerpt in the database includes the following:

- **Excerpt ID** in the format "EXCE-001" up to "EXCE-999".  
- **Technique**: one of the three extreme vocal techniques that are the focus of our research (growling, screaming, and clean vocals).  
- **Artist**  
- **Album**  
- **Year**  
- **Album Popularity**: this metric is taken directly from the Spotify API.  
- **Song**  
- **Stream Count**: this metric is not available via the Spotify API, so it is taken from the Spotify website and manually added to the table.  
- **Track Popularity**: this metric is taken directly from the Spotify API.  
- **Duration**  
- **Timecode**: the specific fragment of the song from which a phrase containing the target vocal technique is extracted.  
- **Lyrics**: the lyrics of the selected passage, taken from the Spotify website.  
- **Rhythmic representation**: A symbolic transcription of the rhythmic pattern of the excerpt in Humdrum format.
- **Melodic Representation**: A symbolic transcription of the melodic contour of the excerpt in Humdrum format (**Screaming** and **Growling** in human language).
- **Time Signature**: The time signature of the song section containing the excerpt. Most of duple meter is indicated as 4/4.
- **Tempo (approx.)**: The approximate tempo in BPM of the excerpted section. Tempo values were initially obtained using online BPM detection tools, and then manually verified and tapped multiple times using the BPM Tapper feature in **GarageBand**.
- **Spectral Centroid**: The average spectral centroid (in Hz) computed for each excerpt. This feature reflects the "brightness" or "sharpness" of the sound and is commonly used in music information retrieval as an indicator of timbral quality. Higher values correspond to higher-frequency energy in the signal.
- **Spotify URL** of the song.  
- **MP3 Path** to locate the song within the database’s root directory.  
- **Date Collected**: since popularity metrics and stream counts change constantly, we also include the date when these metrics were collected.  

### Web Version

A more extensive and continuously updated version of this database is available online:

🔗 [The Database of Extreme Metal Vocal Techniques](https://extreme-vocal-techniques-db.onrender.com/)
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