#!/usr/bin/env python3

# import webview
# webview.create_window('AQM', 'http://127.0.0.1/aqmmaster',frameless=True,fullscreen=True)
# webview.start()

from PyQt5 import QtWebEngineWidgets, QtWidgets, QtCore

class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QtWebEngineWidgets.QWebEnginePage.__init__(self, *args, **kwargs)
        self.profile().downloadRequested.connect(self.on_downloadRequested)

    @QtCore.pyqtSlot(QtWebEngineWidgets.QWebEngineDownloadItem)
    def on_downloadRequested(self, download):
        old_path = download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.view(), "Save File", old_path, "*."+suffix)
        if path:
            download.setPath(path)
            download.accept()
            
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    view = QtWebEngineWidgets.QWebEngineView()
    view.settings().webSettings.setAttribute(QWebEngineSettings.JavascriptEnabl‌​ed, True)
    # view.page().fullScreenRequested.connect(QWebEngineFullScreenReq‌​uest.accept) 
    page = WebEnginePage(view)
    view.setPage(page)
    view.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    view.load(QtCore.QUrl("http://127.0.0.1/aqmmaster"))
    view.showMaximized()
    sys.exit(app.exec_())

