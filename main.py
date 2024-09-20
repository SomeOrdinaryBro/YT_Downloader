import tkinter
import customtkinter
from yt_dlp import YoutubeDL

# Progress callback (adjusted for yt-dlp)
def on_progress(d):
    """Callback function to display download progress."""
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        print(f"Downloaded: {percentage}")

def Download():
    """Handles the download process for the YouTube video."""
    try:
        # Get the YouTube link from the input field
        yt_link = link.get()

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

        # Extracting video info before downloading
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_link, download=False)  # Don't download yet
            ytObject = info_dict  # Use the info for title access

            # Update title label with video title
            title.configure(text=ytObject['title'])  

            # Now download the video
            ydl.download([yt_link])

        finishLabel.configure(text="Download Complete!", text_color="green")

    except Exception as e:
        finishLabel.configure(text=f"Error occurred: {e}", text_color="red")

# Setup for the GUI using customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Disable maximize by making the window non-resizable
app.resizable(False, False)

# Label for instruction
title = customtkinter.CTkLabel(app, 
                               text="Please insert the YouTube video link below:",
                               font=("Arial", 16))
title.pack(padx=10, pady=10)

# Entry field for URL input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(padx=10, pady=10)

# Label to display finish messages
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Button to initiate the download
download_button = customtkinter.CTkButton(app, text="Download", command=Download)
download_button.pack(padx=10, pady=20)

# Run the app loop
app.mainloop()
