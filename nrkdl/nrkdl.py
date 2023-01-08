from __future__ import unicode_literals
import itertools
import os
import yt_dlp
from yt_dlp.postprocessor import MetadataParserPP
import argparse
import requests

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--search",
    type=str,
    help="Search for Movie/TV-show, and then download (e.g: Exit)",
)
group.add_argument(
    "--url",
    type=str,
    help="URL for the Movie/TV-show (e.g: https://tv.nrk.no/program/KOID75006720) ",
)
parser.add_argument(
    "--season",
    type=int,
    help="Season number (e.g: 1) (Only works if --search is used)",
)
parser.add_argument(
    "--episode",
    type=int,
    help="Episode number (e.g: 1) (Only works if --search is used)",
)
parser.add_argument(
    "--write-subs", action="store_true", help="Download and embed subtitles to file"
)
parser.add_argument(
    "--keep-subs",
    action="store_true",
    required=False,
    help="Prevent the subtitle files from being deleted after being embeded",
)
parser.add_argument(
    "--audio-only", action="store_true", required=False, help="Only extract audio files"
)
parser.add_argument(
    "--write-metadata",
    action="store_true",
    required=False,
    help="Write metadata to file",
)
args = parser.parse_args()


class logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hooks(d):
    terminal_width = os.get_terminal_size().columns

    if d["status"] == "finished":
        file_tuple = os.path.split(os.path.abspath(d["filename"]))
        print(" " * terminal_width, end="\r")
        print("Done downloading {}".format(file_tuple[1]))

    if d["status"] == "downloading":
        downloading_text = f"Downloading... {d['_percent_str']} "
        eta_text = f" ETA: {d['_eta_str']}"
        max_width_progress_bar = min(100, terminal_width - len(downloading_text) - len(eta_text))

        progress_width = float(d["_percent_str"][:-1]) * max_width_progress_bar / 100

        progress_done = "█" * round(progress_width)
        progress_remaining = " " * round(max_width_progress_bar - progress_width)

        print(
            f"{downloading_text}{progress_done}{progress_remaining}{eta_text}",
            end="\r",
        )


def ranges(values):
    values = [v for v in values if v is not None]  # ? None == unavailable season/episode
    for _, group in itertools.groupby(enumerate(values), lambda pair: pair[0] - pair[1]):
        group = list(group)
        yield group[0][1], group[-1][1]


def stringify_ranges(r):
    s = []
    for c in r:
        if c[0] == c[1]:
            s.append(str(c[0]))
        else:
            s.append(f"{c[0]}-{c[1]}")
    return ", ".join(s)


def find_seasons(series_id):
    url = f"https://psapi.nrk.no/tv/catalog/series/{series_id}"
    req = requests.get(url)
    if req.status_code != 200:
        print(req)
        return
    data = req.json()
    if data["seriesType"] != "sequential":  # ? Not a TV-show
        return ""
    seasons_dict = data["_embedded"]["seasons"]
    seasons = [
        seasons_dict[i]["sequenceNumber"]
        if seasons_dict[i]["hasAvailableEpisodes"]
        else None  # ? Exists, but unavailable
        for i in range(len(seasons_dict))
    ]
    return seasons


def find_episodes(series_id, season_index):
    url = f"https://psapi.nrk.no/tv/catalog/series/{series_id}"
    req = requests.get(url)
    if req.status_code != 200:
        print(req)
        return
    data = req.json()
    episodes_dict = data["_embedded"]["seasons"][season_index]["_embedded"]["episodes"]

    episodes = [
        episodes_dict[i]["sequenceNumber"]
        if episodes_dict[i]["availability"]["status"] == "available"
        else None  # ? Exists, but unavailable
        for i in range(len(episodes_dict))
    ]
    return episodes


def search(args):
    req = requests.get(f"https://psapi.nrk.no/autocomplete?q={args.search}")
    if req.status_code != 200:
        print(req)
        return

    data = req.json()
    results = data["result"]

    options_count = min(len(results), 5)
    terminal_width = os.get_terminal_size().columns
    series = None
    for i in range(len(results)):
        if results[i]["_source"]["id"] == args.search.lower().replace(
            " ", "-"
        ):  # ? If the search result is an exact match
            series = i + 1
            break

    if series is None:
        for i in range(options_count):
            info = f"{i+1}: {results[i]['_type']} - {results[i]['_source']['title']} - "
            print(
                f"{info}{results[i]['_source']['description'][:terminal_width - len(info) - 2]}.."
            )
        series = input(f"Choose 1-{options_count}: ")
        if series not in (chr(i) for i in range(ord("1"), ord(str(options_count)) + 1)):
            return

    source_dict = results[int(series) - 1]["_source"]
    series_id = source_dict["id"]
    url = "https://tv.nrk.no/" + source_dict["url"]

    season = args.season
    if season == 0:  # ? Download all seasons
        return url

    seasons = find_seasons(series_id)
    if not season:
        if len(seasons) == 1:
            season = seasons[0]
        else:
            season_ranges = stringify_ranges(ranges(seasons))
            season = input(f"Choose season {season_ranges} (a: all): ")
            if season == "a":
                return url
            if not season.isdigit():
                return
    url += f"/sesong/{season}"

    if (
        requests.get(url, allow_redirects=False).status_code != 200
    ):  # TODO check for season count in another way
        raise NotImplementedError("Invalid season number.")

    episode = args.episode
    if episode == 0:  # ? Download all episodes in season
        return url
    if not episode:
        season_index = seasons.index(int(season))

        episodes = find_episodes(series_id, season_index)
        if len(episodes) == 1:
            episode = episodes[0]
        else:
            episodes_ranges = stringify_ranges(ranges(episodes))
            episode = input(f"Choose episode {episodes_ranges} (a: all): ")
            if episode == "a":
                return url
            if not episode.isdigit():
                return
    url += f"/episode/{episode}"

    if (
        requests.get(url, allow_redirects=False).status_code != 200
    ):  # TODO check for episode count in another way
        raise NotImplementedError("Invalid episode number.")

    return url


def main():
    try:
        video_title = "%(series)s"  # Title of show/movie
        movie = "%(title)s.%(ext)s"  # Moviename.mp4
        tvshow = "%(series)s - %(season_number)sx%(episode_number)s - %(episode)s.%(ext)s"
        current_season = "Season %(season_number)s"
        download_path = os.getcwd()  # ? Gets the current working dir
        folder_name = download_path + "/" + video_title

        if args.search:
            args.url = search(args)
            if not args.url:
                print("Quiting...")
                return

        if "/serie/" in args.url:  # ? Identify if its a tvshow or movie
            filename = current_season + "/" + tvshow
        else:
            filename = movie
        ydl_opts = {
            "writesubtitles": args.write_subs,
            "subtitleslangs": ["all"],
            "verbose": False,
            "outtmpl": folder_name + "/" + filename,
            "quiet": True,
            "skip_download": False,
            "no_warnings": True,
            "progress_hooks": [progress_hooks],
            "logger": logger(),
            "postprocessors": [],
        }

        if args.write_subs:
            ydl_opts["postprocessors"].append(
                {
                    "key": "FFmpegSubtitlesConvertor",
                    "format": "srt",
                },
            )
            ydl_opts["postprocessors"].append(
                {
                    "key": "FFmpegEmbedSubtitle",
                    "already_have_subtitle": args.keep_subs,
                },
            )

        if args.write_metadata:
            ydl_opts["postprocessors"].append(
                {
                    "key": "FFmpegMetadata",
                    "add_metadata": True,
                },
            )

        if args.audio_only:
            ydl_opts["postprocessors"].append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                },
            )

        if "/serie/" in args.url:
            ydl_opts["postprocessors"].append(
                {
                    "key": "MetadataParser",
                    "when": "pre_process",
                    "actions": [(MetadataParserPP.Actions.REPLACE, "episode", r"\d+\.+\s", "")],
                },
            )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.url])
    except (KeyboardInterrupt, EOFError):
        print("\nDownload canceled by user...")
    except NotImplementedError as e:
        print(e)
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()
