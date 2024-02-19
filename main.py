import sys
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QApplication
from PyQt5.QtCore import QTimer
import time


class SerialPlotter(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化串口
        self.ser = serial.Serial('COM24', 9600)  # 替换为你的串口号和波特率

        # 初始化数据
        self.time_data = []
        self.value_data = []

        # 初始化程序开始时刻
        self.start_time = time.time()

        # 设置定时器，每隔一段时间更新数据
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(2)  # 每 2 毫秒更新一次

        # 初始化Matplotlib图形
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.time_data, self.value_data)
        self.canvas = FigureCanvas(self.fig)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setCentralWidget(self.canvas)

    def update_plot(self):
        # 获取当前时间
        current_time = time.time() - self.start_time

        # 读取串口数据
        data = self.ser.readline().decode().strip()

        # 更新数据列表
        self.time_data.append(current_time)
        self.value_data.append(float(data))

        # 更新绘图
        self.line.set_xdata(self.time_data)
        self.line.set_ydata(self.value_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialPlotter()
    window.show()
    sys.exit(app.exec_())
