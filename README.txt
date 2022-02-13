Initial setup
 
    1. Instal dependencies. Run the following commands in your terminal: 
        pip3 install pytube
        pip3 install moviepy

        Never paste random commands from the internet unless you trust the source! You trust me, right? 

    2. (Optional) If you want your videos to be downloaded to a specific folder, paste the full path to your folder into pathToTargetFolder = "" on line 24.
        Example for Windows:
        pathToTargetFolder = "C:\Users\Name\Downloads\YouTube\PythonForDummies\"
        Example for good operating systems:
        pathToTargetFolder = "/home/pixselious/Downloads/YouTube/RicingArtixSeason5"

    3. Follow command line prompts. Prepare a link to your YouTube playlist. Use YouTube's share button to avoid any confusion. Make sure it is public or available by link.
        Example:
        https://youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc

Because of the way YouTube works, downloading videos in 720p is much faster than higher resolutions and does not require intense post-processing on your computer. 
Consider limiting the script to 720p if you are running it on your main machine.


Random notes:

    YouTube stores files with both video and sound only in resolutions up to 720p. To get a higher resolution video, this script downloads video and audio separatley and then merges them on your computer. This requires either a lot of time or a powerful computer.

    There is currently no way of "politely" stopping the script, so you will have to just end that process.

    If you see "Local video no longer exists in the playlist" don't worry, that means that last time the program checked, there was a certain video in the YouTube playlist and now there isn't. The script will not stop working and won't download that video again if it reappears in the playlist.

    This script does not support HDR videos, they will be compressed into SDR. This is a limitation of the moviepy library. I don't need to download HDR videos, so they won't be supported anytime soon. But feel free to do it yourself, after all this project is open-source!
