# -*- coding: utf-8 -*-
#basic.py   python2.7.x
#orangleliu@gmail.com    2014-04-30
'''
kivy 基本使用方法
'''

import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):

    def  __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols =2
        self.add_widget(Label(text=u"Username: "))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text=u'Password:'))
        self.password = TextInput(password=True, multilne=False)
        self.add_widget(self.password)

class MyApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
