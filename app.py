#coding=utf-8
# barton.li@primerobotics.com
# 2023/12/15
# learn

import threading, time
# from tkinter import Tk

import os
import pystray
from PIL import Image
from pystray import MenuItem
import iciba
from playsound import playsound

class App(object):
    data = []
    waiting_stray = 8
    running = True
    current = 0
    conf_name = 'config.txt'

    def __init__(self):
        menu = (MenuItem(text='暂停', action=self.on_stop),
            MenuItem(text='恢复', action=self.on_recover),
            MenuItem(text='退出', action=self.on_exit),
        )

        image = Image.open("static/eng.png")
        self.icon = pystray.Icon("BtLearn", image,  "iciba单词", menu)
        if os.path.exists(self.conf_name):
            with open(self.conf_name, 'r') as f:
                self.current = int(f.readline())
        pass

    def run(self, course):
        html = iciba.IcibaHtml()
        self.data = html.loadClass(course)
        threading.Thread(target=self.loop, daemon=True).start()
        self.icon.run()

    def play(self, audio: str):
        try:
            audio = audio.replace("\n", "")
            import requests
            sound_bytes = requests.get(url=audio).content
            name = 'x.mp3'
            with open(name, 'wb') as f:
                f.write(sound_bytes)
            playsound(name)
            os.remove(name)
        except Exception as e:
            print('error play sound')
            pass
        pass

    def loop(self):
        while True:
            if self.current == len(self.data):
                self.current = 0
            if not self.running:
                time.sleep(1)
                continue
            
            val = self.data[self.current]
            print(val)
            self.icon.remove_notification()
            self.icon.notify(val[1], val[0])
            self.play(val[2])
            self.current = self.current + 1
            # 声音
            time.sleep(self.waiting_stray)
            pass
        pass

    def on_exit(self):
        with open(self.conf_name, 'w') as f:
            f.write(str(self.current))
        self.icon.stop()
        # win.destroy()

    def on_stop(self):
        self.running = False
        print('stop ....')

    def on_recover(self):
        self.running = True
        print('recover ....')
    pass


if __name__ == '__main__':
    app = App()
    app.run(16)
    pass


# win = Tk()
# win.geometry("500x300+200+200")
# # 设置窗口属性
# win.overrideredirect(1)
# win.attributes('-alpha', 0.5)
# win.attributes("-transparent", "blue")
# # 重新定义点击关闭按钮的处理
# win.protocol('WM_DELETE_WINDOW', on_exit)

# threading.Thread(target=icon.run, daemon=True).start()
# win.mainloop()

