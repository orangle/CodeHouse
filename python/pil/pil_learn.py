# -*- encoding=utf-8 -*-
'''
author: orangleliu

pil处理图片，验证，处理
大小，格式 过滤
压缩，截图，转换
'''

#图片的基本参数获取
try:
    from PIL import Image
except ImportError:
    import Image

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
    box = (1000, 1000, 1000+200, 1000+600)
    region = img.crop(box)
    #旋转角度
    region = region.transpose(Image.ROTATE_180)
    img.paste(region, box)
    img.save('test2.jpg', 'JPEG')
    print u'重新拼图成功'

#常用的方法
# img.show() 显示图片
# crop 截图
# paste()
# merge()
if __name__ == "__main__":
    im = Image.open('test.jpg')  #image 对象
    print im.format, im.size, im.mode
    #cut_image(im)
    cut_image(im)





