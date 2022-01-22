Initial setup
 
    1. Instal dependencies. Run the following commands in your terminal: 
        pip3 install pytube

        Never paste random commands from the internet unless you trust the source! You trust me, right? 

    2. (Optional) If you want your videos to be downloaded to a specific folder, paste the path to your folder into #.download(output_path = "YOUR_PATH_HERE") on line 57. Remove the "#" and ".download()" to the left. 
        Example for Windows:
        filters.get_highest_resolution().download("C:\Downloads\YouTube\PythonForDummies\") 
        Example for good operating systems:
        filters.get_highest_resolution().download("/home/pixselious/Downloads/YouTube/RicingArtixSeason5") 

    3. Follow command line prompts. Prepare a link to your YouTube playlist. Use YouTube's share button to avoid any confusion. 
        Example:
        https://youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc



Random notes:

    There is currently no way of "politely" stopping the script, so you will have to just end that process.

    Do not set the time interval between checks to less that a couple minutes, or you will ddos your pc and google's servers.

    This script will download videos in 720p. Make sure that you have plenty of free space on your drive.

    If you see "Local video no longer exists in the playlist" don't worry, that means that last time the program checked, there was a certain video in the YouTube playlist and now there isn't. The script will not stop working and won't download that video again if it reappears in the playlist.