# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, QFile, QIODevice
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
import sys, os
from Ui_video_edit import Ui_MainWindow
import qdarkstyle, app_rc


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.update_ui(self)

        self.__ffmpeg = r"ffmpeg.exe"

        self.actions()
        

    def update_ui(self, MainWindow):
        MainWindow.setWindowTitle("Video Edit")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/pic/source/title.ico"))
        MainWindow.setWindowIcon(icon)

    def actions(self):
        self.btn_video.clicked.connect(lambda: self.select_files(self.lineEdit_video))
        self.btn_no_audio.clicked.connect(lambda: self.filter_video("audio", self.lineEdit_video.text()))
        self.btn_no_video.clicked.connect(lambda: self.filter_video("video", self.lineEdit_video.text()))

    def select_files(self, line_edit):
        # 添加filter是防止前面加上参数".",导致第2次加载文件夹时，又回到起点
        files = QFileDialog.getOpenFileName(self, 'Select file', filter = "Video files (*.mp4 *.mov *.avi *.ts)")
        if files:
            file_string = str(files[0])
            if file_string: # 防止没有选择文件而清空之前的文件名
                # 将文件名写到框内 
                line_edit.setText(file_string) 

    def set_command_line(self, remove_type, video_file):
        command_list = [self.__ffmpeg, "-i", video_file]
        if remove_type == "audio":
            command_list.append("-an")
            command_list.append(self.modify_video_name(video_file))
            command_list.insert(3, "-vcodec copy")
        elif remove_type == "video":
            command_list.append("-vn")
            audio_name = self.replace_suffix(video_file, ".mp3")
            command_list.append(audio_name)
        command_line = " ".join(command_list)
        print(command_line)
        return(command_line)

    def modify_video_name(self, video_string):
        name_list = video_string.split("/")
        name_list[-1] = "mute_"+name_list[-1]
        new_video_string = ("/").join(name_list)
        return(new_video_string)

    def replace_suffix(self, text, new_suffix):
        suffix = "." + text.split(".")[-1]
        file_name = text.replace(suffix, new_suffix)
        return(file_name)


    def filter_video(self, remove_type, video_file):
        os.system(self.set_command_line(remove_type, video_file))


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    my_win = MainWindow()

    style_file = QFile(':/qss/style.qss')
    style_file.open(QIODevice.ReadOnly)
    my_win.setStyleSheet(((style_file.readAll()).data()).decode("latin1"))

    my_win.show()
    sys.exit(app.exec_())