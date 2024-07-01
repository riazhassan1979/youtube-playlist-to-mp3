from pytube import Playlist
from moviepy.editor import AudioFileClip
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, ID3NoHeaderError
import os

def download_youtube_playlist(playlist_url, download_path='downloads'):
    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Get playlist
    playlist = Playlist(playlist_url)

    for video in playlist.videos:
        # Download video
        video_stream = video.streams.filter(only_audio=True).first()
        video_file_path = video_stream.download(output_path=download_path)

        # Convert to MP3
        mp3_file_path = os.path.join(download_path, f"{video.author} - {video.title}.mp3")
        audio_clip = AudioFileClip(video_file_path)
        audio_clip.write_audiofile(mp3_file_path, codec='mp3')

        # Close the audio clip
        audio_clip.close()

        # Set MP3 title tag
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

        print(f"Downloaded, converted, and tagged: {video.title}")

# Example usage
playlist_url = 'https://www.youtube.com/watch?v=T6eK-2OQtew&list=PL3-sRm8xAzY-556lOpSGH6wVzyofoGpzU&index=1'
download_youtube_playlist(playlist_url)
