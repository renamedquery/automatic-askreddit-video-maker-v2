#print that the program is starting
print ('comment-image-maker.py is running')

#import statements
import PIL.ImageDraw, PIL.ImageFont, PIL.Image, argparse, textwrap

#create an argument parser for the program (make sure no non alphanumeric characters are passed)
parser = argparse.ArgumentParser()
parser.add_argument('--comment-text', dest = 'commenttext', required = True)
parser.add_argument('--upvotes-total', dest = 'upvotestotal', required = True)
parser.add_argument('--posted-by', dest = 'postedby', required = True)
parser.add_argument('--output-path', dest = 'outputpath', required = True)
parser.add_argument('--output-image-width', dest = 'outputimagewidth', required = True)
parser.add_argument('--output-image-height', dest = 'outputimageheight', required = True)
parser.add_argument('--background-color', dest = 'backgroundcolor', required = True)
parser.add_argument('--font-path', dest = 'fontpath', required = True)
parser.add_argument('--username-text-color', dest = 'usernametextcolor', required = True)
parser.add_argument('--comment-body-text-color', dest = 'commentbodytextcolor', required = True)
parser.add_argument('--comment-upvotes-text-color', dest = 'commentupvotestextcolor', required = True)

#parse the arguments
arguments = parser.parse_args()

#create the pillow image
image = PIL.Image.new('RGBA', [int(arguments.outputimagewidth), int(arguments.outputimageheight)], color = str(arguments.backgroundcolor))

#create a pillow image draw object
draw = PIL.ImageDraw.Draw(image)

#find a nice margin size for the text
marginSize = int(int(arguments.outputimageheight) / 10)

#draw the text that says the users name and the comment score
textSizeForTopRow = int(int(arguments.outputimageheight) / 25)
topRowFont = PIL.ImageFont.truetype(str(arguments.fontpath), textSizeForTopRow)
textSizeForTopRowLeftTextActual = draw.textsize('u/' + str(arguments.postedby) + ' ', font = topRowFont)
draw.text([marginSize, marginSize], 'u/' + str(arguments.postedby), str(arguments.usernametextcolor), font = topRowFont)
draw.text([marginSize + textSizeForTopRowLeftTextActual[0], marginSize], str(arguments.upvotestotal) + ' points', str(arguments.commentupvotestextcolor), font = topRowFont)

#draw the comment body text
textSizeForCommentBody = int(int(arguments.outputimageheight) / 20)
commentBodyFont = PIL.ImageFont.truetype(str(arguments.fontpath), textSizeForCommentBody)
averageWordSize = draw.textsize('a', font = commentBodyFont)
wordsPerLine = int(int(int(int(arguments.outputimagewidth)) - (marginSize * 2)) / averageWordSize[0])
commentText = textwrap.wrap(str(arguments.commenttext), wordsPerLine)
lineCount = 1
for line in commentText:
    commentYPosition = (textSizeForTopRowLeftTextActual[1] * 3) + (textSizeForCommentBody * lineCount)
    if (commentYPosition + (textSizeForCommentBody * 3) >= int(arguments.outputimageheight)):
        line = '...'
    draw.text([marginSize, commentYPosition], str(line), str(arguments.commentbodytextcolor), font = commentBodyFont)
    lineCount += 1
    if (commentYPosition + (textSizeForCommentBody * 3) >= int(arguments.outputimageheight)):
        break

#save the image
image.save(str(arguments.outputpath))