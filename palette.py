import cluster
from os.path import basename
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time

orig_images = ['flatui.png','kite.jpg', 'smaller.jpg', 'google-logo.jpg']
img_Dir = "images/"
numColors = 5

'''
Finds the colors using clustering and append it on the 
right side of the image
'''

# Create equal sized squares of colors
def splicer(origImageSize):
    verticalSize = int(origImageSize[1]/(numColors))
    width = 150;

    verticalImageSize = []
    for i in range(numColors-1):
        size = (width, verticalSize)
        verticalImageSize.append(size)

    verticalImageSize.append((width, origImageSize[1] - (verticalSize * (numColors-1))))
    return verticalImageSize

#Sets the hex value of each color on the image
def setHexVals(coloredImages, colors):
    for i, img in enumerate(coloredImages):
        hex = "#{0:02x}{1:02x}{2:02x}".format(colors[i][0], colors[i][1], colors[i][2])
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", size=18)
        x = 30
        y = img.size[1] - 30
        draw.text((x-1,y-1), hex, (0,0,0), font=font)
        draw.text((x+1,y-1), hex, (0,0,0), font=font)
        draw.text((x-1,y+1), hex, (0,0,0), font=font)
        draw.text((x+1,y+1), hex, (0,0,0), font=font)
        draw.text((x,y), hex, (255, 255, 255), font=font)

# Create Vertical strip of found colors
def vertical_image(colors, origImageSize):
    verticalImageSize = splicer(origImageSize)
    coloredImages = [Image.new("RGB", verticalImageSize[i], colors[i]) for i in range(numColors)]
    fullImage = Image.new("RGB", (verticalImageSize[0][0], origImageSize[1]))
    setHexVals(coloredImages, colors)

    y_offset = 0
    for img in coloredImages:
        fullImage.paste(img, (0, y_offset))
        y_offset += verticalImageSize[0][1]

    return fullImage

# Combines The base image with the color palette strip
def combine_images(palleteImage, orig, origImageSize):
    palleteSize = palleteImage.size
    totalSize = (palleteSize[0] + origImageSize[0], origImageSize[1])
    combinedImage = Image.new("RGB", totalSize)

    combinedImage.paste(orig, (0,0))
    combinedImage.paste(palleteImage, (origImageSize[0], 0)) 
    return combinedImage  

def main():
    for idx, orig_image in enumerate(orig_images):
        im = Image.open(img_Dir + orig_image).convert('RGB')
        colors = []

        if((im.size[0] * im.size[1]) > 22500):
            colors = list(im.resize((150,150)).getdata())
        else:
            colors = list(im.getdata())

        s_v = time.time()
        primary_colors = cluster.k_means(colors, numColors)
        print("k_means: {} secs".format(time.time() - s_v))

        primary = []
        for color in primary_colors:
            color = list(color)
            color = tuple([int(i) for i in color])
            primary.append(color)

        palleteImage = vertical_image(primary, im.size)
        combinedImage = combine_images(palleteImage, im, im.size)
        combinedImage.save("{}{}_palette.png".format(img_Dir, orig_image.split('.')[0]))

if __name__ == "__main__":
    main()
