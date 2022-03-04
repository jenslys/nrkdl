from __future__ import unicode_literals
import os
import yt_dlp
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument(
    "--url",
    type=str,
    required=True,
    help="URL for the Movie/TV-show (e.g: https://tv.nrk.no/program/KOID75006720) ",
)
parser.add_argument(
    "--seasons",
    type=int,
    required=False,
    help="If you wish to download mulitple seasons of a show (--seasons x)",
)
parser.add_argument(
    "--location",
    type=str,
    required=False,
    help="Desired download location (Default is the current working directory)",
    default=os.getcwd(),
)
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
        print(d["filename"], d["_percent_str"], d["_eta_str"])


def nrk_tvshow():
    try:
        video_title = fetch_info()
        for x in range(1, args.seasons):
            season_number = "Season " + str(x)
            folder_name = args.location + "/" + video_title + "/" + season_number
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            ydl_opts = {
                "writesubtitles": True,
                "outtmpl": folder_name + "/" + "%(title)s.%(ext)s",
                "quiet": True,
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
                ydl.download([args.url, "/sesong/", x])
    except Exception as e:
        raise e


def fetch_info():
    ydl_opts = {"skip_download": True, "quiet": True, "no_warnings": True}
    print("Fetching metadata...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(args.url)
        video_title = info_dict.get("title", None)
        return video_title


def nrk_movie():
    try:
        video_title = fetch_info()
        folder_name = args.location + "/" + video_title
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        ydl_opts = {
            "writesubtitles": True,
            "outtmpl": folder_name + "/" + "%(title)s.%(ext)s",
            "quiet": True,
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
    if args.seasons:
        nrk_tvshow()
    else:
        nrk_movie()


if __name__ == "__main__":
    main()
