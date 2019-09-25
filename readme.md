# Automatic Askreddit Video Generator

***How to use it:***

*1.] Set up your FFMPEG run command. If you are on windows then you don't need to do anything, but if you are on linux you might have to do something like change the path to "ffmpeg" if its a command, or if you have it installed in the folder, then "./ffmpeg/ffmpeg.sh".*

*2.] Get the link of an askreddit thread that you want to use. The program works for any askreddit thread as long as it contains a title and comments.*

*3.] Run the program. The syntax and an example of the command are shown below:*

*Syntax:* `{pythonRunCommand} ./video-maker.py --post-url {postURL} --comment-limit {commentLimit}`

*Example:* `python ./video-maker.py --post-url "https://new.reddit.com/r/AskReddit/comments/d8raq7/a_time_machine_has_been_created_but_due_to_an/" --comment-limit "2"`

***If you have any issues with the program, then leave an issue on the github repo.***