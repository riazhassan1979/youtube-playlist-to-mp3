# YouTube Playlist Downloader and MP3 Converter

About this Python script:
    * Downloads videos from a YouTube playlist, 
    * Converts them to MP3 format, 
    * Tags them with the title and contributing artist information. 

The script uses multi-threading to download and convert multiple videos concurrently.

## Features

- Downloads audio from YouTube playlist videos
- Converts audio to MP3 format
- Tags MP3 files with title and contributing artist
- Supports multi-threaded downloading and conversion
- Limits the number of downloads to a specified maximum (default: 200)

## Requirements

- Python 3.x
- pytube
- moviepy
- mutagen

## Usage: 

To start app: ```python ./youtube_playlist_to_mp3.py```
or run the [executable from dist](dist/youtube_playlist_to_mp3.exe)