from PIL import Image, ImageFont, ImageDraw
import os
# Global Variables
FONT_FILE_1 = ImageFont.truetype(r'fonts/Times New Roman Bold.ttf', 30)
FONT_FILE_2 = ImageFont.truetype(r'fonts/Times New Roman Bold.ttf', 14)
FONT_COLOR_1 = "#5E17EB"
FONT_COLOR_2 = "#0E477D"

template = Image.open(r'src/Sertifikat.png')
WIDTH, HEIGHT = template.size

MAX_WIDTH = WIDTH - 80  # Ikkinchi matn uchun maksimal eni
MAX_WORDS_PER_LINE = 8  # Har bir qatorda maksimal so'z soni

def make_certificates(name, second_text):
    
    draw = ImageDraw.Draw(template)

    # Birinchi matnning eni va balandligini topish
    bbox_1 = FONT_FILE_1.getbbox(name)
    text_width_1 = bbox_1[2] - bbox_1[0]
    text_height_1 = bbox_1[3] - bbox_1[1]

    # Birinchi matnni markazga joylashtirish
    draw.text(((WIDTH - text_width_1) / 2 - 40, (HEIGHT - text_height_1) / 2 + 40), name, fill=FONT_COLOR_1, font=FONT_FILE_1)

    # Ikkinchi matnni bir necha qatorga bo'lish
    words = second_text.split()
    lines = []
    line = []
    for word in words:
        if len(line) >= MAX_WORDS_PER_LINE:
            lines.append(' '.join(line))
            line = []
        line.append(word)
    if line:
        lines.append(' '.join(line))

    y = (HEIGHT - text_height_1) / 2 + 55 + text_height_1 + 10

    for line in lines:
        bbox_2 = FONT_FILE_2.getbbox(line)
        text_width_2 = bbox_2[2] - bbox_2[0]
        text_height_2 = bbox_2[3] - bbox_2[1]
        draw.text(((WIDTH - text_width_2) / 2 - 40, y), line, fill=FONT_COLOR_2, font=FONT_FILE_2)
        y += text_height_2 + 5  # Qatorlar orasidagi masofani oshirish

    # Sertifikatlarni boshqa katalogga saqlash
    directory = "out"
    if not os.path.exists(directory):
        os.makedirs(directory)
    template.save("./out/" + name + ".png")