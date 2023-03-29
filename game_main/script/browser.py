import webview
import pygame

class Browser:
    def __init__(self, url, title) -> None:
        self.url = url
        self.title = title
        self.window = None
        self.succeded = False

    def show_browser(self):
        self.window = webview.create_window(self.title, self.url, fullscreen=True, js_api=self)
        
        webview.start()       
    
    def close_window(self):
        self.window.destroy()


# appel de "pythonFunction" dans JS
# window.pywebview.api.pythonFunction("arg");
