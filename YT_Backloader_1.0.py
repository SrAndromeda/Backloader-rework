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



from time import sleep
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
from pytube import YouTube
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

# Go to Google Developer Console, search and enable Youtube Data API v3, then create a credential for Public Data and paste the API key to developerKey = "YOUR_API_KEY_HERE"

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "YOUR_API_KEY_HERE")


#   GETTING URL OF VIDEOS FROM A PLAYLIST

def getUrls(playlistUrl):
    url = playlistUrl
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 999
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)


    urls = [ 
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
        for t in playlist_items
    ]
    
    return(urls)



#   DOWNLOADING VIDEOS

def download(url):
    
    print('Started ' + url)
    
    try:
        yt_obj = YouTube(url)
    
        filters = yt_obj.streams.filter(progressive=True, file_extension='mp4')
        filters.get_highest_resolution().download() #.download(output_path = "YOUR_PATH_HERE")
        print('Downloaded ' + url)
        
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
    newUrls.sort()
    with open("downloadedUrls" + '.txt', 'a') as file:
        for url in newUrls:
            file.write(url + " ") # Im sick and tired of trying to write each url on a new line I cant make it read properly

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

def downloadVideos(urls):
    for url in urls:
        download(url)
        
        
        
#   UI

if showLicenceNotice == True:
    print("""
    YouTube Backloader  Copyright (C) 2022  Pixselious
    This program comes with ABSOLUTELY NO WARRANTY; for details read LICENCE.txt .
    This is free software, and you are welcome to redistribute it
    under certain conditions; Read LICENCE.txt for details.
    """)

playlistUrl = input("Enter playlist URL:")
ignoreCurrent = input("Do you want to download videos thet are already in this playlist? (Y/N)")
interval = int(input("Enter time interval between checks in seconds (1 hour = 3600 seconds, 1 day = 86400 seconds):"))
count = input("Enter total amount of checks you want to run:")

if ignoreCurrent == ("n" or "N"):
    currentVideos = checkPlaylist(playlistUrl)
    appendFile(currentVideos)

for i in range(int(count)):
    newVideos = checkPlaylist(playlistUrl)
    
    if len(newVideos) == 0:
        print("No new videos")
    else:
        downloadVideos(newVideos)
        appendFile(newVideos)
    
    print("Waiting " + str(interval) + " seconds")
    sleep(interval)
    
    i += 1
    
print("Reached limit of checks")