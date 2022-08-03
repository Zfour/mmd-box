import json
import os
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from PyQt5.QtCore import QThread,pyqtSignal
import run
import design
import json
from functools import partial
import webbrowser
import requests

class MyMainForm(QMainWindow, design.Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 实例化线程对象
        self.work = WorkThread()
        self.label.setStyleSheet("color:red")
        open_info(self)
        self.pushButton.clicked.connect(partial(start_sever, self))
        self.pushButton_2.clicked.connect(partial(end_sever, self))
        self.pushButton.clicked.connect(self.execute)
        self.pushButton_3.clicked.connect(self.open_website)
        self.pushButton_4.clicked.connect(self.open_path)
        self.pushButton_5.clicked.connect(self.push_once)
        self.pushButton_6.clicked.connect(self.push_once_last)
        self.radioButton.clicked.connect(self.play_mode_1)
        self.radioButton_2.clicked.connect(self.play_mode_2)
        self.radioButton_3.clicked.connect(self.show_mode_1)
        self.radioButton_4.clicked.connect(self.show_mode_2)
    def execute(self):
        # 启动线程
        self.textBrowser.append('MMD-BOX服务已开启！')
        self.work.start()
    def open_website(self):
        webbrowser.open("http://127.0.0.1:5050")
    def open_path(self):
        os.startfile(os.getcwd()+'/static/video')
    def push_once(self):
        requests.get("http://127.0.0.1:5050/nextvideo")
        return self.textBrowser.append('已切换至下一个视频！')
    def push_once_last(self):
        requests.get("http://127.0.0.1:5050/lastvideo")
        return self.textBrowser.append('已切换至上一个视频！')
    def play_mode_1(self):
        requests.get("http://127.0.0.1:5050/play_mode_1")
        return self.textBrowser.append('已切换至单个视频循环！')
    def play_mode_2(self):
        requests.get("http://127.0.0.1:5050/play_mode_2")
        return self.textBrowser.append('已切换至列表视频循环！')
    def show_mode_1(self):
        requests.get("http://127.0.0.1:5050/show_mode_1")
        return self.textBrowser.append('已切换至显示UI模式！')
    def show_mode_2(self):
        requests.get("http://127.0.0.1:5050/show_mode_2")
        return self.textBrowser.append('已切换至隐藏UI模式！')
class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()

    def run(self):
        #重写线程执行的run函数
        #触发自定义信号
        run.start()



def start_sever(ui):
    ui.pushButton.setEnabled(False)
    ui.pushButton_2.setEnabled(True)
    ui.label.setText("服务运行中")
    ui.label.setStyleSheet("color:green")
    webbrowser.open("http://127.0.0.1:5050")

def end_sever(ui):
    ui.textBrowser.append('MMD-BOX服务已关闭！')
    ui.pushButton.setEnabled(True)
    ui.pushButton_2.setEnabled(False)
    ui.label.setText("服务未运行")
    ui.label.setStyleSheet("color:red")
    sys.exit(app.exec_())


def open_info(ui):
    try:
        with open("static/config.json", "r", encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
            if load_dict["current_show_mode"]==1:
                ui.radioButton.setChecked(1)
            elif load_dict["current_show_mode"]==2:
                ui.radioButton_2.setChecked(1)
            if load_dict["play_mode"] == 1:
                ui.radioButton_3.setChecked(1)
            elif load_dict["play_mode"] == 2:
                ui.radioButton_4.setChecked(1)
    except:
        with open("static/config.json", "w", encoding='utf-8') as w_f:
            result = {"current_video_src": "./static/video/1.mp4", "current_show_mode": 1, "play_mode": 1}
            ui.radioButton.setChecked(1)
            ui.radioButton_3.setChecked(1)
            w_dict = w_f.write(json.dumps(result))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyMainForm()
    MainWindow.show()
    sys.exit(app.exec_())


