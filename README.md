
Backloader is a web app to download videos from YouTube. Supports SponsorBlock. UI inspired my macOS.

**This is still in active development. Please use one of the releases for a stable experience. The relevant readme will be included with the download.**

[[_TOC_]]

## Run inside of a docker container (recommended)

1. **Build a docker image.** Copy the path to the folder where the script is. (Assuming you have Docker installed) Run this command in the terminal: `docker build -t backloader3 PATH_TO_DIR_WITH_THE_DOCKERFILE` 
2. **Run the docker image.** Copy the path to the folder where you want to save videos (Jellyfin media folder). Backloader will create subfolders for each playlist (each library). Run this command in the terminal: `docker run --name backloader -v PATH_TO_YOUR_DOWNLOAD_DIR:/app/backloader/host -p 8097:80 backloader3`. Here is the command I use on my mac (zsh) `docker run --name backloader -v "/Volumes/HDD/Jellyfin media":/app/backloader/host -p 8097:80 backloader3`.

The interface will be available on `localhost:8097`. It is very basic, but *just barely* enough to set up basic playlist auto download.


## How to use
 - Create an outlet (In the path field put `host/` to access the directory you specified in the run command)
 - Create a flow (Only the Playlist type is implemented. Feel free to use the built in template for Jellyfin.)


I recommend using [this Jellyfin plugin](https://github.com/ankenyr/jellyfin-youtube-metadata-plugin) for downloading video and channel metadata alongside backloader. Follow the guide provided by its author, the Jellyfin template will work with it.


## vp9 and av01 support on Apple devices

### macOS

In Safari preferences, enable the Developer tab in the top bar, then go to Developer → Experimental functions and enable av01 and vp9 codecs as needed.

### iOS and iPadOS

I haven't been able to enable these codecs in Safari. To avoid live transcoding, play vp9 and av01 content using Swiftfin or Infuse (Available on the App Store).
