# backend.py

import yt_dlp

def download_video(url, output_path, as_mp3=False, as_mp4=True, progress_hook=None):
    postprocessors = []
    format_selector = 'bestvideo+bestaudio/best'
    merge_format = 'mp4'

    # if as_mp3:
    #     postprocessors = [
    #         {
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         },
    #         {
    #             'key': 'EmbedThumbnail',
    #             'already_have_thumbnail': False,
    #         },
    #         {
    #             'key': 'FFmpegMetadata',
    #         }
    #     ]
    #     format_selector = 'bestaudio/best'
    #     merge_format = None

    if as_mp3:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',  # best audio-only format, usually webm or m4a
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'quiet': True,
            'updatetime': False,
            # no postprocessors, so no conversion to mp3
        }




    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
