import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 225, 800, 550)
        # 创建并设置标签
        self.class1 = QLabel('请选择场景', self)
        self.define_label(self.class1, 50, 50, 200, 70)
        self.prob1 = QLabel('请选择场景', self)
        self.define_label(self.prob1, 300, 50, 250, 70)
        self.class2 = QLabel('请选择场景', self)
        self.define_label(self.class2, 50, 170, 200, 70)
        self.prob2 = QLabel('请选择场景', self)
        self.define_label(self.prob2, 300, 170, 250, 70)
        self.class3 = QLabel('请选择场景', self)
        self.define_label(self.class3, 50, 290, 200, 70)
        self.prob3 = QLabel('请选择场景', self)
        self.define_label(self.prob3, 300, 290, 250, 70)
        # 室内音频识别按钮
        self.indoor_model = QPushButton('室内音频识别', self)
        self.define_button(self.indoor_model, 600, 150, 150, 50)
        self.indoor_model.setStyleSheet("background-color: white; color: black")
        self.indoor_model.clicked.connect(self.on_indoor_model_clicked)  # 连接信号
        # 室外音频识别按钮
        self.outdoor_model = QPushButton('室外音频识别', self)
        self.define_button(self.outdoor_model, 600, 250, 150, 50)
        self.outdoor_model.setStyleSheet("background-color: white; color: black")
        self.outdoor_model.clicked.connect(self.on_outdoor_model_clicked)  # 连接信号
        # 开始按钮
        self.start_button = QPushButton('Start', self)
        self.define_button(self.start_button, 50, 400, 300, 100)
        self.start_button.clicked.connect(self.on_start_clicked)  # 连接信号
        # 结束按钮
        self.stop_button = QPushButton('Stop', self)
        self.define_button(self.stop_button, 450, 400, 300, 100)
        self.stop_button.clicked.connect(self.on_stop_clicked)  # 连接信号
        # 用于记忆所选择的模型的布尔变量
        self.which_model = True

    def define_label(self, label, x, y, width, height):
        label.setStyleSheet("QLabel {background-color: black; color: white;}")
        label.setAlignment(Qt.AlignCenter)  # 使文本居中
        label.setStyleSheet(
            f"QLabel {{background-color: black; color: white; font-size: {int(height * 0.5)}px;}}")  # 增大字体
        label.setFixedSize(width, height)
        label.move(x, y)

    def define_button(self, button, x, y, width, height):
        button.setFixedSize(width, height)
        button.move(x, y)

    def on_indoor_model_clicked(self):
        self.indoor_model.setStyleSheet("background-color: red; color: black")  # 改变按钮背景颜色
        self.class1.setText('Footsteps:')  # 改变标签文本
        self.class2.setText('MouseClick:')
        self.class3.setText('Laughing:')
        self.prob1.setText('点击开始')
        self.prob2.setText('点击开始')
        self.prob3.setText('点击开始')
        self.which_model = True

    def on_outdoor_model_clicked(self):
        self.outdoor_model.setStyleSheet("background-color: red; color: black")  # 改变按钮背景颜色
        self.class1.setText('Dog:')  # 改变标签文本
        self.class2.setText('Rain:')
        self.class3.setText('CarHorn:')
        self.prob1.setText('点击开始')
        self.prob2.setText('点击开始')
        self.prob3.setText('点击开始')
        self.which_model = False

    def on_start_clicked(self):
        result = subprocess.run(['python', 'calculate.py'], capture_output=True, text=True)
        prob = result.stdout.strip().split(',')
        self.prob1.setText(prob[0] if len(prob) > 0 else 'Error')
        self.prob1.setAlignment(Qt.AlignLeft)
        self.prob2.setText(prob[1] if len(prob) > 1 else 'Error')
        self.prob2.setAlignment(Qt.AlignLeft)
        self.prob3.setText(prob[2] if len(prob) > 2 else 'Error')
        self.prob3.setAlignment(Qt.AlignLeft)

    def on_stop_clicked(self):
        self.close()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
