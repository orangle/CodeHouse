# coding:utf-8
'''
生成文字类图片

orangleliu@gmail.com
'''

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance

def word_pic():
    img = Image.new('RGB', (200, 100))
    draw = ImageDraw.Draw(img)
    # want words bigger
    draw.text((30,30), "failure", (255,255,255))
    img.save('w.png')


if __name__ == "__main__":
    word_pic()
