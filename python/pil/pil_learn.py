# -*- encoding=utf-8 -*-
'''
author: orangleliu
pil处理图片，验证，处理
大小，格式 过滤
压缩，截图，转换
'''

#图片的基本参数获取
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance

def compress_image(img, w=128, h=128):
    img.thumbnail((w,h))
    im.save('test1.png', 'PNG')
    print u'成功保存为png格式, 压缩为128*128格式图片'

def cut_image(img):
    '''
    截图, 旋转，再粘贴
    '''
    #eft, upper, right, lower
    #x y z w  x,y 是起点， z,w是偏移值
    width, height = img.size
    box = (width-200, height-100, width, height)
    region = img.crop(box)
    #旋转角度
    region = region.transpose(Image.ROTATE_180)
    img.paste(region, box)
    img.save('test2.jpg', 'JPEG')
    print u'重新拼图成功'


def equal_ratio_compress_image(img, ratio=0.8):
    '''
    对图片的等比压缩
    '''
    pass 


def logo_watermark(img, logo_path):
    '''
    添加一个图片水印,原理就是合并图层，用png比较好
    '''
    baseim = img
    logoim = Image.open(logo_path) 
    bw, bh = baseim.size
    lw, lh = logoim.size
    baseim.paste(logoim, (bw-lw, bh-lh))
    baseim.save('test3.jpe', 'JPEG')
    print u'logo水印组合成功'
    
def text_watermark(img, text, out_file="test4.jpg", angle=23, opacity=0.25):
    '''
    添加一个文字水印，做成透明水印的模样，应该是png图层合并
    http://www.pythoncentral.io/watermark-images-python-2x/
    这里会产生著名的 ImportError("The _imagingft C module is not installed") 错误
    Pillow通过安装来解决 pip install Pillow
    '''
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    FONT = "msyh.ttf"
    size = 2
    
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while (n_width+n_height < watermark.size[0]):
        size += 2
        n_font = ImageFont.truetype(FONT, size=size)
        n_width, n_height = n_font.getsize(text)    
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font, fill="#ff00ff")    
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
    print u"文字水印成功"

#常用的方法
# img.show() 显示图片
# crop 截图
# paste()
# merge()
if __name__ == "__main__":
    im = Image.open('test.jpg')  #image 对象
    print im.format, im.size, im.mode
    #cut_image(im)
    #cut_image(im)
    #logo_watermark(im, 'logo.png')
    text_watermark(im, 'Orangleliu')
