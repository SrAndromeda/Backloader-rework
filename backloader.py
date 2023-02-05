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

from time import sleep
from yt_dlp import YoutubeDL
import os
from PIL import Image
import multiprocessing as mp
import json



#   GETTING URL OF VIDEOS FROM A PLAYLIST


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


def download(url, resolution, pathToTargetFolder, flowId):
    
    #Selecting resolution
    if str(resolution) == '720':
        format = 'best' # Selecting the best progressive (video and audio in one file) stream
    elif str(resolution) == 'BEST':
        format = 'bestaudio[ext=m4a]+bestvideo[ext=mp4]/best' #Selecting best audio and merging it to best video. If NA, fall back to best progressive stream.
    elif str(resolution) == 'WORST':
        format = 'wv*+wa'       #Selecting worst video and merging it to worst audio !!!very slow download speed!!!
    elif str(resolution) == 'AUDIO':
        format = 'bestaudio[ext=m4a]' #Selecting the best audio only stream 
    else:
        format = 'bestaudio[ext=m4a]+bestvideo[height={}][ext=mp4]/bestaudio[ext=m4a]+bestvideo[ext=mp4]/best'.format(str(resolution)) #Selecting best audio and merging it to video of requested resolution. If NA, fall back to best separate streams, if NA fall back to best progressive stream.

    
    #Selecting appropriate output templates for each supported library type
    #Guide for these unreadable blobs https://github.com/yt-dlp/yt-dlp#output-template
    if str(resolution) == 'AUDIO':
        outtmpl = {
                'default': '%(channel)s /%(title)s.%(ext)s'
        } # Music library type https://jellyfin.org/docs/general/server/media/music.html
    else:
        outtmpl = {
                'default': '%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s',
                'thumbnail': '%(title)s [%(id)s]/poster.%(ext)s',
                'infojson': '%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s'
            } # Movies library type https://jellyfin.org/docs/general/server/media/movies.html
    

    try:
        
        ydl_opts = {
            'format': format,       #What to download
            'writethumbnail': 'True',       #Download the thumbnail
            'download_archive': 'downloaded_{}.txt'.format(flowId),         #Keep a record of  downloaded videos 
            'writeinfojson': 'True',        #Download video metadata (description, author, etc)
            'merge_output_format': 'mp4',       #Keep videos mp4
            'paths': {
                'home': pathToTargetFolder,
                'temp': pathToTargetFolder + '/tmp'
            },      #Where to save the videos
            'outtmpl': outtmpl,         #Where to save the videos and how to name them
            'progrss': 'True',       #Show progress bars   
            'embed_metadata': 'True'        #Embed the thumbnail, subtitles, chapters and other metadata when possible 
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([ "%s" %url ]) # It wants me to pass a list of urls so i'm creating one right here
        
        
    except Exception as e:
        print(e)




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
        
    with YoutubeDL({'quiet': 'True', 'ignoreerrors': True, }) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        #playlist_url = info_dict.get("url", None)
        #playlist_id = info_dict.get("id", None)
        playlist_title = info_dict.get('title', None)

    return(playlist_title) 

# Creates a dictionary and adds it to the list
def createFlow(workingDirectory, interval, limit, resolution, playlistUrl):
    
        id = len(flowData)
        name = str(id) + " " + removeBadChars(getPlaylistName(playlistUrl))
        
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
 
    
# Loads flow data from config.json 
def loadFlows():
    f = open('config.json')

    data = json.load(f)

    for i in data['flows']:
        createFlow(i["base_directory"], int(i["interval"]), int(i["limit"]), i["resolution"], i["url"])
        
    f.close()



        
        
#   UI

if showLicenceNotice == True:
    print("""
    Backloader  Copyright (C) 2022  Pixselious
    This program comes with ABSOLUTELY NO WARRANTY; for details read LICENCE.txt .
    This is free software, and you are welcome to redistribute it
    under certain conditions; Read LICENCE.txt for details.
    
    Thank you to the contributors of yt-dlp
    """)

print("")


def flowInstance (id, name, workingDirectory, interval, limit, resolution, playlistUrl):

    print(name+" Flow started")
        
    if limit == 0:   
        while True:
            print(name+" Checking playlist")
            download(playlistUrl, resolution, workingDirectory, id) #Downloading videos, thumbnails and metadata
            
            thumbnails = [os.path.join(root, name) #Getting paths to all thumbnails
                for root, dirs, files in os.walk(workingDirectory)
                for name in files
                if name.endswith(".webp")]
            
            for thumbnail in thumbnails: #Converting thumbnails into a supported format
                tmp = Image.open(thumbnail).convert("RGB")
                tmp.save(thumbnail.replace(".webp", ".jpg"), "jpeg")
                os.remove(thumbnail) #Removing old thumbnails
            
            print(name+" Waiting " + str(interval) + " seconds")
            sleep(interval)
    else:
        for i in range(limit):
            print(name+" Checking playlist")
            download(playlistUrl, resolution, workingDirectory, id)    
            
            thumbnails = [os.path.join(root, name)
                for root, dirs, files in os.walk(workingDirectory)
                for name in files
                if name.endswith(".webp")]
            
            for thumbnail in thumbnails:
                tmp = Image.open(thumbnail).convert("RGB")
                tmp.save(thumbnail.replace(".webp", ".jpg"), "jpeg")
                os.remove(thumbnail)
            
            print(name+" Waiting " + str(interval) + " seconds")
            sleep(interval)
            
            i += 1
        print(name+" Reached limit of checks")
        
    print(name+" Flow ended")
        

    
    
# MULTIPROCESSING


if __name__ == '__main__':
    
    loadFlows()
    
    # Uncomment and fill out the template below if you want to skip the config.json file
    #createFlow(workingDirectory= "/path/to/jellyfin/media", interval= 3600, limit= 0, resolution= "720", playlistUrl= "https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
    
    for flow in flowData:
        flowProcesses.append(mp.Process(target = flowInstance, name = "Backloader " + flow["name"], args = (flow["id"], flow["name"], flow["workingDirectory"], flow["interval"], flow["limit"], flow["resolution"], flow["playlistUrl"])))
    
    for process in flowProcesses:
        process.start()
    
