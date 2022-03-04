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


from fileinput import filename
from multiprocessing import connection
from time import sleep

from pytube import YouTube, Playlist
from moviepy.editor import *

import os
import shutil
import ssl
import urllib.request
import sqlite3

ssl._create_default_https_context = ssl._create_stdlib_context



#   SETTING UP SQL

sqliteConnection = sqlite3.connect("backloader.db")
cursor = sqliteConnection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS videos(
    id TEXT PRIMARY KEY,
    url TEXT,
    name TEXT,
    thumbnail TEXT,
    description TEXT,
    tags TEXT,
    file TEXT,
    quality INT,
    playlist TEXT,
    channel TEXT);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS playlists(
    id TEXT PRIMARY KEY,
    url TEXT,
    name TEXT,
    quality INT,
    settings TEXT);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS channels(
    id TEXT PRIMARY KEY,
    url TEXT,
    name TEXT,
    profile TEXT);
""")

sqliteConnection.commit()



#   DEFINING CLASSES FOR PASSING DATA INSIDE THIS SCRIPT AND TO UI
class Video:
    def __init__(self, id, url, name, thumbnail, description, tags, file, quality, playlist, channel):
        self.id = id
        self.url = url
        self.name = name
        self.thumbnail = thumbnail
        self.description = description
        self.tags = tags
        self.file = file
        self.quality = quality
        self.playlist = playlist
        self.channel = channel



#   GETTING URL OF VIDEOS FROM A PLAYLIST

def getUrls(playlistUrl):

    playlist = Playlist(playlistUrl)
    
    urls = list(playlist.video_urls)
    
    return(urls)


def URLtoID(url):
    # Converts URLs from pytube to IDs for the database. This only works for regular short links, like the ones we get from pytube.
    id = url.split("=")[1]
    return id



#   DOWNLOADING VIDEOS

def download(url):
    
    print('Started ' + url)
    
    try:
        youtube = YouTube(url)
    
        filters = youtube.streams.filter(progressive=True, file_extension = "mp4")
        
        filters.get_highest_resolution().download(filename = URLtoID(url) + ".mp4", output_path = os.path.normcase("./videos"))
        
        print('Downloaded')
        
        # Download the thumbnail
        
        urllib.request.urlretrieve(youtube.thumbnail_url, os.path.normcase("./thumbnails/") + URLtoID(url) + ".jpg")
        
        # Prepare data for the database
        
        video = Video(URLtoID(url), url, youtube.title, os.path.abspath(os.path.normcase("./thumbnails/") + URLtoID(url) + ".jpg"), youtube.description, youtube.keywords, os.path.abspath(os.path.normcase("./videos/") + URLtoID(url) + ".mp4"), resolution, "Default", youtube.channel_id)
        
        return(video)
        
    except Exception as e:
        print(e)
    
def downloadHiRes(url, resolution):
    
    resolution = resolution + "p"
    
    print('Started ' + url)
    
    try:
        youtube = YouTube(url)
    
        # Getting all available resolutions
    
        video = youtube.streams.filter(only_video = True, file_extension = "mp4")
        
        # Checking if user requested a specific resolution
        if resolution != "MAXp":
            # Checking if the requested resolution is available
            temp = video.filter(res = resolution)
            
            if len(temp) == 0: 
                # If the video is not available in the requested resolution, get the highest possible.
                print("Requested resolution is not available")
                video.desc()
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
        completeClip.write_videofile(filename = URLtoID(url) + ".mp4", audio_codec = "aac")
        
        # Removing temporary video and audio files
        
        os.remove("temp_video_" + url.split("v=")[-1] + ".mp4")
        os.remove("temp_audio_" + url.split("v=")[-1] + ".mp4")
        
        shutil.move(URLtoID(url) + ".mp4", os.path.normcase("./videos"))
        
    
        print('Merged')
        print("")
        
        # Download the thumbnail
        
        urllib.request.urlretrieve(youtube.thumbnail_url, os.path.normcase("./thumbnails/") + URLtoID(url) + ".jpg")
        
        # Prepare data for the database
        
        video = Video(URLtoID(url), url, youtube.title, os.path.abspath(os.path.normcase("./thumbnails/") + URLtoID(url) + ".jpg"), youtube.description, youtube.keywords, os.path.abspath(os.path.normcase("./videos/") + URLtoID(url) + ".mp4"), resolution, "Default", youtube.channel_id)
    
        return(video)
        
    except Exception as e:
        print(e)
    
    
#   LOGGING DOWNLOADED VIDEOS

# Creates folders on the first run 

try:
    os.mkdir("videos")
except:
    pass

try:
    os.mkdir("thumbnails")
except:
    pass

try:
    os.mkdir("channels")
except:
    pass

# Used to add urls of newly downloaded videos to a log file
def updateVideos(videos):
    for video in videos:
        
        cursor.execute(f"""INSERT INTO videos(
            id,
            url,
            name,
            thumbnail,
            description,
            tags,
            file,
            quality,
            playlist,
            channel)
            
            VALUES(
            "{video.id}",
            "{video.url}",
            "{video.name}",
            "{video.thumbnail}",
            "{video.description}",
            "{video.tags}",
            "{video.file}",
            "{video.quality}",
            "{video.playlist}",
            "{video.channel}")
        ;""")
        
    sqliteConnection.commit()

# Used to fetch urls of previously downloaded videos to compare with urls from YT playlist
def readVideos(playlistUrl):
    urls = []
    
    cursor.execute(f""" SELECT url 
        FROM videos 
        WHERE playlist = '{URLtoID(playlistUrl)}'
    ;""")
    
    data = cursor.fetchall()
    
    for url in data:
        urls.append(url[0])
    
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
    local = readVideos(playlistUrl)
    online = getUrls(playlistUrl)
    newVideos = compare(local, online)
    
    return(newVideos)

def downloadVideos(urls, resolution, playlistUrl):
    report = []
    for url in urls:
        if resolution == "720":
            video = download(url)
        else:
            video = downloadHiRes(url, resolution)
        
        video.playlist = URLtoID(playlistUrl)
        report.append(video)
        
    return(report)
        
        
        
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
    updateVideos(currentVideos)

for i in range(count):
    newVideos = checkPlaylist(playlistUrl)
    
    if len(newVideos) == 0:
        print("No new videos")
    else:
        report = downloadVideos(newVideos, resolution, playlistUrl)
        updateVideos(report)
    
    print("Waiting " + str(interval) + " seconds")
    sleep(interval)
    
    i += 1
    
print("Reached limit of checks")