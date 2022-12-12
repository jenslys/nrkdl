# nrkdl

[![Releases](https://img.shields.io/github/v/release/jenslys/nrkdl.svg)](https://github.com/jenslys/nrkdl/releases/)

Download content from nrk.no

**Disclaimer:** This is for educational purposes **ONLY**.

## Table of contents

- [nrkdl](#nrkdl)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)
  - [Updating](#updating)
    - [System requirements](#system-requirements)
  - [Usage](#usage)
    - [Example usage](#example-usage)
      - [Download an entire tv-show with subtitles](#download-an-entire-tv-show-with-subtitles)
      - [Download a single tv-show episode](#download-a-single-tv-show-episode)
      - [Download a movie](#download-a-movie)
      - [Search for a series and download all seasons](#search-for-a-series-and-download-all-seasons)
      - [Search for a specific episode](#search-for-a-specific-episode)
    - [Supported sites](#supported-sites)


  
## Installation

```bash
pip install nrkdl
```

## Updating

```bash
pip install nrkdl --upgrade
```

### System requirements

- [python3](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)
- [ffmpeg](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

## Usage

```text
usage: nrkdl.py [-h] (--search SEARCH | --url URL) [--season SEASON] [--episode EPISODE] [--write-subs] [--keep-subs] [--audio-only] [--write-metadata]

options:
  -h, --help         show this help message and exit
  --search SEARCH    Search for Movie/TV-show, and then download (e.g: Exit)
  --url URL          URL for the Movie/TV-show (e.g: https://tv.nrk.no/program/KOID75006720)
  --season SEASON    Season number (e.g: 1) (Only works if --search is used) (0 for all)
  --episode EPISODE  Episode number (e.g: 1) (Only works if --search is used) (0 for all)
  --write-subs       Download and embed subtitles to file
  --keep-subs        Prevent the subtitle files from being deleted after being embeded
  --audio-only       Only extract audio files
  --write-metadata   Write metadata to file
```

### Example usage

#### Download an entire tv-show with subtitles

```bash
nrkdl --url https://tv.nrk.no/serie/exit --write-subs
```

#### Download a single tv-show episode

```bash
nrkdl --url https://tv.nrk.no/serie/exit/sesong/2/episode/6/
```

#### Download a movie

```bash
nrkdl --url https://tv.nrk.no/program/MSUI31006017
```

#### Search for a series and download all seasons

```bash
nrkdl --search rådebank --season 0
```

#### Search for a specific episode

```
nrkdl --search exit --season 2 --episode 6
```

### Supported sites

```text
NRK
NRKPlaylist
NRKRadioPodkast
NRKSkole: NRK Skole
NRKTV: NRK TV and NRK Radio
NRKTVDirekte: NRK TV Direkte and NRK Radio Direkte
NRKTVEpisode
NRKTVEpisodes
NRKTVSeason
NRKTVSeries
```
