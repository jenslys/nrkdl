# nrkdl

<a href="https://github.com/jenslys/nrkdl/releases/"><img src="https://img.shields.io/github/v/release/jenslys/nrkdl.svg" alt="Releases"></a>

Download shows and movies from tv.nrk.no

**Disclaimer:** This is for educational purposes ONLY. Use at your own risk.

## Installation

```bash
pip install nrkdl
```

#### System requirements

- python3
- ffmpeg

## Options

```
  -h, --help           Show this help message and exit

  --url URL            URL for the Movie/TV-show (e.g:
                       https://tv.nrk.no/program/KOID75006720)

  --write-subtitles    Download subtitles

```

### Example usage

#### Download an entire tv-show with subtitles:

```bash
nrkdl --url https://tv.nrk.no/serie/exit --write-subtitles
```

#### Download a single tv-show episode:

```bash
nrkdl --url https://tv.nrk.no/serie/exit/sesong/2/episode/6/
```

#### Download a movie:

```bash
nrkdl --url https://tv.nrk.no/program/MSUI31006017
```
