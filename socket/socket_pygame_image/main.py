# Import 'kivy.core.text' must be called in entry point script
# before import of cv2 to initialize Kivy's text provider.
# This fixes crash on app exit.
from kivy.properties import ObjectProperty
import kivy.core.text
# import cv2
from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import os
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import threading,time
from net.Sever import senddata

# 维护全局变量
import PARAM
# change code
import pygame.camera
import pygame.image

class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None
        self.clock_event = None
    def start(self, capture, fps=30):
        self.capture = capture
        self.clock_event = Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule(self.clock_event)
        if self.capture != None:
            self.capture.release()

    def update(self, dt): 
        frame = self.capture.get_image()
        # 转化为字符串

        frame = pygame.image.tostring(frame, 'RGB')
        # 判断次数到达，

        if PARAM.TIMES_ENTER_UPDATE ==  PARAM.TIME_TO_SAVE_PIC:
            # 如果 为BMP_FLAG为0 ，表示通信传输完成，此时更新图片
            if PARAM.BMP_FLAG == 0:
                # pygame.image.save(frame, PARAM.FILENAME)
                # 将数据给frame
                PARAM.IMAGE_STORE = frame
                PARAM.BMP_FLAG = 1
                PARAM.TIMES_ENTER_UPDATE = 0
            # 只得重新计数
            else:
                PARAM.TIMES_ENTER_UPDATE = 0
            # print('saved')
        # 否则， ++次数

        PARAM.TIMES_ENTER_UPDATE += 1
        # print(PARAM.TIMES_ENTER_UPDATE)
        # print(frame)
        #print()

        texture = self.texture
        self.texture = texture = Texture.create(size=PARAM.IMAGE_SIZE)
        texture.flip_vertical()
        texture.blit_buffer(frame)
        self.canvas.ask_update()




class QrtestHome(BoxLayout):
    capture = None
    recog_name = ObjectProperty()
    # def change_racob_name(self, name_):
    #     self.recog_name

    def dostart(self, *largs):
        # self.capture = cv2.VideoCapture(0)
        # self.capture.set(3, 320)
        # self.capture.set(4, 240)
        pygame.camera.init()

        cameras = pygame.camera.list_cameras()
        print(len(cameras))
        # print("Using camera %s ..." % cameras[0])
        # SIZE = (320, 240)
        webcam = pygame.camera.Camera(cameras[0], PARAM.IMAGE_SIZE)

        webcam.start()
        self.capture = webcam
        self.ids.qrcam.start(self.capture)



class FaceApp(App):
    homeWin = None
    def build(self):
        #Window.clearcolor = (.4,.4,.4,1)
        Window.size = (800, 600)
        self.homeWin = QrtestHome()
        # homeWin.init_()

        # 把线程放在这里
        t = threading.Thread(target = senddata)
        t.start()
        return self.homeWin
    
    def on_start(self):
        self.homeWin.dostart()

if __name__ == '__main__':
    FaceApp().run()
