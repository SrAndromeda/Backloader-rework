# YouTube Backloader

Backloader is a project for automatically downloading videos from YouTube in the background. It is available as a bare python script. A containerized version for use with Jellyfin is in active development.

A macOS app is in early stages of development and might be cancelled in favour of better integration with Jellyfin.

## Requirements

* Python 3.8+
* Linux or macOS (Feel free to containerize this script using the Ubuntu template and run it on any platform)
* Internet connection
* Decently powerful hardware (All resolutions other than 720p <span dir="">require merging video and audio on your computer</span>)

## Setup

1. **Download** the script. 
2. Install or **update python**. Follow steps on [python.org](http://python.org).
3. **Install dependencies** `python pip install pytube moviepy shutil ssl urllib`.
4. **Create a playlist** on YouTube and set it to be accessible by link or public. You will add the videos that you want to download once the script is running.
5. Open the script in any editor and **configure the values** on the first few lines. You need to set a path to the **folder** where the videos will be saved (`pathToBaseFolder`) and set a link to the **playlist** that you want to monitor (`playlistUrl`). You might want to change the **resolution** in which the videos will be downloaded (`resolution = "720"`) and set the script to **run forever** (`unlimited = True`). Everything else will work fine with the default values (by default, the playlist is checked for new videos every 12 hours). 
6. **Run** the script `python path/to/backloader.py`.

## For Jellyfin users


Backloader 1.2 and later were designed to work with Jellyfin. The script automatically organizes downloaded data for the Movies library type. Just create an empty folder for the new library in your media folder, like you normally would, and give the path to this folder to the script (<span dir="">`pathToBaseFolder = "/jellyfin/media/youtube"`</span>)

All you need to do when creating a library is <span dir="">turn off all the default metadata providers and image fetchers.</span> When you manually trigger a library scan, never check the “replace all images” box.

## Limitations

* YouTube team sometimes change something on their end and break the library used here for downloading videos. Monitor [this](https://github.com/pytube/pytube) GitHub page for changes in the cypher.py file.
* The library used here for merging video and audio does not support HDR videos.
* Since I am the one who wrote this, there are bugs.
