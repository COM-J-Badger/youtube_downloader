# import yt_dlp
# import os
# import subprocess

# def download_audio_and_thumbnail(url, output_path):
#     ydl_opts = {
#         'format': 'bestaudio[ext=m4a]',
#         'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
#         'writethumbnail': True,
#         'quiet': False,
#         'prefer_ffmpeg': True,
#         'updatetime': False,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
    
#     title = info.get('title', 'audio')
#     audio_file = os.path.join(output_path, f"{title}.m4a")
    
#     # The thumbnail is saved in the same folder, typically as .jpg or .webp
#     # Find the thumbnail filename by checking extensions
#     for ext in ['jpg', 'jpeg', 'png', 'webp']:
#         thumbnail_file = os.path.join(output_path, f"{title}.{ext}")
#         if os.path.isfile(thumbnail_file):
#             break
#     else:
#         thumbnail_file = None
    
#     return audio_file, thumbnail_file, title


# def embed_thumbnail_manual(audio_file, thumbnail_file, output_file):
#     if not thumbnail_file:
#         print("No thumbnail found, skipping embedding.")
#         return audio_file  # return original if no thumbnail
    
#     cmd = [
#         'ffmpeg',
#         '-y',  # overwrite output without asking
#         '-i', audio_file,
#         '-i', thumbnail_file,
#         '-map', '0',
#         '-map', '1',
#         '-c', 'copy',
#         '-disposition:v:0', 'attached_pic',
#         output_file
#     ]
    
#     print(f"Embedding thumbnail: running ffmpeg command:\n{' '.join(cmd)}")
#     subprocess.run(cmd, check=True)
#     return output_file

# def download_video(url, output_path):
#     audio_file, webp_thumbnail_file, title = download_audio_and_thumbnail(url, output_path)
    
#     if webp_thumbnail_file and webp_thumbnail_file.lower().endswith('.webp'):
#         print("Converting WebP thumbnail to JPG...")
#         jpeg_thumbnail_file = convert_webp_to_jpg(webp_thumbnail_file)

#     output_file = os.path.join(output_path, title)
    
#     final_file = embed_thumbnail_manual(audio_file, jpeg_thumbnail_file, output_file)
    
#     print(f"Final file with embedded thumbnail: {final_file}")

# from PIL import Image
# import os

# def convert_webp_to_jpg(webp_path):
#     img = Image.open(webp_path)
#     jpg_path = os.path.splitext(webp_path)[0] + ".jpg"
#     img.convert('RGB').save(jpg_path, "JPEG")
#     return jpg_path

import yt_dlp
import os
import subprocess
from PIL import Image

def download_audio_and_thumbnail(url, output_path):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'writethumbnail': True,
        'postprocessors': [],
        'quiet': False,
        'prefer_ffmpeg': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    
    title = info.get('title', 'audio')
    audio_file = os.path.join(output_path, f"{title}.m4a")

    # Find thumbnail (jpg, png, or webp)
    thumbnail_file = None
    for ext in ['jpg', 'jpeg', 'png', 'webp']:
        candidate = os.path.join(output_path, f"{title}.{ext}")
        if os.path.isfile(candidate):
            thumbnail_file = candidate
            break

    return audio_file, thumbnail_file

def convert_webp_to_jpg(webp_path):
    img = Image.open(webp_path)
    jpg_path = os.path.splitext(webp_path)[0] + ".jpg"
    img.convert('RGB').save(jpg_path, "JPEG")
    return jpg_path

def embed_thumbnail_overwrite(audio_file, thumbnail_file):
    if not thumbnail_file:
        print("No thumbnail found; skipping embedding.")
        return audio_file

    # Convert thumbnail if it's a webp
    if thumbnail_file.lower().endswith('.webp'):
        print("Converting .webp to .jpg...")
        thumbnail_file = convert_webp_to_jpg(thumbnail_file)

    temp_output = audio_file.replace('.m4a', '_with_thumb.m4a')

    # Embed thumbnail with ffmpeg
    cmd = [
        'ffmpeg',
        '-y',
        '-i', audio_file,
        '-i', thumbnail_file,
        '-map', '0',
        '-map', '1',
        '-c', 'copy',
        '-disposition:v:0', 'attached_pic',
        temp_output
    ]

    subprocess.run(cmd, check=True)

    # Overwrite original audio
    os.replace(temp_output, audio_file)

    # Delete all thumbnail files
    for ext in ['jpg', 'jpeg', 'png', 'webp']:
        thumb_path = os.path.splitext(audio_file)[0] + f'.{ext}'
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    print(f"Embedded thumbnail and cleaned up. Final file: {audio_file}")
    return audio_file

def download_video(url, output_path):
    audio_file, thumbnail_file = download_audio_and_thumbnail(url, output_path)
    final_file = embed_thumbnail_overwrite(audio_file, thumbnail_file)
    return final_file
