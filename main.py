import tkinter  # Imports the tkinter library for creating the GUI.
import customtkinter  # Imports customtkinter, a custom extension of tkinter with enhanced UI components.
from yt_dlp import YoutubeDL  # Imports the YoutubeDL class for downloading videos from YouTube.
from yt_dlp.utils import DownloadError  # Imports DownloadError to handle download-related errors.
import re  # Imports the regex library for regular expression operations.

# Function to update the progress bar and percentage label
def update_progress(percentage):
    """Update the progress bar and percentage label."""
    progressBar.set(percentage / 100)  # Sets the progress bar to the percentage value (scaled to 0-1).
    pPercentage.configure(text=f"{percentage}%")  # Updates the percentage label with the current progress.

def on_progress(d):
    """Callback function to display download progress."""
    if d['status'] == 'downloading':  # Checks if the current status is 'downloading'.
        percentage_str = d.get('_percent_str', '')  # Retrieves the percentage string if available.
        if percentage_str:
            # Use regex to extract numeric part
            match = re.search(r'(\d+(\.\d+)?)%', percentage_str)  # Searches for a numeric percentage in the string.
            if match:
                percentage = match.group(1)  # Extracts the numeric part of the percentage.
                try:
                    percent_value = float(percentage)  # Converts the percentage string to a float.
                    # Update the progress bar and percentage label on the main thread
                    app.after(0, update_progress, percent_value)  # Schedules the update on the main thread.
                except ValueError:
                    print(f"Error converting percentage: {percentage_str}")  # Prints an error if conversion fails.
            else:
                print(f"Could not extract percentage from: {percentage_str}")  # Prints an error if regex fails.

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL."""
    youtube_regex = re.compile(  # Compiles a regex pattern for matching YouTube URLs.
        r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}', re.IGNORECASE)
    return re.match(youtube_regex, url) is not None  # Returns True if the URL matches the pattern, False otherwise.

def normalize_youtube_url(url):
    """Normalize different YouTube URL formats to a standard format."""
    if 'youtu.be/' in url:  # Checks if the URL is in the shortened format.
        video_id = url.split('youtu.be/')[1].split('?')[0]  # Extracts the video ID from the shortened URL.
        return f'https://www.youtube.com/watch?v={video_id}'  # Returns the normalized URL in standard format.
    elif 'youtube.com/watch?v=' in url:  # Checks if the URL is in the standard format.
        return url.split('&')[0]  # Returns the URL without any additional query parameters.
    return url  # Returns the original URL if no conditions matched.

def Download():
    """Handles the download process for the YouTube video."""
    try:
        # Get the YouTube link from the input field
        yt_link = link.get().strip()  # Retrieves and trims the user-input URL.

        # Validate the URL
        if not is_valid_youtube_url(yt_link):  # Checks if the URL is valid.
            finishLabel.configure(text="Invalid YouTube URL.", text_color="red")  # Displays an error message.
            return  # Exits the function if the URL is invalid.

        # Normalize the URL
        yt_link = normalize_youtube_url(yt_link)  # Converts the URL to a standard format.

        # Ensure the URL is using HTTPS
        if yt_link.startswith('http://'):  # Checks if the URL starts with HTTP.
            yt_link = yt_link.replace('http://', 'https://')  # Converts it to HTTPS.

        # yt-dlp options
        ydl_opts = {  # Sets options for yt-dlp
            'format': 'best',  # Specifies to download the best quality available.
            'outtmpl': '%(title)s.%(ext)s',  # Saves the file with the video title as the filename.
            'progress_hooks': [on_progress],  # Attaches the progress callback function.
        }

        finishLabel.configure(text="")  # Clears any previous messages.
        progressBar.set(0)  # Resets the progress bar to 0.
        pPercentage.configure(text="0%")  # Resets the percentage label to 0%.

        # Extracting video info before downloading
        with YoutubeDL(ydl_opts) as ydl:  # Creates an instance of YoutubeDL with specified options.
            info_dict = ydl.extract_info(yt_link, download=False)  # Extracts video information without downloading.
            ytObject = info_dict  # Stores the extracted information for later use.

            # Update title label with video title
            title.configure(text=ytObject['title'], text_color="white")  # Updates the title label with the video title.

            # Now download the video
            ydl.download([yt_link])  # Initiates the download of the video.

        finishLabel.configure(text="Download Complete!", text_color="green")  # Displays a success message.

    except DownloadError:
        finishLabel.configure(text="Error: Could not retrieve video information.", text_color="red")  # Displays error for download issues.
    except Exception as e:
        finishLabel.configure(text=f"Error occurred: {e}", text_color="red")  # Displays any other errors that may occur.

"""
GUI CONFIG IS BELOW THIS LINE, CUSTOMIZE THE FEEL OF THE APP BELOW
"""

# Setup for the GUI using customtkinter
customtkinter.set_appearance_mode("dark")  # Sets the overall theme of the application to dark mode for better visibility in low light.
customtkinter.set_default_color_theme("blue")  # Sets the default color theme to blue, giving the UI a consistent look.

# Initialize the main application window
app = customtkinter.CTk()  # Creates an instance of the CTk class, which serves as the main application window.
app.geometry("720x480")  # Sets the window size to 720 pixels wide by 480 pixels high.
app.title("YouTube Downloader")  # Sets the title of the window to "YouTube Downloader".

# Disable maximize by making the window non-resizable
app.resizable(False, False)  # Prevents the user from resizing the window, keeping the layout consistent.

# Title label
title = customtkinter.CTkLabel(app, 
                               text="YouTube Downloader",  # The text displayed in the label.
                               font=("Helvetica", 20, "bold"),  # Sets the font to Helvetica, size 20, and bold.
                               text_color="#00BFFF")  # Sets the text color to a bright blue.
title.pack(pady=(20, 10))  # Adds the title label to the window and applies vertical padding.

# Instruction label
instructionLabel = customtkinter.CTkLabel(app, 
                                           text="Please insert the YouTube video link below:",  # Provides user instructions.
                                           font=("Helvetica", 14),  # Sets the font to Helvetica, size 14.
                                           text_color="#FFFFFF")  # Sets the text color to white.
instructionLabel.pack(pady=(0, 10))  # Adds the instruction label to the window with some padding.

# Entry field for URL input
url_var = tkinter.StringVar()  # Creates a StringVar to hold the user input for the YouTube URL.
link = customtkinter.CTkEntry(app, 
                               width=350,  # Sets the width of the entry field to 350 pixels.
                               height=40,  # Sets the height of the entry field to 40 pixels.
                               textvariable=url_var,  # Binds the entry field to the url_var variable.
                               placeholder_text="Enter YouTube URL",  # Placeholder text to guide user input.
                               fg_color="#333333",  # Sets the background color of the entry field to dark gray.
                               text_color="white",  # Sets the text color to white for readability.
                               border_color="#00BFFF")  # Sets the border color to bright blue.
link.pack(pady=(0, 20))  # Adds the entry field to the window with some vertical padding.

# Label to display finish messages
finishLabel = customtkinter.CTkLabel(app, text="", font=("Helvetica", 12))  # Initializes a label for messages, starting empty.
finishLabel.pack()  # Adds the finish label to the window.

# Percentage label for download progress
pPercentage = customtkinter.CTkLabel(app, text="0%", font=("Helvetica", 12))  # Initializes a label to display the download percentage, starting at 0%.
pPercentage.pack(pady=(10, 0))  # Adds the percentage label to the window with some vertical padding.

# Progress bar for download status
progressBar = customtkinter.CTkProgressBar(app, width=400, progress_color="#00BFFF")  # Creates a progress bar with a width of 400 pixels and a bright blue color.
progressBar.set(0)  # Sets the initial progress of the bar to 0.
progressBar.pack(pady=(0, 20))  # Adds the progress bar to the window with some vertical padding.

# Button to initiate the download
download_button = customtkinter.CTkButton(app, 
                                           text="Download",  # Text displayed on the button.
                                           command=Download,  # Specifies the function to call when the button is clicked.
                                           fg_color="#00BFFF",  # Sets the button background color to bright blue.
                                           hover_color="#0080FF")  # Sets the button color to a lighter blue when hovered over.
download_button.pack(pady=20)  # Adds the button to the window with some vertical padding.

# Run the app loop
app.mainloop()  # Starts the application, allowing it to listen for user interactions.
