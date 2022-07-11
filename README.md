# YouTube Backloader

Backloader is a project for automatically downloading videos from YouTube in the background. It is available as a bare python script. A containerized version for use with Jellyfin is in active development.

A macOS app is in early stages of development and might be cancelled in favour of better integration with Jellyfin.

## Requirements

* Python 3.10+
* Linux or macOS (Feel free to containerize this script using the Ubuntu template and run it on any platform)
* Internet connection
* Decently powerful hardware (All resolutions other than 720p <span dir="">require merging video and audio on your computer</span>)

## Setup

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



