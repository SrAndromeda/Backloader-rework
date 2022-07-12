
Backloader is a project for automatically downloading videos from YouTube in the background. You can monitor multiple playlists at the same time. It supports any quality, HDR, audio-only downloads and slow 144p downloads. Designed for Jellyfin.

[[_TOC_]]

## Run inside of a docker container (recommended)

1. **Download** the latest release. 
2. **Create a playlist** on YouTube and set it to be public or accessible by link. You can add some videos to it now.
3. Open **config.json** file and fill out the template. You can copy and paste as many as you want, all of your playlists will be monitored in parallel. Here is a description of all variables:
    | value | default | description |
    | ------ | ------ | ------ |
    | base_directory | /media | A directory where the videos will be saved. **Do not change the default value** if you plan to run the script inside a container. |
    | interval | 3600 | Interval between checks in seconds. 1 hour = 3600 seconds. |
    | limit | 0 | Limit the total number of checks for this playlist. 0 = unlimited. |
    | resolution | 720 | Select quality of the downloaded videos. Any resolution other than 720 and AUDIO require merging audio and video streams on your computer. Read "select a resolution" for more info. |
    | url | https://www.youtube.com/watch?v=dQw4w9WgXcQ | Link to your playlist. Use YouTube's share button to avoid any confusion. |
4. Save and close the file
5. **Build a docker image.** Copy the path to the folder where the script is. (Assuming you have Docker installed) Run this command in the terminal: `docker build -t backloader YOUR_PATH_HERE` 
6. **Run the docker image.** Copy the path to the folder where you want to save videos (Jellyfin media folder). Backloader will create subfolders for each playlist (each library). Run this command in the terminal: `docker run -v YOUR_PATH_HERE:/media backloader`

To stop the container, run this command `docker ps`, copy the name of the container tagged "backloader" and then run this command `docker kill NAME_HERE`.

Here is a [video tutorial](https://youtu.be/dHGdwpchwL8) if you need more help.




<details><summary>You can also run Backloader as a bare script (only on macOS and Linux)</summary>

1. **Download** the script. 
2. Install or **update python**. Follow the guide on [python.org](http://python.org).
3. **Install dependencies** `pip install yt_dlp pillow`.
4. **Create a playlist** on YouTube and set it to be public or accessible by link. You can add some videos to it now.
5. Follow steps 3 and 4 from the list above.
6. **Run** the script `python path/to/backloader.py`.

Note that backloader will create some files at this location "/", so you might want to run it inside of a virtual environment.

</details>

## Select a resolution

Here is what you can put in the "resolution" value:
- Any valid resolution without the "p" (**144, 240, 360, 480, 720, 1080, 1440, 2140 and so on**). Keep in mind that YouTube limits bandwidth for small resolutions, so you will not be able to download a small file instantly. Videos in 720p are download as a complete file. Videos in a higher resolution require separate downloads for video and audio. These files are then merged on your computer.
- **BEST** Backloader will download the best available resolution.
- **WORST** Backloader will download the worst available resolution. Keep in mind the slow download speed.
- **AUDIO** Backloader will download only the audio stream. It will create folders for each artist (channel) and put .m4a files there. You will need to sort these by albums yourself. Here are some useful links: [Picard - an app to automate adding metadata to files](https://picard.musicbrainz.org), [how to organize your music for Jellyfin](https://jellyfin.org/docs/general/server/media/music.html).

All downloads are optimized for Jellyfin. Videos are encoded using H264, audio is in AAC. All of this is contained in mp4. Thumbnails are converted to jpg.




## For Jellyfin users


Backloader 1.2 and later were designed to work with Jellyfin. 
The script automatically organizes downloaded data for the Movies library type in an automatically created folder. 
Just run the script, create a new library and point Jellyfin to the new folder (example: /your/path/media/Playlist_0). All you need to do when creating a library is turn off all the default metadata providers and image fetchers. When you manually trigger a deep library scan, do not check the “replace all images” box.

I recommend using [this plugin](https://github.com/ankenyr/jellyfin-youtube-metadata-plugin) for downloading video and channel metadata alongside backloader. Follow the guide provided by its author, backloader does not require any additional setup.




