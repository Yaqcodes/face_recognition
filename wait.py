# PROGRAM TO GENERATE WAIT SCREEN IMAGE USING NCAIR LOGO

from PIL import Image, ImageDraw, ImageFont
import os


# Get waiting screen image
wait_image = Image.open(os.path.join(os.getcwd(), "img/ncair.jpg"))

# Create a ImageDraw instance
draw = ImageDraw.Draw(wait_image)

# specified font size
font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 30)
white = (255, 255, 255)
message = 'Press any key...'
draw.text((100, 30), message, font=font, fill=white, align='right')
wait_image.save('img/wait_image.jpg')
wait_image.show()
