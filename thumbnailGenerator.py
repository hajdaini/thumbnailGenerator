from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap, argparse, os, math
from slugify import slugify

TEXT_SIZE = 62

parser = argparse.ArgumentParser(description='Create thumbnail automatically')
parser.add_argument('--text', '-t', help='text to display in your image')
parser.add_argument('--size', '-s', type=int, help='size of the text that will be display')
parser.add_argument('--offsetY', '-y', type=int, help='Offset in y position of the text')
parser.add_argument('--file', '-f', help='Select text line by line from a file')
args = parser.parse_args() 

def addTitle(background, text, fontSize, textColor, borderColor, offset = 0):
    bW, bH = background.size
    draw = ImageDraw.Draw(background)
    tW, tH = draw.textsize(text)
    font = ImageFont.truetype("./fonts/ObelixProB-cyr.ttf", fontSize)

    xPos = (bW//5)*2  # 2/5 width of background
    newLineCount = len(textwrap.wrap(text, width=15))

    index = 0
    newLineHeight = 17
    for line in textwrap.wrap(text, width=15):
        yPos = getTextWrapPosition(newLineCount, bH, offset, tH)
        if index > 0:
            yPos += index * newLineHeight
        index += 1 
        borderText(2.7, borderColor, draw,  xPos, yPos, line, font)
        draw.text((xPos, yPos), line, font=font, fill=textColor)
        offset += font.getsize(line)[1]


def getTextWrapPosition(newLineCount, bH, offset, textHight):
    if newLineCount >= 5:
        yPos = bH//7  + offset
    elif newLineCount == 4:
        yPos = bH//5  + offset
    elif newLineCount == 3 :
        yPos = bH//3  + offset
    elif newLineCount == 2 :
        yPos = bH//3  + offset
    else :
        # yPos = bH//2 + textHight*4 + offset
        yPos = bH//2 + offset
    return yPos


def borderText(borderSize, color, draw, xPos, yPos, text, font):
    # thin border
    draw.text((xPos-borderSize, yPos), text, font=font, fill=color)
    draw.text((xPos+borderSize, yPos), text, font=font, fill=color)
    draw.text((xPos, yPos-borderSize), text, font=font, fill=color)
    draw.text((xPos, yPos+borderSize), text, font=font, fill=color)

    # thicker border
    draw.text((xPos-borderSize, yPos-borderSize), text, font=font, fill=color)
    draw.text((xPos+borderSize, yPos-borderSize), text, font=font, fill=color)
    draw.text((xPos-borderSize, yPos+borderSize), text, font=font, fill=color)
    draw.text((xPos+borderSize, yPos+borderSize), text, font=font, fill=color)

def addMascot(background, img, sizeMultiplier):
    W, H = background.size
    img_w, img_h = img.size
    img = img.resize((round(img_w * sizeMultiplier), round(img_h * sizeMultiplier)), Image.ANTIALIAS)
    img_w, img_h = img.size
    background.paste(img, ( (W//5) - (img_w // 2), (H - img_h) // 2 ), mask=img) # 1/5 width and 1/2 height of background size

def addBackgroundImage(background, img, sizeMultiplier):
    W, H = background.size
    img_w, img_h = img.size
    img = img.resize((round(img_w * sizeMultiplier), round(img_h * sizeMultiplier)), Image.ANTIALIAS)
    img_w, img_h = img.size
    background.paste(img, ( 0, 0 ), mask=img) # 1/5 width and 1/2 height of background size


def addDecors(background, sizeMultiplier):
    imgs = [Image.open("decors/decor.png", "r"), Image.open("decors/decor2.png", "r")]
    for index, img in enumerate(imgs):
        img = img.convert("RGBA")
        W, H = background.size
        img_w, img_h = img.size
        img = img.resize((round(img_w * sizeMultiplier), round(img_h * sizeMultiplier)), Image.ANTIALIAS)
        img = img.filter((ImageFilter.GaussianBlur (radius=30)))
        img_w, img_h = img.size
        if index == 0:
            background.paste(img, (200, 0 ), mask=img) # 1/5 width and 1/2 height of background size
            background.paste(img, (700, 0 ), mask=img) # 1/5 width and 1/2 height of background size
        else:
            background.paste(img, (0, 0 ), mask=img) # 1/5 width and 1/2 height of background size

def addCredit(background):
    bW, bH = background.size
    credit = "devopssec.fr"
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("./fonts/Circus Of Innocents.ttf", 50)
    tW, tH = font.getsize(credit)
    offset = 12
    xPos, yPos = (bW - tW - offset, bH - tH - offset)
    borderText(2, (211, 208, 245), draw, xPos, yPos, credit, font)
    draw.text( (xPos, yPos), credit, font=font, fill=(102, 98, 148))


def get_pixel(image, i, j):
    # Inside image bounds?
    W, H = image.size
    if i > W  or j > H:
        return None
    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def get_max_value_color(value):
    if value > 255:
        return 255
    return int(value)

def addFilter(background, type="B", amount = 5):
    bW, bH = background.size
    pixel_data = background.load()
    colors = list(background.getdata())
    for x in range(bW):
        for y in range(bH):
            c = colors[x * y]
            if type ==  "R":
                pixel_data[x, y] = (get_max_value_color(c[0]) + amount, c[1], c[2])
            elif type ==  "V":
                pixel_data[x, y] = (c[0], get_max_value_color(c[1]) + amount, c[2])
            elif type ==  "B":
                pixel_data[x, y] = (c[0], c[1], get_max_value_color(c[2]) + amount)

def addLogo(background):
    bW, bH = background.size
    logo = Image.open('logo.png', 'r')
    iW, iH = logo.size
    logo = logo.resize((55, 55), Image.ANTIALIAS)
    iW, iH = logo.size
    xPos, yPos = (10, bH - iH - 10)
    background.paste(logo, ( xPos, yPos ), mask=logo) # 1/5 width and 1/2 height of background size


def gradientBackground(background, innerColor, outerColor):
    bW, bH = background.size
    for y in range(bH):
        for x in range(bW):
            #Find the distance to the center
            distanceToCenter = math.sqrt((x -bW/2) ** 2 + (y - bH/2) ** 2)

            #Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * bW/2)

            #Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

            #Place the pixel        
            background.putpixel((x, y), (int(r), int(g), int(b)))

textList, textSave = [], []

if args.file:
    with open(args.file) as f:
        textList = f.readlines()
        textSave = textList
else:
    if args.text:
        textList.append(args.text)
        textSave = textList
    else:
        textList =(
            "My beautiful text 1",
            "My beautiful text 2",
        )

        textSave = (
            "My beautiful text part 1",
            "My beautiful text part 2",
        )
        # print("use -t or -f")
        # exit(0)


def cleanText(text):
    return text.replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('œ', 'oe')


def createBgImage(bgColor, textColor, borderColor, text):
    background = Image.new('RGBA',(1200, 627) , bgColor) # linkedin recommended size
    mascot = Image.open("mascots/ansible.png", "r").convert("RGBA")
    bgImage = Image.open("bg/bg-red.jpg", "r").convert("RGBA")
    addBackgroundImage(background, bgImage, 1)
    # addFilter(background)
    background = background.filter((ImageFilter.GaussianBlur (radius=5)))
    # addDecors(background, 1)
    if args.size and args.offsetY:
        addTitle(background, text, args.size, textColor, borderColor, args.offsetY)
    elif args.size:
        addTitle(background, text, args.size, textColor, borderColor)
    else:
        addTitle(background, text, TEXT_SIZE, textColor, borderColor)
    addMascot(background, mascot, 1) # k8s
    addCredit(background)
    addLogo(background)
    return background


def saveImage(background, filename, show = False):
    if not background.mode == 'RGB':
        background = background.convert('RGB')
    try:
        path = './images/' + slugify(filename) + '.jpg'
        background.save(path, "JPEG", quality=80)
        if show is True:
            background.show()
        print("Successfully saved in '{}'".format(os.path.abspath(path)))
    except Exception as e:                
        print(e)


for idx, text in enumerate(textList):
    text = cleanText(text)
    bgColor = (245, 102, 66)
    textColor, borderColor = (255,255,255),(4, 18, 45)
    background = createBgImage(bgColor, textColor, borderColor, text)
    saveImage(background, textSave[idx], True)

    
