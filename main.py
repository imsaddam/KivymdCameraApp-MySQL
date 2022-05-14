from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import time

import db as DB

Builder.load_file("frontend.kv")


class HomePage(MDScreen):
    pass

class CameraScreen(MDScreen):
    def capture(self):
        images = []
        for i in range(5):
            current_time = time.strftime('%Y%m%d-%H%M%S')
            self.filepath= f"files/{current_time}-{i}.png"
            self.ids.camera.export_to_png(self.filepath)
            images.append(self.filepath)

        DB.save_images(images)

    def change_cam(self):
        cam = self.ids.camera
        if cam.index == 0:
            cam.index = int(cam.index) + 1
        elif cam.index == 1:
            cam.index = int(cam.index) - 1
        else:
            cam.index = cam.index


class ImageScreen(MDScreen):
    def showImage(self):
        image_path = MDApp.get_running_app().root.ids.camera_screen.filepath
        print(image_path)


class RootWidget(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return RootWidget()


MainApp().run()
