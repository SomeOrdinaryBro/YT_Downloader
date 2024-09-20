import tkinter
import customtkinter
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
import re

# Function to update the progress bar and percentage label
def update_progress(percentage):
    """Update the progress bar and percentage label."""
    progressBar.set(percentage / 100)
    pPercentage.configure(text=f"{percentage}%")

def on_progress(d):
    """Callback function to display download progress."""
    if d['status'] == 'downloading':
        percentage_str = d.get('_percent_str', '')
        if percentage_str:
            # Use regex to extract numeric part
            match = re.search(r'(\d+(\.\d+)?)%', percentage_str)
            if match:
                percentage = match.group(1)  # Extract the numeric part of the percentage
                try:
                    percent_value = float(percentage)
                    # Update the progress bar and percentage label on the main thread
                    app.after(0, update_progress, percent_value)
                except ValueError:
                    print(f"Error converting percentage: {percentage_str}")
            else:
                print(f"Could not extract percentage from: {percentage_str}")

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL."""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}', re.IGNORECASE)
    return re.match(youtube_regex, url) is not None

def normalize_youtube_url(url):
    """Normalize different YouTube URL formats to a standard format."""
    if 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1].split('?')[0]
        return f'https://www.youtube.com/watch?v={video_id}'
    elif 'youtube.com/watch?v=' in url:
        return url.split('&')[0]  # Remove any additional parameters
    return url

def Download():
    """Handles the download process for the YouTube video."""
    try:
        # Get the YouTube link from the input field
        yt_link = link.get().strip()

        # Validate the URL
        if not is_valid_youtube_url(yt_link):
            finishLabel.configure(text="Invalid YouTube URL.", text_color="red")
            return

        # Normalize the URL
        yt_link = normalize_youtube_url(yt_link)

        # Ensure the URL is using HTTPS
        if yt_link.startswith('http://'):
            yt_link = yt_link.replace('http://', 'https://')

        # yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Saves file with video title as name
            'progress_hooks': [on_progress],  # Attach progress callback
        }

        finishLabel.configure(text="")  # Clear previous messages
        progressBar.set(0)  # Reset the progress bar
        pPercentage.configure(text="0%")  # Reset the percentage label

        # Extracting video info before downloading
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)  # Don't download yet
            ytObject = info_dict  # Use the info for title access

            # Update title label with video title
            title.configure(text=ytObject['title'], text_color="white")  

            # Now download the video
            ydl.download([yt_link])

        finishLabel.configure(text="Download Complete!", text_color="green")

    except DownloadError:
        finishLabel.configure(text="Error: Could not retrieve video information.", text_color="red")
    except Exception as e:
        finishLabel.configure(text=f"Error occurred: {e}", text_color="red")



"""GUI CODE BELOW"""

# Setup for the GUI using customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Disable maximize by making the window non-resizable
app.resizable(False, False)

# Title label
title = customtkinter.CTkLabel(app, 
                               text="YouTube Downloader",
                               font=("Helvetica", 20, "bold"),
                               text_color="#00BFFF")  # Bright blue
title.pack(pady=(20, 10))

# Instruction label
instructionLabel = customtkinter.CTkLabel(app, 
                                           text="Please insert the YouTube video link below:",
                                           font=("Helvetica", 14),
                                           text_color="#FFFFFF")  # White
instructionLabel.pack(pady=(0, 10))

# Entry field for URL input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, 
                               width=350, 
                               height=40, 
                               textvariable=url_var, 
                               placeholder_text="Enter YouTube URL",
                               fg_color="#333333",  # Dark gray
                               text_color="white",
                               border_color="#00BFFF")  # Bright blue border
link.pack(pady=(0, 20))

# Label to display finish messages
finishLabel = customtkinter.CTkLabel(app, text="", font=("Helvetica", 12))
finishLabel.pack()

# Percentage label
pPercentage = customtkinter.CTkLabel(app, text="0%", font=("Helvetica", 12))
pPercentage.pack(pady=(10, 0))

# Progress bar
progressBar = customtkinter.CTkProgressBar(app, width=400, progress_color="#00BFFF")  # Bright blue progress
progressBar.set(0)
progressBar.pack(pady=(0, 20))

# Button to initiate the download
download_button = customtkinter.CTkButton(app, 
                                           text="Download", 
                                           command=Download, 
                                           fg_color="#00BFFF",  # Bright blue
                                           hover_color="#0080FF")  # Lighter blue on hover
download_button.pack(pady=20)

# Run the app loop
app.mainloop()
