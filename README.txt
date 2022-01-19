Initial setup
 
    1. Instal dependencies. Run the following commands in your terminal: 
        pip3 install pytube
        pip3 install --upgrade google-api-python-client

        Never paste random commands from the internet unless you trust the source! You trust me, right? 

    2. Paste your Youtube Data API v3 key into developerKey = "YOUR_API_KEY_HERE" on line 36. 
        Example:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "mguYreQMoiQRb9W4CoAj")

        Never share your API key with anyone! Think of it like a password to your account. That example was just a random string.

    3. (Optional) If you want your videos to be downloaded to a specific folder, paste the path to your folder into #.download(output_path = "YOUR_PATH_HERE") on line 79. Remove the "#" and ".download()" to the left. 
        Example for Windows:
        filters.get_highest_resolution().download("C:\Downloads\YouTube\PythonForDummies\") 
        Example for good operating systems:
        filters.get_highest_resolution().download("/home/pixselious/Downloads/YouTube/RicingArtixSeason5") 

    4. Follow command line prompts. Prepare a complete link to your YouTube playlist. Use YouTube's share function to avoid any confusion. 
        Example:
        https://youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc



Random notes:

    There is currently no way of "politely" stopping the script, so you will have to just end that process.

    Do not set the time interval between checks to less that a couple minutes, or you will ddos your pc and google's servers.

    This script will download videos in the highest available quality. Make sure that you have plenty of free space on your drive. (I don't know what will happen if there isn't enough space)

    There is a hard limit on how many videos can be viewed by the script. The default is 999. You can raise it on line 49, but your pc will probably explode from that amount of data.

    If you see "Local video no longer exists in the playlist" don't worry, that means that last time the program checked, there was a certain video in the YouTube playlist and now there isn't. The script will not stop working and won't download that video again if it reappears in the playlist.



How to get an API key:

    1. Go to Google Developer Console

    2. Search and enable "Youtube Data API v3"

    3. Click "Create credentials", then select "Youtube Data API v3" and "Public data".
