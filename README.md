# YouTube Video Downloader

This YouTube Downloader application allows you to easily download videos from YouTube. Built using Python with a graphical user interface (GUI), the app simplifies the download process—just enter the YouTube video link, and the app handles the rest.

![YouTube Downloader GUI](screenshots/Screengrap_v1.1.PNG)
<p align="center">
*UI may look outdated because I was using a virtual machine (VM) during the demonstration*
</p>

<br><br>

<p align="center">
  <strong>For the latest updates and improvements, please read the <a href="Updates_and_Improvements.md">Updates and Improvements</a> document.</strong>
</p>

<p align="center">
  <strong>For those who don't have a VSCode setup, check out the guide: <a href="No_VSCode_Setup_No_Worries.md">No VSCode Setup? No Worries!</a></strong>
</p>

<br><br>

## Requirements

- Python 3.7 or higher.
- Libraries: `yt-dlp`, `customtkinter`, etc. (see [Installing Dependencies](#installing-dependencies)).

## Installing Dependencies

1. **Download the Project:**
   - To get started, download the project files by either:
     - Clicking the "Download" button if available.
     - Cloning the repository using Git:
       ```bash
       git clone <repository-url>
       ```
     - Replace `<repository-url>` with the actual URL of the project repository.

2. **Open a Terminal/Command Prompt:**
   - After downloading the project, open a terminal (macOS/Linux) or Command Prompt (Windows).
   - Navigate to the folder where you downloaded the project using the `cd` command:
     ```bash
     cd path/to/your/project-folder
     ```

3. **Install Required Libraries:**
   - Run the following command to install necessary libraries:
     ```bash
     pip install -r requirements.txt
     ```

## How to Run the Application

1. **Open the Project Folder:**
   - Ensure you are still in the project folder in your terminal or Command Prompt.

2. **Run the Application:**
   - Execute the following command to start the YouTube Downloader application:
     ```bash
     python main.py
     ```

3. **Using the Application:**
   - Once the application opens, you will see a GUI with a text box.
   - Paste the YouTube video link you wish to download in the text box. Ensure the link starts with `https://` (e.g., `https://www.youtube.com/watch?v=video_id`).
   - Click the "Download" button.

4. **Check the Download Status:**
   - The application will display download progress in the GUI, indicating how much of the video has been downloaded.
   - A message will appear upon successful completion of the download.

## Exporting Files

- The downloaded video will be saved in the same folder as the application, named according to its title on YouTube with the appropriate file extension (e.g., `.mp4`).

## Troubleshooting

- **If you encounter errors:**
  - **Invalid Video URL:** Ensure the URL is correct and starts with `https://www.youtube.com/`.
  - **DownloadError:** If you receive a `DownloadError`, verify the video is available on YouTube.
  - **Internet Connection Issues:** Check that your internet connection is stable.
  - **Application Crashes:** Take note of any error messages displayed, which can help identify the problem. Refer to the documentation or seek help from the community.

- **Need Further Assistance?** If you're still having issues, please create an issue in the repository, and I'll be happy to help troubleshoot.

## Additional Notes

- This application is intended for educational purposes only. It does not allow the downloading of copyrighted content without proper authorization. Please ensure you have the right to download any video before using this application.
- Use this tool responsibly and adhere to YouTube's Terms of Service. Always respect the rights of content creators.

## License

This project is licensed under the MIT License. Feel free to modify and use it as needed.
