#!/usr/bin/env python3

# import webview
# webview.create_window('AQM', 'http://127.0.0.1/aqmmaster',frameless=True,fullscreen=True)
# webview.start()
import sys
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
web = QWebEngineView()
web.load(QUrl("http://127.0.0.1/aqmmaster/"))
web.show()
sys.exit(app.exec_())