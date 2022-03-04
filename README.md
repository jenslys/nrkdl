# nrkdl

Download shows and movies from tv.nrk.no

**Disclaimer:** This is for educational purposes ONLY. Use at your own risk.

## Installation

```bash
pip install nrkdl
```

## Options

```
  -h, --help           Show this help message and exit

  --url URL            URL for the Movie/TV-show (e.g:
                       https://tv.nrk.no/program/KOID75006720)

  --location LOCATION  Desired download location (Default is the current
                       working directory)

```

### Example usage

#### Download an entire tv-show:

```bash
nrkdl --url https://tv.nrk.no/serie/exit
```

#### Download a single tv-show episode:

```bash
nrkdl --url https://tv.nrk.no/serie/exit/sesong/2/episode/6/avspiller
```

#### Download a movie:

```bash
nrkdl --url https://tv.nrk.no/program/MSUI31006017
```
