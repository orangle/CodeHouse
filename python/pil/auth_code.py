# -*- encoding=utf-8 -*-
'''
author: orangleliu
date: 2015-02-06

生成验证码
图片库最好用Pillow
参考：
http://codingnow.cn/language/627.html 
https://github.com/EchoMemory/Projects/blob/master/Python/CAPTCHA/Verification%20Code%20Generator.py

'''

import random

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
except ImportError:
    import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

#数字，字母 4位的验证码
base=('0','1','2','3','4','5','6','7','8','9',  
      'A','B','C','D','E','F','G','H','I','J',  
      'K','L','M','N','O','P','Q','R','S','T',  
      'U','V','W','X','Y','Z') 

chars = ''.join(map(str, base))

def create_validate_code(size=(120, 30), chars=chars, mode="RGB", \
                         bg_color=(255, 255, 255), fg_color=(255, 0, 0), \
                         font_size=18, font_type="msyh.ttf", \
                         length=4, draw_points=True, point_chance = 2): 
    '''
    size: 图片的大小，格式（宽，高），默认为(120, 30)
    chars: 允许的字符集合，格式字符串
    mode: 图片模式，默认为RGB
    bg_color: 背景颜色，默认为白色
    fg_color: 前景色，验证码字符颜色
    font_size: 验证码字体大小
    font_type: 验证码字体，需要指定一个字体文件的路径
    length: 验证码字符个数
    draw_points: 是否画干扰点
    point_chance: 干扰点出现的概率，大小范围[0, 50]
    ''' 

    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)
 
    '''随机取出指定个数符串'''
    get_chars = lambda : random.sample(chars, length) 
 
    def create_points(): 
        '''绘制干扰点，遍历这个图片的所有点，根据概率决定时候加黑点点''' 
        chance = min(50, max(0, int(point_chance))) # 大小限制在[0, 50] 
 
        for w in xrange(width): 
            for h in xrange(height): 
                tmp = random.randint(0, 50) 
                if tmp > 50 - chance: 
                    draw.point((w, h), fill=(0, 0, 0))
 
    def create_strs():
        '''绘制验证码字符，验证码的主体''' 
        c_chars = get_chars() 
        strs = '%s' % ''.join(c_chars) 
 
        font = ImageFont.truetype(font_type, font_size) 
        font_width, font_height = font.getsize(strs) 
        
        #起码的一组参数是位置
        draw.text(((width - font_width) / 3, (height - font_height) / 4), 
                    strs, font=font, fill=fg_color) 
        return strs 
 
    if draw_points: 
        create_points()
    strs = create_strs() 
 
    #图形扭曲参数 
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 
              1 - float(random.randint(1, 10)) / 100, 
              float(random.randint(1, 2)) / 500, 0.001, 
              float(random.randint(1, 2)) / 500 ]

    img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大） 
    print strs 
    img.save("code1.jpg", "JPEG", quality=85)
 
if __name__ == "__main__":
    create_validate_code()