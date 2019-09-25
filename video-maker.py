#import statements
import json, os, string, argparse, sys, praw, shutil, gtts

#create an argument parser to parse the arguments
parser = argparse.ArgumentParser(description = 'the main program that turns a reddit URL into a video')
parser.add_argument('--post-url', dest = 'posturl', required = True, help = 'the URL for the reddit post')
parser.add_argument('--comment-limit', dest = 'commentlimit', required = True, help = 'the max amount of comments to be used for the video')
parser.add_argument('--output-path', '-o', dest = 'outputpath', required = True, help = 'the path that the program will save the final video')

#parse the arguments
arguments = parser.parse_args()

#create a reddit bot user
redditBotUser = praw.Reddit('python-reddit-comment-gatherer', user_agent = 'python-reddit-comment-gatherer')

#create a function that reads json files
def readJSONFile(path) -> dict:
    return json.loads(str(open(path).read()))

#create variables that hold the acceptable characters for posts and ones to replace them with
acceptableCharacters = [*string.ascii_lowercase, *string.ascii_uppercase, *string.digits, *string.whitespace, *str(string.punctuation.replace('"', ''))]
unacceptableCharacterReplaceWithCharatacter = '?'

#create a function to turn a string into a valid string with no unacceptable characters
def makeAcceptable(string) -> str:
    global acceptableCharacters, unacceptableCharacterReplaceWithCharatacter
    newString = ''
    string = str(string)
    for char in string:
        if (char.lower() not in acceptableCharacters): #if the character isnt recognized as a legal character then replace it with a question mark
            char = '?'
        newString += str(char)
    return newString.replace('\n', ' ') #replace new line characters with spaces

#store the max number of images that can be saved
maxNumberOfImages = 9999999

#get the data from the submission url
submission = redditBotUser.submission(url = str(arguments.posturl))
postData = {
    'title':submission.title,
    'author':submission.author,
    'score':submission.score,
    'comments':len(submission.comments)
}

#get the json data from the json files
JSONData = {
    'dimensions':readJSONFile('./utils/image-dimensions.json'),
    'fonts':readJSONFile('./utils/fonts.json'),
    'colors':readJSONFile('./utils/color-scheme.json'),
    'images':readJSONFile('./utils/images.json'),
    'ffmpeg':readJSONFile('./utils/ffmpeg-config.json')
}

#create a function that turns the lists of commands into actual command line commands
def parseCommandList(commandList) -> str:
    endString = ''
    for command in commandList:
        endString += str(str(command[0]) + ' "' + str(command[1]) + '" ')
    return endString

#create a function that fills in the rest of an integer with spaces
def makeIntegerFileCountFriendly(integer) -> str:
    global maxNumberOfImages
    integer = str(integer)
    tmpMaxNumberOfImages = str(maxNumberOfImages)
    return str(('0' * int(len(tmpMaxNumberOfImages) - len(integer)))) + str(integer)

#make an integer to store the file count
fileCount = 0

#make the command for making the title of the video
titleCommand = [
    [str(sys.executable), './title-image-maker.py'],
    ['--title-text', makeAcceptable(postData['title'])],
    ['--comments-total', postData['comments']],
    ['--upvotes-total', postData['score']],
    ['--posted-by', makeAcceptable(postData['author'])],
    ['--output-path', './tmp/coverimage/' + makeIntegerFileCountFriendly(fileCount) + '.png'],
    ['--output-image-width', JSONData['dimensions']['width']],
    ['--output-image-height', JSONData['dimensions']['height']],
    ['--background-color', JSONData['colors']['background-color']],
    ['--font-path', JSONData['fonts']['normal-font-path-from-root']],
    ['--upvote-arrow-icon-path', JSONData['images']['upvote-arrow']],
    ['--title-text-color', JSONData['colors']['post-title-text-color']],
    ['--comment-button-path', JSONData['images']['comment-button']],
    ['--comment-count-color', JSONData['colors']['post-buttons-text-color']],
]

#make a temporary directory for the images
try:
    os.mkdir('./tmp')
except:
    shutil.rmtree('./tmp')
    os.mkdir('./tmp')


#run the command for the title post
os.mkdir('./tmp/coverimage') #folder for the images on the first step of the program
os.system(parseCommandList(titleCommand))

#generate the tts file for the title
tts = gtts.gTTS(makeAcceptable(postData['title']), lang = 'en')
tts.save('./tmp/coverimage/{}.mp3'.format(makeIntegerFileCountFriendly(fileCount)))

#increase the file count
fileCount += 1

#make a directory for the comment images and tts files
os.mkdir('./tmp/images')

#get the top few post comments
commentsLimit = int(arguments.commentlimit)
commentStep = 0
for comment in submission.comments:
    commentStep += 1

    #make the command for generating the image
    imageCommand = [
        [str(sys.executable), './comment-image-maker.py'],
        ['--comment-text',  makeAcceptable(comment.body)],
        ['--upvotes-total', makeAcceptable(comment.score)],
        ['--posted-by', makeAcceptable(comment.author)],
        ['--output-path', './tmp/images/' + makeIntegerFileCountFriendly(fileCount) + '.png'],
        ['--output-image-width', JSONData['dimensions']['width']],
        ['--output-image-height', JSONData['dimensions']['height']],
        ['--background-color', JSONData['colors']['background-color']],
        ['--font-path', JSONData['fonts']['normal-font-path-from-root']],
        ['--username-text-color', JSONData['colors']['comment-username-color']],
        ['--comment-body-text-color', JSONData['colors']['comment-body-text-color']],
        ['--comment-upvotes-text-color', JSONData['colors']['comment-upvotes-text-color']],
    ]

    #run the image command
    os.system(parseCommandList(imageCommand))

    #generate the tts file
    tts = gtts.gTTS(makeAcceptable(comment.body), lang = 'en')
    tts.save('./tmp/images/{}.mp3'.format(makeIntegerFileCountFriendly(fileCount)))
    
    #increase the file count
    fileCount += 1

    #check to make sure the program hasnt gone over the comment limit
    if (commentStep >= commentsLimit):
        break

os.mkdir('./tmp/videos')