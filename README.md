![image](https://github.com/riazhassan1979/youtube-playlist-to-mp3/assets/30632644/5c9162fd-7899-47e1-bf25-1c5537dc43e6)    

  
# YouTube Playlist To MP3 

About this Python script:  
    - Downloads videos from a YouTube playlist,  
    - Converts them to MP3 format,  
    - Tags them with the title and contributing artist information.  
  
The script uses multi-threading to download and convert multiple videos concurrently.  
  
## Usage:  
  
To start app: 

    ```python ./youtube_playlist_to_mp3.py```  

or run the [executable from dist](dist/youtube_playlist_to_mp3.zip)  
  
## Features  
  
- Downloads audio from YouTube playlist videos  
- Converts audio to MP3 format
- Tags MP3 files with title and contributing artist
- User can configure how many threads to use
- Supports multi-threaded downloading and conversion
- Limits the number of downloads to a specified maximum (default: 200)


## Requirements

- Python 3.x
- pytube
- moviepy
- mutagen

## To build the executable:
Run the command ```pyinstaller --onefile --windowed .\youtube_playlist_to_mp3.py```
