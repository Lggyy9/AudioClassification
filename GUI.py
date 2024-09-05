import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import re

# 创建一个子线程类，用于运行AudioAcquisition.py录取音频
class AudioacqThread(QThread):
    finished_signal = pyqtSignal()

    def run(self):
        # 定义要运行的脚本路径
        script_path = r"F:\python_inter\AudioClassificatioin\Scripts\python.exe"
        script_name = "AudioAcquisition.py"

        # 使用subprocess运行脚本
        process = subprocess.Popen([script_path, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 等待脚本执行完成
        process.wait()

        # 脚本执行完成后发射信号
        self.finished_signal.emit()

# 创建一个子线程类，用于运行AudioClassifier.py并捕获输出
class ClassifierThread(QThread):
    finished_signal = pyqtSignal(str, float)  # 自定义信号，传递预测结果类型和概率

    def __init__(self, script_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.script_path = script_path

    def run(self):
        process = subprocess.Popen(
            [r"F:\python_inter\AudioClassificatioin\Scripts\python.exe", self.script_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()

        # 解析输出，找到Predictions部分的第一个预测结果
        prediction_type, prediction_prob = self.extract_first_prediction(stdout)
        self.finished_signal.emit(prediction_type, prediction_prob)  # 发送预测结果

    def extract_first_prediction(self, output):
        # 使用正则表达式匹配第一个预测结果和置信概率
        match = re.search(r"--> Predictions:\s+\['(.*?)'\]\n(.*?)\t(\d+\.\d+)", output)
        if match:
            prediction_path = match.group(1)
            prediction = prediction_path.split('\\')[-1]  # 提取路径中的文件名部分
            confidence = match.group(3)
            return prediction, float(confidence)
        else:
            return "None", 0.0

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 225, 800, 550)
        self.setWindowTitle('Audio Classification')
        # 创建并设置显示模块
        self.display = QLabel('请选择场景', self)
        self.define_label(self.display, 50, 50, 500, 310)
        # 室内音频识别按钮
        self.indoor_model = QPushButton('室内音频识别', self)
        self.define_button(self.indoor_model, 600, 50, 150, 50)
        self.indoor_model.setStyleSheet("background-color: white; color: black")
        self.indoor_model.clicked.connect(self.on_indoor_model_clicked)  # 连接信号
        # 室外音频识别按钮
        self.outdoor_model = QPushButton('室外音频识别', self)
        self.define_button(self.outdoor_model, 600, 150, 150, 50)
        self.outdoor_model.setStyleSheet("background-color: white; color: black")
        self.outdoor_model.clicked.connect(self.on_outdoor_model_clicked)  # 连接信号
        # 音频采集按钮
        self.audioacq_button = QPushButton('点击采集音频', self)
        self.define_button(self.audioacq_button, 600, 250, 150, 100)
        self.audioacq_button.clicked.connect(self.on_audioacq_button_clicked) # 连接信号
        # 开始按钮
        self.start_button = QPushButton('开始分析', self)
        self.define_button(self.start_button, 50, 400, 300, 100)
        self.start_button.clicked.connect(self.on_start_clicked)  # 连接信号
        # 结束按钮
        self.quit_button = QPushButton('退出', self)
        self.define_button(self.quit_button, 450, 400, 300, 100)
        self.quit_button.clicked.connect(self.on_quit_clicked)  # 连接信号
        # 用于记忆所选择的模型的布尔变量
        self.which_model = True

    def define_label(self, label, x, y, width, height):
        label.setAlignment(Qt.AlignCenter)  # 使文本居中
        label.setStyleSheet(
            f"QLabel {{background-color: black; color: white; font-size: {int(height * 0.5)}px;}}")  # 增大字体
        label.setFixedSize(width, height)
        label.move(x, y)
        label.setWordWrap(True)  # 设置自动换行

    def define_button(self, button, x, y, width, height):
        button.setFixedSize(width, height)
        button.move(x, y)

    def on_indoor_model_clicked(self):
        self.indoor_model.setStyleSheet("background-color: red; color: black")  # 改变按钮背景颜色
        self.display.setText('请采集音频')  # 改变标签文本
        self.which_model = True

    def on_outdoor_model_clicked(self):
        self.outdoor_model.setStyleSheet("background-color: red; color: black")  # 改变按钮背景颜色
        self.display.setText('请采集音频')  # 改变标签文本
        self.which_model = False

    def on_audioacq_button_clicked(self):
        self.display.setText("正在采集音频...")
        self.display.setStyleSheet(f"QLabel {{background-color: black; color: white; font-size: {75}px;}}")
        self.audioacq_thread = AudioacqThread()
        self.audioacq_thread.finished_signal.connect(self.on_audioacq_finished)
        self.audioacq_thread.start()

    def on_audioacq_finished(self):
        self.display.setText("音频采集完毕，请点击开始分析")
        self.display.setStyleSheet(f"QLabel {{background-color: black; color: white; font-size: {50}px;}}")

    def on_start_clicked(self):
        # 开始时将prob1设置为"Calculating..."
        self.display.setText("正在计算...")
        # 根据which_model变量决定运行哪个脚本
        script_path = "AudioClassifierIndoor.py" if self.which_model else "AudioClassifierOutdoor.py"
        # 创建并启动子线程运行相应的脚本
        self.classifier_thread = ClassifierThread(script_path)
        self.classifier_thread.finished_signal.connect(self.on_classification_finished)
        self.classifier_thread.start()

    def on_classification_finished(self, prediction_type, prediction_prob):
        # 运行结束后，显示提取到的概率值
        self.display.setText(f"这段音频可能是{prediction_type}，置信概率为{prediction_prob:.2f}")
        self.display.setStyleSheet(f"QLabel {{background-color: black; color: white; font-size: {50}px;}}")


    def on_quit_clicked(self):
        self.close()
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
