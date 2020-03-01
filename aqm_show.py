#!/usr/bin/env python3

# import webview
# webview.create_window('AQM', 'http://127.0.0.1/aqmmaster',frameless=True,fullscreen=True)
# webview.start()
import sys 
from PyQt5 import QtWidgets, QtGui, QtCore 
from PyQt5.QtWebEngineWidgets import * 

app=QtWidgets.QApplication(sys.argv) 
w=QWebEngineView() 
w.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
w.settings().setAttribute(QWebEngineSettings.JavascriptEnabl‌​ed, True) 
w.settings().setAttribute(QWebEngineSettings.FullScreenSuppo‌​rtEnabled, True)
w.page().fullScreenRequested.connect(QWebEngineFullScreenReq‌​uest.accept) 
w.load(QtCore.QUrl('http://127.0.0.1/aqmmaster'))

w.showMaximized() 
app.exec_()