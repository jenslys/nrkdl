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
parser.add_argument("--write-subs", action="store_true", help="Download and embed subtitles to file")
parser.add_argument(
    "--keep-subs",
    action="store_true",
    required=False,
    help="Prevent the subtitle files from being deleted after being embeded",
)
parser.add_argument("--audio-only", action="store_true", required=False, help="Only extract audio files")
parser.add_argument("--write-metadata", action="store_true", required=False, help="Write metadata to file")
args = parser.parse_args()


class logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hooks(d):
    if d["status"] == "finished":
        file_tuple = os.path.split(os.path.abspath(d["filename"]))
        print("Done downloading {}".format(file_tuple[1]))

        # ! Regex rename (temp solution)
        # Exit - 1x2 - 2. Horer og hummer på Hankø → Exit - 1x2 - Horer og hummer på Hankø
        pattern = r"[0-9]+[.]+[ ]"
        subst = ""
        result = re.sub(pattern, subst, d["filename"], 0, re.MULTILINE)
        os.rename(d["filename"], result)

    if d["status"] == "downloading":
        print("Downloading:", d["filename"])
        print("Progress:", d["_percent_str"])
        print("ETA:", d["_eta_str"])
        print()


def download():
    try:
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
            "writesubtitles": args.write_subs,
            "subtitleslangs": ["all"],
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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([args.url])
    except Exception as e:
        raise e


def main():
    download()


if __name__ == "__main__":
    main()
