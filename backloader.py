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

pathToTargetFolder = ""


from time import sleep

from pytube import YouTube, Playlist
from moviepy.editor import *

import os
import shutil
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


#   GETTING URL OF VIDEOS FROM A PLAYLIST

def getUrls(playlistUrl):

    playlist = Playlist(playlistUrl)
    
    urls = list(playlist.video_urls)
    
    return(urls)



#   DOWNLOADING VIDEOS

def download(url):
    
    print('Started ' + url)
    
    try:
        yt_obj = YouTube(url)
    
        filters = yt_obj.streams.filter(progressive=True, file_extension = "mp4")
        
        if len(pathToTargetFolder) == 0:
            filters.get_highest_resolution().download()
        else:
            filters.get_highest_resolution().download(output_path = pathToTargetFolder)
        
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
        
        newName = youtube.title + ".mp4"
        os.rename("final_" + url.split("v=")[-1] + ".mp4", newName)
        
        if len(pathToTargetFolder) != 0:
            shutil.move(newName, pathToTargetFolder)
        
        print('Merged')
        print("")
        
    except Exception as e:
        print(e)
    
    
#   LOGGING DOWNLOADED VIDEOS

# Creates a log file on the first run 
try:
    file = open("downloadedUrls" + '.txt', 'x')
    file.close
except:
    pass

# Used to add urls of newly downloaded videos to a log file
def appendFile(newUrls):
    with open("downloadedUrls" + '.txt', 'a') as file:
        for url in newUrls:
            file.write(url + " ")

# Used to fetch urls of previously downloaded videos to compare with urls from YT playlist
def readFile():
    urls = []
    with open("downloadedUrls" + '.txt', 'r') as file:
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

playlistUrl = input("Enter playlist URL: ")
ignoreCurrent = input("Do you want to download videos thet are already in this playlist? (Y/N): ")
print("")
print("Downloading videos in the highest quality requires intense post-processing on your computer. This might cause your computer to heat up and be noisy.")
print("Downloading videos in 720p does not require post-processing and will be much faster. Consider limiting the script to 720p if you are running it on your main machine.")

i = False
while i == False:
    resolution = input("Set a resolution limit for the downloaded videos. (Enter one of the following numbers: 720, 1080, 1440, 2160, 4320 or enter 'MAX' if you do not wish to set a limit): ")
    print("")
    if resolution == "720" or resolution == "1080" or resolution == "1440" or resolution == "2160" or resolution == "4320" or resolution == "MAX": # Yes, I know, looks horrible, but it works and I don't want to spend half an hour to figure out how to make it more efficient. I will make a gui anyway.
        i = True
    else:
        print("Invalid resolution. You entered: " + resolution)
        print("Please enter one of the following numbers without commas, 'p', or any extra characters: 720, 1080, 1440, 2160, 4320. You can also enter the word 'MAX' without quotation marks and in all caps to get the best available resolution.")
        

interval = int(input("Enter time interval between checks in seconds (1 hour = 3600 seconds, 1 day = 86400 seconds): "))
count = int(input("Enter total amount of checks you want to run: "))

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