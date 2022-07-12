# YouTube Backloader

Backloader is a project for automatically downloading videos from YouTube in the background. You can monitor multiple playlists at the same time. It supports any quality, HDR, audio-only downloads and slow 144p downloads.


## Run inside of a docker container (recommended)

1. **Download** the latest release. 
2. **Create a playlist** on YouTube and set it to be public or accessible by link. You can add some videos to it now.
3. Open **config.json** file and fill out the template. You can copy and paste as many as you want, all of your playlists will be monitored in parallel. Here is a description of all variables:
    | value | default | description |
    | ------ | ------ | ------ |
    | base_directory | /media | A directory where the videos will be saved. **Do not change the default value** if you plan to run the script inside a container. |
    | interval | 3600 | Interval between checks in seconds. 1 hour = 3600 seconds. |
    | limit | 0 | Limit tho the total number of checks for this playlist. 0 = unlimited. |
    | resolution | 720 | Select quality of the downloaded videos. Any resolution other than 720 and AUDIO require merging audio and video streams on your computer. Read select a resolution for more info. |
    | url | https://www.youtube.com/watch?v=dQw4w9WgXcQ | Link to your playlist. Use YouTube's share button to avoid any confusion. |
4. Save and close the file
5. Build a docker image. Copy the path to the folder where the script is. (Asumming you have Docker installed) Run this command in the terminal: `docker build -t backloader YOUR_PATH_HERE` 
6. Run the docker image. Copy the path to the folder where you want to save videos (Jellyfin media folder). Backloader will create subfolders for each playlist (each library). Run this command in the terminal: `docker run -v YOUR_PATH_HERE:/media backloader`

To stop the container, run this command `docker ps`, copy the name of the container tagged "backloader" and then run this command `docker kill NAME_HERE`.


## Run as a bare script (only on macOS and Linux)

1. **Download** the script. 
2. Install or **update python**. Follow the guide on [python.org](http://python.org).
3. **Install dependencies** `pip install yt_dlp`. Also, make sure that ffmpeg is installed on your computer.
4. **Create a playlist** on YouTube and set it to be public or accessible by link. You can add some videos to it now.
5. Open the script in any editor and **configure the values** on the last few lines. You need to set a path to the **folder** where the videos will be saved (`workingDirectory= "/Volumes/HDD/Jellyfin/media"`). Backloader will automatically create a new folder for every playlist. Set a link to the **playlist** that you want to monitor (`playlistUrl= "Your link"`). You might want to change the **resolution** in which the videos will be downloaded (`resolution= "1080"`) and set the script to **run forever** (`limit= 0`). Everything else will work fine with the default values (by default, the playlist is checked for new videos every 30 minutes). 
6. **Run** the script `python path/to/backloader.py`.

For example, here is my personal configuration:
```
    createFlow(workingDirectory= "/Volumes/HDD/Jellyfin media", interval= 1800, limit= 0, resolution= "1080", playlistUrl= "https://youtube.com/playlist?list=PL-redacted") # Main video playlist
    createFlow(workingDirectory= "/Volumes/HDD/Jellyfin media", interval= 3600, limit= 0, resolution= "720", playlistUrl= "https://youtube.com/playlist?list=PL-redacted") # Secondary video playlist
    createFlow(workingDirectory= "/Volumes/HDD/Jellyfin media", interval= 3600, limit= 0, resolution= "AUDIO", playlistUrl= "https://youtube.com/playlist?list=PL-redacted") # Music
```

Backloader runs flows as separate processes in parallel, so you can create as many as you want.


## For Jellyfin users


Backloader 1.2 and later were designed to work with Jellyfin. 
The script automatically organizes downloaded data for the Movies library type in an automatically created folder. 
Just run the script, create a new library and point Jellyfin to the new folder (example: /your/path/media/Playlist_0). All you need to do when creating a library is turn off all the default metadata providers and image fetchers. When you manually trigger a deep library scan, do not check the “replace all images” box.

I recommend using [this plugin](https://github.com/ankenyr/jellyfin-youtube-metadata-plugin) for downloading video and channel metadata alongside backloader. Follow the guide provided by its author, backloader does not require any additional setup.

If you select AUDIO, backloader will create folders for each artist (channel) and put .m4a files there. You will need to sort these by albums yourself. Here are some useful links: [app to automate adding metadata to files](https://picard.musicbrainz.org), [how to organize your files for Jellyfin](https://jellyfin.org/docs/general/server/media/music.html).



