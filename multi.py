from pytube import Playlist
from moviepy.editor import AudioFileClip
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, ID3NoHeaderError
import os
import re
from concurrent.futures import ThreadPoolExecutor

def sanitize_filename(filename):
    # Remove or replace characters that are not allowed in filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_and_convert(video, download_path):
    # Download video
    video_stream = video.streams.filter(only_audio=True).first()
    video_file_path = video_stream.download(output_path=download_path)

    # Sanitize the video title and author for the filename
    sanitized_title = sanitize_filename(video.title)
    sanitized_author = sanitize_filename(video.author)
    mp3_file_path = os.path.join(download_path, f"{sanitized_author} - {sanitized_title}.mp3")

    # Skip if file already exists and is greater than 0 bytes
    if os.path.exists(mp3_file_path) and os.path.getsize(mp3_file_path) > 0:
        return
    
    # Convert to MP3
    audio_clip = AudioFileClip(video_file_path)
    audio_clip.write_audiofile(mp3_file_path, codec='mp3')

    # Close the audio clip
    audio_clip.close()

    # Set MP3 title and contributing artist tags
    try:
        audio = MP3(mp3_file_path, ID3=ID3)
    except ID3NoHeaderError:
        audio = MP3(mp3_file_path)
        audio.add_tags()

    audio.tags.add(
        TIT2(
            encoding=3,  # UTF-8 encoding
            text=video.title,
        )
    )
    audio.tags.add(
        TPE1(
            encoding=3,  # UTF-8 encoding
            text=video.author
        )
    )        
    audio.save()

    # Optionally, remove the original video file
    os.remove(video_file_path)
    
def download_youtube_playlist(playlist_url, download_path='downloads', max_workers=20, max_files=200):
    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Get playlist
    playlist = Playlist(playlist_url)

    # Limit to the first `max_files` videos
    videos = playlist.videos[:max_files]

    # Use ThreadPoolExecutor to download and process videos concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_and_convert, video, download_path) for video in videos]

        # Ensure all futures are completed
        for future in futures:
            future.result()

# Example usage
playlist_url = 'https://www.youtube.com/watch?v=T6eK-2OQtew&list=PL3-sRm8xAzY-556lOpSGH6wVzyofoGpzU&index=1'
download_youtube_playlist(playlist_url)
