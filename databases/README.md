# Metal Music Databases

This directory contains all the datasets developed as part of the research on the perception, aesthetics, and acoustic structure of extreme metal vocals. 
Each subdirectory includes a specific database with its own metadata files, audio folder and a dedicated `README.md` describing its contents, structure, and purpose.

## Available Datasets

- [`EMVT_database`](./EMVT_database/)  
  (In development) A large-scale dataset with over 1000 annotated vocal fragments representing diverse techniques and vocal effects. 
See `emvt/README.md` for current status.

- [`excerpts/`](./excerpts/)  
  Source excerpts from lesser-known metal tracks, used as the foundation for all stimulus sets. 
Includes detailed metadata for each excerpt.

- [`metal_vox/`](./metal_vox/)  
  An extended stimuli set with recordings from 6 vocalists across six conditions (3 techniques × 2 melodic contexts).
Includes detailed metadata and audio in dual-channel format.

- [`triple_twelve_stimuli_set/`](./triple_twelve/)  
  A controlled stimulus set consisting of 12 identical and 12 unique excerpts recorded by 12 vocalists in two conditions (with/without melody) and three vocal techniques.

---

Each dataset folder contains:
- A metadata file (`.tsv`)
- A dedicated `README.md` with full documentation
- An optional `audio/` folder with WAV or MP3 files

For more context on how these datasets are used in the experiment and analysis, see the [main project README](../README.md).
