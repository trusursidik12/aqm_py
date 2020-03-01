#!/usr/bin/env python3

# import webview
# webview.create_window('AQM', 'http://127.0.0.1/aqmmaster',frameless=True,fullscreen=True)
# webview.start()

 
# import sys
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.QtWebKit import *
 
# app = QApplication(sys.argv)
 
# web = QWebView()
# web.load(QUrl("http://127.0.0.1/aqmmaster"))
# web.show()
 
# sys.exit(app.exec_())

import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget

# from PyQt5.QtWebKitWidgets import QWebView , QWebPage
# from PyQt5.QtWebKit import QWebSettings

from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings

from PyQt5.QtNetwork import *
import sys
from optparse import OptionParser

class MyBrowser(QWebPage):
    def userAgentForUrl(self, url):
        return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

class Browser(QWebView):
    def __init__(self):
        # QWebView
        self.view = QWebView.__init__(self)
        #self.view.setPage(MyBrowser())
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)
        #super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&amp;)"), self.adjustTitle)

    def load(self,url):
        self.setUrl(QUrl(url))
    
    def adjustTitle(self):
        self.setWindowTitle(self.title())
    
    def disableJS(self):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)

app = QApplication()
view = Browser()
view.showMaximized()
view.load("http://127.0.0.1/aqmmaster")
app.exec_()