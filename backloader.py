"""
    
    Backloader will download new videos from a selected YouTube playlist.
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

pathToBaseFolder = "" 

from time import sleep

from pytube import YouTube, Playlist
from moviepy.editor import *

import multiprocessing as mp
import os
import shutil
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_stdlib_context


#   GETTING URL OF VIDEOS FROM A PLAYLIST

def getUrls(playlistUrl):
    # Getting URLs of videos from a playliat. Returns a list of strings
    playlist = Playlist(playlistUrl)
    
    urls = list(playlist.video_urls)
    
    return(urls)

def URLtoID(url):
    # Converts URLs from pytube to IDs for the database. This only works for regular short links, like the ones we get from pytube. Returns a string.
    id = url.split("=")[1]
    return id


def removeBadChars(string):
    blacklist = ["|", "/", "\\"] # This script is designed to run on UNIX based OS's. If you are using Windows, consider switching to Linux. Or run this script in a Linux container.
    
    for i in blacklist:
        string = string.replace(i, "")
    return string

#   DOWNLOADING VIDEOS

def downloadProgressive(url, pathToTargetFolder):
    # Download video in the highest progressive (image + sound) resolution. Returns a Video() object. 
    print('Started ' + url)
    
    try:
        youtube = YouTube(url)
    
        filters = youtube.streams.filter(progressive=True, file_extension = "mp4")
        
        filters.get_highest_resolution().download(output_path = pathToTargetFolder, filename = removeBadChars(youtube.title) + ".mp4")
        
        # Download the thumbnail
        
        urllib.request.urlretrieve(youtube.thumbnail_url, pathToTargetFolder + "/poster.jpg")
        
        print('Downloaded')
        
    except Exception as e:
        print(e)
        
def downloadHiRes(url, resolution, pathToTargetFolder):
    # Download video and audio separately and them merge them. Returns a Video() object.
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
        
        
        video.first().download(filename = "temp_video_" + URLtoID(url) + ".mp4")
        
        # Downloading the audio
        
        audio = youtube.streams
        audio.get_audio_only().download(filename = "temp_audio_" + URLtoID(url) + ".mp4")
        
        # Merging video and audio together
        
        print('Merging video and audio, this might take a while')
        
        videoClip = VideoFileClip(os.path.normcase("temp_video_" + URLtoID(url) + ".mp4"))
        audioClip = AudioFileClip(os.path.normcase("temp_audio_" + URLtoID(url) + ".mp4"))
        
        completeClip = videoClip.set_audio(audioClip)
        completeClip.write_videofile(filename = "final_" + url.split("v=")[-1] + ".mp4", audio_codec = "aac")
        
        # Removing temporary video and audio files
        
        os.remove(os.path.normcase("temp_video_" + URLtoID(url) + ".mp4"))
        os.remove(os.path.normcase("temp_audio_" + URLtoID(url) + ".mp4"))
        
        shutil.move(URLtoID(url) + ".mp4", os.path.normcase("./videos"))
        
    
        # Renaming final file here instead of during creation to not confuse the terminal with emojis or anything like that.
        
        #TODO: give savers a complete path instead of them coming up with a new one on their own
        
        newName = removeBadChars(youtube.title) + ".mp4"
        os.rename("final_" + url.split("v=")[-1] + ".mp4", newName)
        
        if len(pathToBaseFolder) != 0:
            shutil.move(newName, pathToTargetFolder)
            urllib.request.urlretrieve(youtube.thumbnail_url, pathToTargetFolder + "/poster.jpg")
            
        
        print('Merged')
        print("")
        
    except Exception as e:
        print(e)


    
#   LOGGING DOWNLOADED VIDEOS

# Creates a log file on the first run 
#TODO: put this in a for loop under if __name__ == '__main__':
try:
    file = open(pathToBaseFolder + "/downloadedUrls" + '.txt', 'x')
    file.close
except:
    pass
#TODO: make separate files for different playlists
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


#   SAVING FLOW SETTINGS AND OTHER FLOW HELPER FUNCTIONS

#TODO add a list of dict that fetches and stores itself in a json file and has a setter fuction for flows to selfreport (sus) their settings

jellyfin = True

flowData = [] # Stores flow settings. Saved to a json file.
flowProcesses = []

"""
"id" : 0,
"name" : "0 playlist title",
"workingDirectory" : "/media",
"interval" : 43200,
"limit" : 0,
"resolution" : "720",
"playlistUrl" : ""
"""


def getPlaylistName(url):
    # Gets the name of a playlist
    playlist = Playlist(url = url)
    name = playlist.title
    return(name)

# Creates a dictionary and adds it to the list
def createFlow(workingDirectory, interval, limit, resolution, playlistUrl):
    
        id = len(flowData)
        name = str(id) + " " + removeBadChars(getPlaylistName(playlistUrl))
        if jellyfin:
            workingDirectory = workingDirectory + "/" + name
            
        newFlow = {"id" : id,
            "name" : name,
            "workingDirectory" : workingDirectory,
            "interval" : interval,
            "limit" : limit,
            "resolution" : resolution,
            "playlistUrl" : playlistUrl
        }
        
        flowData.append(newFlow)
        print("Added new flow " + str(newFlow))
 
    

#   CHECKING FOR NEW VIDEOS AND DOWNLOADING THEM

def checkPlaylist(playlistUrl):
    local = readFile()
    online = getUrls(playlistUrl)
    newVideos = compare(local, online)
    
    return(newVideos)

def downloadVideos(urls, resolution, path):
    for url in urls:
        if resolution == "720":
            downloadProgressive(url, path)
        else:
            downloadHiRes(url, resolution, path)
        
        
#   UI

if showLicenceNotice == True:
    print("""
    Backloader  Copyright (C) 2022  Pixselious
    This program comes with ABSOLUTELY NO WARRANTY; for details read LICENCE.txt .
    This is free software, and you are welcome to redistribute it
    under certain conditions; Read LICENCE.txt for details.
    
    Thank you to the contributors of pytube and moviepy
    """)

print("")


def flowInstance (id, name, workingDirectory, interval, limit, resolution, playlistUrl):

    print("Launched flow " + name)
    
    #currentVideos = checkPlaylist(playlistUrl)
    #appendFile(currentVideos) 

    if limit == 0:
        
        while True:
            newVideos = checkPlaylist(playlistUrl)
            
            if len(newVideos) == 0:
                print("No new videos")
            else:
                downloadVideos(newVideos, resolution, workingDirectory)
                appendFile(newVideos)
            
            print("Waiting " + str(interval) + " seconds")
            sleep(interval)
            
    else:
            
        for i in range(limit):
            newVideos = checkPlaylist(playlistUrl)
            
            if len(newVideos) == 0:
                print("No new videos")
            else:
                downloadVideos(newVideos, resolution, workingDirectory)
                appendFile(newVideos)
            
            print("Waiting " + str(interval) + " seconds")
            sleep(interval)
    
            
            i += 1
            
        print("Reached limit of checks")
        
    
    
    
    
# MULTIPROCESSING


if __name__ == '__main__':
    
    #TODO: Load flowData from memory
    
    # Debug
    createFlow(workingDirectory= "", interval= 3, limit= 3, resolution= "720", playlistUrl= "")
    
    for flow in flowData:
        flowProcesses.append(mp.Process(target = flowInstance, name = "Backloader " + flow["name"], args = (flow["id"], flow["name"], flow["workingDirectory"], flow["interval"], flow["limit"], flow["resolution"], flow["playlistUrl"])))
    
    for process in flowProcesses:
        process.start()
    
