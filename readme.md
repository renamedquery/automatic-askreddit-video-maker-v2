# Automatic Askreddit Video Generator

***How to use it:***

*1.] Set up FFMPEG and install it. Once you have FFMPEG installed, then set the path in the file "./utiks/ffmpeg-config.json" to the path for the command. It should be set to something like "ffmpeg" or "%appdata%/ffmpeg/ffmpeg.exe".*

*2.] Configure the "praw.ini" file in this folder. If you need help on how to fill it out, try looking it up. Without proper information in this file, then the program wont work, as it will fail to authenticate.*

*3.] Get the link of an askreddit thread that you want to use. The program works for any askreddit thread as long as it contains a title and comments.*

*4.] Run the program. The syntax and an example of the command are shown below:*

*Syntax:* `{pythonRunCommand} ./video-maker.py --post-url {postURL} --comment-limit {commentLimit} --output-path {outputPath}`

*Example:* `python ./video-maker.py --post-url "https://new.reddit.com/r/AskReddit/comments/d8raq7/a_time_machine_has_been_created_but_due_to_an/" --comment-limit "2" --output-path "output.mp4"`

***If you have any issues with the program, then leave an issue on the github repo.***