from jnius import autoclass, PythonJavaClass, java_method
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import json

# Java classes import
Context = autoclass('android.content.Context')
GeckoView = autoclass('org.mozilla.geckoview.GeckoView')
GeckoRuntime = autoclass('org.mozilla.geckoview.GeckoRuntime')
GeckoSession = autoclass('org.mozilla.geckoview.GeckoSession')
WebExtension = autoclass('org.mozilla.geckoview.WebExtension')
JSONObject = autoclass('org.json.JSONObject')
Toast = autoclass('android.widget.Toast')
ViewGroup = autoclass('android.view.ViewGroup')
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
Button = autoclass('android.widget.Button')

Builder.load_string('''
<GeckoViewContainer>:
    orientation: 'vertical'
''')

class PortDelegate(PythonJavaClass):
    __javainterfaces__ = ['org/mozilla/geckoview/WebExtension$PortDelegate']
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    @java_method('(Ljava/lang/Object;Lorg/mozilla/geckoview/WebExtension$Port;)V')
    def onPortMessage(self, message, port):
        try:
            if isinstance(message, JSONObject):
                action = message.getString("action")
                if action == "JSBridge":
                    data = message.getString("data")
                    self.callback(data)
        except Exception as e:
            print("Error handling message:", e)

class MessageDelegate(PythonJavaClass):
    __javainterfaces__ = ['org/mozilla/geckoview/WebExtension$MessageDelegate']
    
    def __init__(self, port_delegate):
        super().__init__()
        self.port_delegate = port_delegate
    
    @java_method('(Lorg/mozilla/geckoview/WebExtension$Port;)V')
    def onConnect(self, port):
        print("Extension connected")
        port.setDelegate(self.port_delegate)

class GeckoViewContainer(BoxLayout):
    gecko_view = ObjectProperty(None)
    button = ObjectProperty(None)
    count = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.runtime = None
        self.session = None
        self.port = None
        
        # Setup GeckoView
        context = autoclass('org.kivy.android.PythonActivity').mActivity
        self.gecko_view = GeckoView(context)
        self.add_widget(self.gecko_view)
        
        # Setup Button
        self.button = Button(context)
        self.button.setText("Test Evaluate Javascript")
        self.button.setOnClickListener(ButtonClickListener(self))
        self.add_widget(self.button)
        
        # Initialize Gecko
        self.init_gecko()
    
    def init_gecko(self):
        context = autoclass('org.kivy.android.PythonActivity').mActivity
        if not self.runtime:
            self.runtime = GeckoRuntime.create(context)
            self.runtime.getSettings().setRemoteDebuggingEnabled(True)
            self.install_extension()
        
        self.session = GeckoSession()
        self.session.open(self.runtime)
        self.gecko_view.setSession(self.session)
        self.session.loadUri("https://bing.com/")
    
    def install_extension(self):
        controller = self.runtime.getWebExtensionController()
        extension = WebExtension("resource://android/assets/messaging/", "messaging@example.com")
        
        class InstallCallback(PythonJavaClass):
            __javainterfaces__ = ['org/mozilla/geckoview/WebExtension$InstallCallback']
            
            @java_method('(Lorg/mozilla/geckoview/WebExtension;)V')
            def onSuccess(self, extension):
                print("Extension installed")
                extension.setMessageDelegate(
                    MessageDelegate(PortDelegate(self.show_toast)),
                    "browser"
                )
            
            @java_method('(Ljava/lang/Throwable;)V')
            def onError(self, error):
                print("Extension install error:", error)
        
        controller.ensureBuiltIn(extension, InstallCallback())
    
    def evaluate_javascript(self, script):
        if self.port:
            try:
                msg = JSONObject()
                msg.put("action", "evalJavascript")
                msg.put("data", script)
                msg.put("id", str(System.currentTimeMillis()))
                self.port.postMessage(msg)
            except Exception as e:
                print("Error sending message:", e)
    
    def show_toast(self, message):
        context = autoclass('org.kivy.android.PythonActivity').mActivity
        Toast.makeText(context, message, Toast.LENGTH_LONG).show()

class ButtonClickListener(PythonJavaClass):
    __javainterfaces__ = ['android/view/View$OnClickListener']
    
    def __init__(self, container):
        super().__init__()
        self.container = container
    
    @java_method('(Landroid/view/View;)V')
    def onClick(self, view):
        self.container.count += 1
        self.container.evaluate_javascript(
            f"window.appMessage('app button click {self.container.count}')"
        )

class GeckoApp(App):
    def build(self):
        return GeckoViewContainer()

if __name__ == '__main__':
    GeckoApp().run()