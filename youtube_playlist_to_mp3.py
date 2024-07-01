import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import Playlist
from moviepy.editor import AudioFileClip
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, ID3NoHeaderError
import os
import re
from concurrent.futures import ThreadPoolExecutor
import threading

# Global variable to manage abort state
abort_flag = False

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_and_convert(video, download_path, progress_var, total_files):
    global abort_flag
    if abort_flag:
        return
    
    sanitized_title = sanitize_filename(video.title)
    sanitized_author = sanitize_filename(video.author)
    mp3_file_path = os.path.join(download_path, f"{sanitized_author} - {sanitized_title}.mp3")

    # Skip if file already exists and is greater than 0 bytes
    if os.path.exists(mp3_file_path) and os.path.getsize(mp3_file_path) > 0:
        return

    video_stream = video.streams.filter(only_audio=True).first()
    video_file_path = video_stream.download(output_path=download_path)
    audio_clip = AudioFileClip(video_file_path)
    audio_clip.write_audiofile(mp3_file_path, codec='mp3')
    audio_clip.close()

    try:
        audio = MP3(mp3_file_path, ID3=ID3)
    except ID3NoHeaderError:
        audio = MP3(mp3_file_path)
        audio.add_tags()

    audio.tags.add(TIT2(encoding=3, text=video.title))
    audio.tags.add(TPE1(encoding=3, text=video.author))
    audio.save()
    os.remove(video_file_path)

    progress_var.set(progress_var.get() + 1)
    progress_bar.update_idletasks()

def download_youtube_playlist(playlist_url, download_path='downloads', max_workers=4, max_files=200):
    global abort_flag
    abort_flag = False
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    playlist = Playlist(playlist_url)
    
    if len(playlist.videos) == 0:
        messagebox.showerror("Error", "No videos found in playlist")
        return
    
    if len(playlist.videos) > max_files:
        videos = playlist.videos[:max_files]
    else:
        videos = playlist.videos
    total_files = len(videos)
    
    progress_var.set(0)
    progress_bar.config(maximum=total_files)
    status_label.config(text="Downloads started!")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_and_convert, video, download_path, progress_var, total_files) for video in videos]

        for future in futures:
            if abort_flag:
                break
            future.result()

def start_download():
    global abort_flag
    abort_flag = False

    playlist_url = url_entry.get()
    download_path = location_entry.get() or os.path.join(os.path.expanduser("~"), "Music")
    max_workers = int(threads_entry.get() or 4)
    max_files = int(files_entry.get() or 200)

    if not playlist_url:
        messagebox.showerror("Error", "Playlist URL is required")
        return

    def run_download():
        try:
            download_youtube_playlist(playlist_url, download_path, max_workers, max_files)
            if not abort_flag:
                messagebox.showinfo("Success", "Download completed successfully")
                status_label.config(text="Download completed successfully")
                start_button.config(state=tk.NORMAL)
        except Exception as e:
            if not abort_flag:
                messagebox.showerror("Error", str(e))
                status_label.config(text="Error: " + str(e))
                start_button.config(state=tk.NORMAL)

    start_button.config(state=tk.DISABLED)
    download_thread = threading.Thread(target=run_download)
    download_thread.start()

def abort_download():
    global abort_flag
    abort_flag = True
    status_label.config(text="Abort operation in progress... no further files will be queued")
    start_button.config(state=tk.NORMAL)

# GUI setup
root = tk.Tk()
root.title("YouTube Playlist Downloader")

tk.Label(root, text="Playlist URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Download Location:").grid(row=1, column=0, padx=10, pady=10)
location_entry = tk.Entry(root, width=50)
location_entry.grid(row=1, column=1, padx=10, pady=10)
location_entry.insert(0, os.path.join(os.path.expanduser("~"), "Music"))

tk.Label(root, text="Number of Threads:").grid(row=2, column=0, padx=10, pady=10)
threads_entry = tk.Entry(root, width=10)
threads_entry.grid(row=2, column=1, padx=10, pady=10)
threads_entry.insert(0, "4")

tk.Label(root, text="Maximum Number of Files:").grid(row=3, column=0, padx=10, pady=10)
files_entry = tk.Entry(root, width=10)
files_entry.grid(row=3, column=1, padx=10, pady=10)
files_entry.insert(0, "200")

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, length=400, variable=progress_var)
progress_bar.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Buttons
start_button = tk.Button(root, text="Start Download", command=start_download)
start_button.grid(row=6, column=0, padx=10, pady=20)
abort_button = tk.Button(root, text="Abort Download", command=abort_download)
abort_button.grid(row=6, column=1, padx=10, pady=20)

root.mainloop()
