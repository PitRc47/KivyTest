from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader

class MusicGameWidget(Widget):
    def __init__(self, **kwargs):
        super(MusicGameWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)  # 设置白色背景
            self.rect = Rectangle(size=self.size, pos=self.pos)
        

    def on_size(self, *args):
        self.rect.size = self.size

class MusicGameApp(App):
    def build(self):
        return MusicGameWidget()

if __name__ == '__main__':
    MusicGameApp().run()