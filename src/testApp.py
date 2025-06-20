import os

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
import time


class Interface(GridLayout):

    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.cols = 2

        startButton = Button(text='Start')
        startButton.bind(on_press=self.start)
        self.add_widget(startButton)

        self.item_list = []
        self.text_box = TextInput(
            readonly=True,
            font_size=16,
            size_hint=(1, 1)
        )
        self.add_widget(self.text_box)

        self.URLtext = TextInput(multiline=False)
        self.add_widget(self.URLtext)

        addButton = Button(text='Add')
        addButton.bind(on_press=self.addURL)
        self.add_widget(addButton)
    
    def addURL(self, instance):
        url = self.URLtext.text
        if url:
            print(f"URL added: {url}")
            self.URLtext.text = ''
            self.item_list.append(url)
            self.update_text_box()

    def update_text_box(self):
        self.text_box.text = '\n'.join(f"{item}" for item in self.item_list)

    def start(self, instance):
        if len(self.item_list) == 0:
            Logger.error("YTAudioDownloader: No URLs to process.")
            return

        for url in self.item_list[:]:
            Logger.info(f"YTAudioDownloader: Processing URL: {url}")
            # Here you would call the actual download function
            # For example: download_audio(url)
            print(url)
            time.sleep(1)
            self.item_list.remove(url)
            time.sleep(1)
            print(self.item_list)
            self.update_text_box()
            time.sleep(1)
        
        Logger.info("YTAudioDownloader: All URLs processed.")


class YTAudioDownloader(App):

    def build(self):
        return Interface()


if __name__ == '__main__':
    YTAudioDownloader().run()