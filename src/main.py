import yt_dlp

url = "https://youtu.be/2lAe1cqCOXo?si=_aQhUb8lkYcwGYGr"

options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
}

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download([url])
