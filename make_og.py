from PIL import Image, ImageDraw, ImageFont
import os

SRC  = r"C:\Users\User\Desktop\Дизайнер Владимир Кандинский\portrait.avif"
OUT  = r"C:\Users\User\Desktop\Дизайнер Владимир Кандинский\og-image.jpg"

OG_W, OG_H = 1200, 630

# Hero page background = --paper: #f3efe7
PAPER = (243, 239, 231)
INK   = (13,  13,  13)
RED   = (230, 50,  31)
MUTE  = (90,  85,  77)

# --- open & smart-crop portrait ---
img = Image.open(SRC).convert("RGB")
iw, ih = img.size

# scale so height fills OG_H
scale = OG_H / ih
nw = int(iw * scale)
img = img.resize((nw, OG_H), Image.LANCZOS)

# paste onto paper canvas (hero background)
canvas = Image.new("RGB", (OG_W, OG_H), PAPER)
x_offset = OG_W - nw   # align portrait to the right
canvas.paste(img, (x_offset, 0))
img = canvas

# --- paper gradient: left side for text (paper → transparent) ---
overlay = Image.new("RGBA", (OG_W, OG_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

grad_width = 680
for x in range(grad_width):
    alpha = int(255 * (1 - x / grad_width))
    draw.line([(x, 0), (x, OG_H)], fill=(*PAPER, alpha))

# subtle paper strip at bottom for text legibility
draw.rectangle([(0, OG_H - 80), (600, OG_H)], fill=(*PAPER, 230))

img = img.convert("RGBA")
img = Image.alpha_composite(img, overlay)
img = img.convert("RGB")

# --- text ---
draw = ImageDraw.Draw(img)

def try_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_bold = try_font("C:/Windows/Fonts/arialbd.ttf", 72)
font_sub  = try_font("C:/Windows/Fonts/arial.ttf",   22)
font_mono = try_font("C:/Windows/Fonts/cour.ttf",    16)
font_badge = try_font("C:/Windows/Fonts/arialbd.ttf", 20)

# Red vertical accent bar
draw.rectangle([(52, 58), (60, 220)], fill=RED)

# Main name — dark ink on paper bg
draw.text((80, 54),  "ВЛАДИМИР",   font=font_bold, fill=INK)
draw.text((80, 136), "КАНДИНСКИЙ", font=font_bold, fill=INK)

# Subtitle
draw.text((80, 228), "Цифровой художник  ·  BVG AI  ·  New York", font=font_sub, fill=MUTE)

# Thin red rule under subtitle
draw.rectangle([(80, 262), (420, 265)], fill=RED)

# Bottom left — domain
draw.text((52, OG_H - 52), "v-kandinskiy.ru", font=font_mono, fill=MUTE)

# Bottom right — BVG AI badge
bx = OG_W - 180
draw.rectangle([(bx, OG_H - 68), (bx + 128, OG_H - 36)], fill=RED)
draw.text((bx + 12, OG_H - 62), "BVG AI", font=font_badge, fill=PAPER)

img.save(OUT, "JPEG", quality=93, optimize=True)
print("Saved: " + str(os.path.getsize(OUT)//1024) + " KB")
