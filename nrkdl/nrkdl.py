from __future__ import unicode_literals
import os
import yt_dlp
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    type=str,
    required=True,
    help="URL for the Movie/TV-show (e.g: https://tv.nrk.no/program/KOID75006720) ",
)
parser.add_argument("--write-subtitles", action="store_true", required=False, help="Download subtitles")
args = parser.parse_args()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        file_tuple = os.path.split(os.path.abspath(d["filename"]))
        print("Done downloading {}".format(file_tuple[1]))
    if d["status"] == "downloading":
        print("Downloading:", d["filename"])
        print("Progress:", d["_percent_str"])
        print("ETA:", d["_eta_str"])
        print()


def download():
    try:
        _pattern = r"[0-9]+[.]+[ ]"
        video_title = "%(series)s"  # Title of show/movie
        movie = "%(title)s.%(ext)s"  # Moviename.mp4
        tvshow = "%(series)s - %(season_number)sx%(episode_number)s - %(episode)s.%(ext)s"  # Exit - 1x2 - Horer og hummer på Hankø
        download_path = os.getcwd()
        folder_name = download_path + "/" + video_title
        if "/serie/" in args.url:  # Identify if its a tvshow or movie
            filename = tvshow
        else:
            filename = movie
        ydl_opts = {
            "writesubtitles": args.write_subtitles,
            "outtmpl": folder_name + "/" + filename,
            "quiet": True,
            "skip_download": False,
            "no_warnings": True,
            "progress_hooks": [my_hook],
            "logger": MyLogger(),
            "postprocessors": [
                {
                    "key": "FFmpegSubtitlesConvertor",
                    "format": "srt",
                }
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.url])
    except Exception as e:
        raise e


def main():
    download()


if __name__ == "__main__":
    main()
