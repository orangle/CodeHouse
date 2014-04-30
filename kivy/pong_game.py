# -*- coding: utf-8 -*-
#pong_game.py   python2.7.x
#orangleliu@gmail.com    2014-04-30
'''
编写一个乒乓球的小应用
'''

from kivy.app  import App
from kivy.uix.widget import Widget

class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()


