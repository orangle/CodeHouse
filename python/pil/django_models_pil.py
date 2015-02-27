# -*- encoding=utf-8 -*-
import os
from time import time
from tempfile import NamedTemporaryFile
try:
    from PIL import Image
except ImportError:
    import Image

from settings import MEDIA_ROOT
from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

def generate_restaurant(instance, filename):
    ext = filename.split('.')[-1]
    nname = str(int(time())) + '.' + ext
    return os.path.join("restaurant", nname)

def generate_food(instance, filename):
    ext = filename.split('.')[-1]
    nname = str(int(time())) + '.' + ext
    return os.path.join("food", nname)

class Restaurant(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(max_length=255, default='', upload_to=generate_restaurant)
    note = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=11, default='')

    def __unicode__(self):
        return self.phone

class Activity(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=40, default='')

    def __unicode__(self):
        return self.content

class Food(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, default='')
    image = models.ImageField(max_length=255, default='', upload_to=generate_food)
    small = models.ImageField(max_length=255, default='', upload_to="food")  #small 为空的时候报错！！
    price = models.IntegerField()
    discount = models.IntegerField()
    note = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        #windows 下会有问题，linxu可以正常运行

        super(Food, self).save(*args, **kwargs)
        im = Image.open(os.path.join(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size


        #im.thumbnail((200,100), Image.ANTIALIAS)    #这种方式质量损坏很大
        fn, ext = os.path.splitext(self.image.name)
        x, y, w, h = resize_image(self.width, self.height)
        box = (x,y,w+x,h+y)
        ratio = float(300) / w
        newWidth = int(w * ratio)
        newHeight = int(h * ratio)

        newIm = im.crop(box)
        im = None
        #newIm.resize((newWidth,newHeight),Image.ANTIALIAS)  #压缩图片
        print box
        print self.width, self.height

        simage_name = fn + "-s" + ext
        tf = NamedTemporaryFile(delete=True)
        newIm.save(tf.name, "JPEG", quality=95)
        self.small.save(simage_name, File(open(tf.name)), save=False)
        tf.close()
        super(Food, self).save(*args, **kwargs)


def resize_image(ori_w, ori_h, dst_w=200, dst_h=100):
    '''
    计算裁剪尺度
    '''
    dst_scale = float(dst_h) / dst_w #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比

    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        #过宽
        height = ori_h
        width = int(height*(1/dst_scale))

        x = (ori_w - width) / 2
        y = 0
    return x,y,width,height
