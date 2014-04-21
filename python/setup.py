# -*- coding: utf-8 -*-
#setup.py   python2.7.x
#orangleliu   2014-04-21
'''
distutils 模块的简单使用，用来对模块进行打包
常用的命令：
python setup.py build
python setup.py clean
python setup.py install
python setup.py sdist  zip或者是tar包
python setup.py bdist_wininst /bdist_rpm 在windows平台上可以生成一个可执行包.exe
python setup.py bdist --help-format  可以看到所有打包格式


sdist可以创建一个存档文件
'''

from os.path import join
from distutils.core import setup
from distutils.core import Command
import os

class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        self._clean_me = []
        for root, dirs, files in os.walk('.'):
            for  f in files:
                if f.endswith('.pyc'):
                    self._clean_me.append(join(root, f))

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.remove(clean_me)
            except:
                print 'remove %s falure'%clean_me
                pass


setup(
    name = 'orangleliu',
    version = '1.00',
    description = "This is orangleliu's modules",

    author = 'Orangleliu',
    author_email = 'orangleliu@gmail.com',
    url = '',
    license = 'BSD',

    packages = ['oop'],   #需要有__init__.py 的包，文件夹的配置
    package_dir = {},   #没有__init__.py的文件夹使用这个配置
    py_modules = '',  #单个文件的配置
    data_files = '',

    cmdclass = {'clean': CleanCommand}
)

