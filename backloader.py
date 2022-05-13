"""
    
    YouTube Backloader will download new videos from a selected YouTube playlist.
    Copyright (C) 2022  Pixselious

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
   
"""


showLicenceNotice = True

pathToBaseFolder = "" # Path to the folder where the videos will be saved. If you're using this for Jellyfin, this should be the path to the library folder in your media folder (Example: "/jellyfin/media/youtube"). Set the library type to movies and turn off all default metadata providers and image fetchers.  
# This script will create large temporary files and a log file in the same folder that it is in.
# Make sure the user runnig this script has rights to read and write in this folder.

interval = 43200 # Time interval between checks in seconds (1 hour = 3600 seconds, 1 day = 86400 seconds) Default: 43200 (12 hours)
count = 3 # Total amount of checks you want to run. Default: 3
unlimited = False # If True, ignores count, so the script will run forever. Set count to 3 ar any other number > 1 to be safe. Default: False

resolution = "720" # 720, 1080, 1440, 2160, 4320 or MAX. 720 requires no post-processing, higher resolutions require merging video and audio on your computer. Default: "720"
playlistUrl = "" # Link to the playlist you want to monitor. Make sure that it is set to public or accessible by link. Use YouTube's share button to avoid any problems.
ignoreCurrent = "y" # y : download the videos that are already in the playlist; n : ignore the current videos and only download the ones that are added later. Default: "y"


from time import sleep

from pytube import YouTube, Playlist
from moviepy.editor import *

import os
import shutil
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_stdlib_context


#   GETTING URL OF VIDEOS FROM A PLAYLIST

def getUrls(playlistUrl):

    playlist = Playlist(playlistUrl)
    
    urls = list(playlist.video_urls)
    
    return(urls)

def removeBadChars(string):
    blacklist = ["|", "/", "\\"] # This script is designed to run on UNIX based OS's. If you are using Windows, consider switching to Linux. Or run this script in a Linux container.
    
    for i in blacklist:
        string = string.replace(i, "")
    return string

#   DOWNLOADING VIDEOS

def download(url):
    
    print('Started ' + url)
    
    try:
        yt_obj = YouTube(url)
    
        filters = yt_obj.streams.filter(progressive=True, file_extension = "mp4")
        
        if len(pathToBaseFolder) == 0:
            filters.get_highest_resolution().download(filename = removeBadChars(yt_obj.title) + ".mp4")
        else:
            pathToTargetFolder = pathToBaseFolder + "/" + removeBadChars(yt_obj.title)
            os.mkdir(pathToTargetFolder)
            filters.get_highest_resolution().download(output_path = pathToTargetFolder, filename = removeBadChars(yt_obj.title) + ".mp4")
            urllib.request.urlretrieve(yt_obj.thumbnail_url, pathToTargetFolder + "/poster.jpg")
            
        
        print('Downloaded')
        print("")
        
    except Exception as e:
        print(e)
    
def downloadHiRes(url, resolution):
    
    resolution = resolution + "p"
    
    print('Started ' + url)
    
    try:
        youtube = YouTube(url)
    
        # Getting all available resolutions
    
        video = youtube.streams.filter(only_video = True, file_extension = "mp4")
        print(video)
        
        # Checking if user requested a specific resolution
        if resolution != "MAXp":
            # Checking if the requested resolution is available
            temp = video.filter(res = resolution)
            print(temp)
            
            if len(temp) == 0: 
                # If the video is not available in the requested resolution, get the highest possible.
                print("Requested resolution is not available")
                video.desc()
                print(video.first())
            else:
                video = temp
        
        
        video.first().download(filename = "temp_video_" + url.split("v=")[-1] + ".mp4")
        
        # Downloading the audio
        
        audio = youtube.streams
        audio.get_audio_only().download(filename = "temp_audio_" + url.split("v=")[-1] + ".mp4")
        
        # Merging video and audio together
        
        print('Merging video and audio, this might take a while')
        
        videoClip = VideoFileClip("temp_video_" + url.split("v=")[-1] + ".mp4")
        audioClip = AudioFileClip("temp_audio_" + url.split("v=")[-1] + ".mp4")
        
        completeClip = videoClip.set_audio(audioClip)
        completeClip.write_videofile(filename = "final_" + url.split("v=")[-1] + ".mp4", audio_codec = "aac")
        
        # Removing temporary video and audio files
        
        os.remove("temp_video_" + url.split("v=")[-1] + ".mp4")
        os.remove("temp_audio_" + url.split("v=")[-1] + ".mp4")
        
        # Renaming final file here instead of during creation to not confuse the terminal with emojis or anything like that.
        
        newName = removeBadChars(youtube.title) + ".mp4"
        os.rename("final_" + url.split("v=")[-1] + ".mp4", newName)
        
        pathToTargetFolder = pathToBaseFolder + "/" + removeBadChars(youtube.title)
        
        if len(pathToBaseFolder) != 0:
            shutil.move(newName, pathToTargetFolder)
            urllib.request.urlretrieve(youtube.thumbnail_url, pathToTargetFolder + "/poster.jpg")
            
        
        print('Merged')
        print("")
        
    except Exception as e:
        print(e)
    
    
#   LOGGING DOWNLOADED VIDEOS

# Creates a log file on the first run 
try:
    file = open(pathToBaseFolder + "/downloadedUrls" + '.txt', 'x')
    file.close
except:
    pass

# Used to add urls of newly downloaded videos to a log file
def appendFile(newUrls):
    with open(pathToBaseFolder + "/downloadedUrls" + '.txt', 'a') as file:
        for url in newUrls:
            file.write(url + " ")

# Used to fetch urls of previously downloaded videos to compare with urls from YT playlist
def readFile():
    urls = []
    with open(pathToBaseFolder + "/downloadedUrls" + '.txt', 'r') as file:
        raw = file.read()
    urls = raw.split()
    return(urls)

# Shows new videos in the playlist
def compare(local, online): 
    
    for url in local:
        try:
            online.remove(url)
        except:
            print("Local video no longer exists in the playlist")
    
    difference = online 
    return difference    
    
    
    

#   CHECKING FOR NEW VIDEOS AND DOWNLOADING THEM

def checkPlaylist(playlistUrl):
    local = readFile()
    online = getUrls(playlistUrl)
    newVideos = compare(local, online)
    
    return(newVideos)

def downloadVideos(urls, resolution):
    for url in urls:
        if resolution == "720":
            download(url)
        else:
            downloadHiRes(url, resolution)
        
        
        
#   UI

if showLicenceNotice == True:
    print("""
    YouTube Backloader  Copyright (C) 2022  Pixselious
    This program comes with ABSOLUTELY NO WARRANTY; for details read LICENCE.txt .
    This is free software, and you are welcome to redistribute it
    under certain conditions; Read LICENCE.txt for details.
    
    Thank you to the contributors of pytube and moviepy
    """)

print("")


if ignoreCurrent == ("n" or "N"):
    currentVideos = checkPlaylist(playlistUrl)
    appendFile(currentVideos)

for i in range(count):
    newVideos = checkPlaylist(playlistUrl)
    
    if len(newVideos) == 0:
        print("No new videos")
    else:
        downloadVideos(newVideos, resolution)
        appendFile(newVideos)
    
    print("Waiting " + str(interval) + " seconds")
    sleep(interval)
    
    i += 1
    
print("Reached limit of checks")