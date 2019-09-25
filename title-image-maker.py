#print that the program is starting
print ('title-image-maker.py is running')

#import statements
import PIL.ImageDraw, PIL.ImageFont, PIL.Image, argparse, textwrap

#create an argument parser for the program (make sure no non alphanumeric characters are passed)
parser = argparse.ArgumentParser()
parser.add_argument('--title-text', dest = 'titletext', required = True)
parser.add_argument('--comments-total', dest = 'commentstotal', required = True)
parser.add_argument('--upvotes-total', dest = 'upvotestotal', required = True)
parser.add_argument('--posted-by', dest = 'postedby', required = True)
parser.add_argument('--output-path', dest = 'outputpath', required = True)
parser.add_argument('--output-image-width', dest = 'outputimagewidth', required = True)
parser.add_argument('--output-image-height', dest = 'outputimageheight', required = True)
parser.add_argument('--background-color', dest = 'backgroundcolor', required = True)
parser.add_argument('--font-path', dest = 'fontpath', required = True)
parser.add_argument('--upvote-arrow-icon-path', dest = 'upvotearrowpath', required = True)
parser.add_argument('--title-text-color', dest = 'titletextcolor', required = True)
parser.add_argument('--comment-button-path', dest = 'commentbuttonpath', required = True)
parser.add_argument('--comment-count-color', dest = 'commentcountcolor', required = True)

#parse the arguments
arguments = parser.parse_args()

#create the pillow image
image = PIL.Image.new('RGBA', [int(arguments.outputimagewidth), int(arguments.outputimageheight)], color = str(arguments.backgroundcolor))

#create a pillow image draw object
draw = PIL.ImageDraw.Draw(image)

#draw the reddit upvote arrow icon to the corner of the screen
redditUpvoteArrowImage = PIL.Image.open(str(arguments.upvotearrowpath))
redditUpvoteArrowImageSize = int(int(arguments.outputimageheight) / 10)
redditUpvoteArrowOffset = int(redditUpvoteArrowImageSize / 2)
redditUpvoteArrowImage = redditUpvoteArrowImage.resize([redditUpvoteArrowImageSize, redditUpvoteArrowImageSize], PIL.Image.ANTIALIAS)

#paste the new upvote arrow image on top of the base image
image.paste(redditUpvoteArrowImage, ([redditUpvoteArrowOffset, redditUpvoteArrowOffset]), redditUpvoteArrowImage)

#make a variable to hold the size of the text
textSizeDefault = int(int(int(arguments.outputimageheight) / 10) / 2)

#wrap the title text to fit on one line
wordsPerLine = int(int(arguments.outputimagewidth) / (textSizeDefault * 0.55)) #since words have about a 1:2 ratio, divide the text size by 2 to get how many words fit
wrappedTitleText = textwrap.wrap(str(arguments.titletext), wordsPerLine)

#create a font object to be used for font drawing
defaultFont = PIL.ImageFont.truetype(str(arguments.fontpath), textSizeDefault)

#draw the text that says who posted it
poster = 'u/' + str(arguments.postedby)
postTextSize = int(textSizeDefault / 2)
postTextFont = PIL.ImageFont.truetype(str(arguments.fontpath), postTextSize)
draw.text([(redditUpvoteArrowOffset * 2) + redditUpvoteArrowImageSize, redditUpvoteArrowOffset], poster, str(arguments.titletextcolor), font = postTextFont)

#create a variable to tell where the top of the title text is
topOfTitleTextOffset = (redditUpvoteArrowOffset * 2) + postTextSize

#draw the text to the screen that says the title
lineCount = 0
for line in wrappedTitleText:
    draw.text([(redditUpvoteArrowOffset * 2) + redditUpvoteArrowImageSize, topOfTitleTextOffset + int(lineCount * textSizeDefault)], wrappedTitleText[lineCount], str(arguments.titletextcolor), font = defaultFont)
    lineCount += 1

#draw the text that says the number of upvotes
upvotes = int(arguments.upvotestotal)
upvotesTextSize = textSizeDefault
upvotesTextFont = PIL.ImageFont.truetype(str(arguments.fontpath), upvotesTextSize)
upvotesTextSizeOnScreenPixels = draw.textsize(str(upvotes), font = upvotesTextFont)
upvotesTextPosition = [int(((redditUpvoteArrowImageSize + (redditUpvoteArrowOffset * 2)) - upvotesTextSizeOnScreenPixels[0]) / 2), redditUpvoteArrowImageSize + (redditUpvoteArrowOffset * 2)]
draw.text(upvotesTextPosition, str(upvotes), str(arguments.titletextcolor), font = upvotesTextFont)

#resize and paste the comment button onto the screen
redditCommentButtonImage = PIL.Image.open(str(arguments.commentbuttonpath))
redditCommentButtonImage = redditCommentButtonImage.resize([redditUpvoteArrowImageSize, redditUpvoteArrowImageSize], PIL.Image.ANTIALIAS)
redditCommentButtonCoords = [redditUpvoteArrowOffset, int(int(arguments.outputimageheight) - redditUpvoteArrowOffset - redditUpvoteArrowImageSize)]
image.paste(redditCommentButtonImage, (redditCommentButtonCoords), redditCommentButtonImage)

#create text that shows the amount of comments
comments = int(arguments.commentstotal)
commentsTextFont = PIL.ImageFont.truetype(str(arguments.fontpath), redditUpvoteArrowImageSize)
draw.text([redditCommentButtonCoords[0] + redditUpvoteArrowImageSize + redditUpvoteArrowOffset, redditCommentButtonCoords[1]], str(comments) + ' Comments', str(arguments.commentcountcolor), font = commentsTextFont)

#save the pillow image
image.save(str(arguments.outputpath))