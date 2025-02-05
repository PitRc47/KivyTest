from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.audio import SoundLoader
def toDowngradeAPI():
    global mixer
    
    if checksys.main != 'Android':
        from os import environ; environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
        from pygame import mixer as _mixer
        _mixer.Sound
        
        _mixer.init()
        mixer = _mixer
        
        length = -1
        _load = mixer.music.load
        _get_pos = mixer.music.get_pos
        
        def _loadhook(fn: str):
            nonlocal length
            
            length = _mixer.Sound(fn).get_length()
            _load(fn)
            
        mixer.music.load = _loadhook
        mixer.music.get_length = lambda: length
        mixer.music.get_pos = lambda: _get_pos() / 1000

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
        toDowngradeAPI()
        return MusicGameWidget()

if __name__ == '__main__':
    MusicGameApp().run()