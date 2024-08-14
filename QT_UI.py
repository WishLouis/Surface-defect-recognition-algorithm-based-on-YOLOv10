import cv2
import os
import time
from threading import Thread
from collections import Counter
from PySide6 import QtWidgets, QtCore, QtGui

# 不然每次YOLO处理都会输出调试信息
os.environ['YOLO_VERBOSE'] = 'False'
from ultralytics import YOLOv10


class MWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # 设置界面
        self.setupUI()

        self.camBtn.clicked.connect(self.startCamera)
        self.stopBtn.clicked.connect(self.stop)
        self.videoBtn.clicked.connect(self.openVideoFile)
        self.imageBtn.clicked.connect(self.openImageFile)
        self.last_detection_results = {}  # 存储上一帧的检测结果
        self.output_threshold = 2  # 输出阈值，超过阈值的变化才输出

        # 定义定时器，用于控制显示视频的帧率
        self.timer_camera = QtCore.QTimer()
        # 定时到了，回调 self.show_camera
        self.timer_camera.timeout.connect(self.show_camera)

        # 加载 YOLO nano 模型，第一次比较耗时，要20秒左右
        self.model = YOLOv10('runs/detect/train/weights/best.pt')  # load a custom model

        # 要处理的视频帧图片队列，目前就放1帧图片
        self.frameToAnalyze = []
        self.imageToAnalyze = []

        # 启动处理视频帧独立线程
        self.processing_active = True
        Thread(target=self.frameAnalyzeThreadFunc, daemon=True).start()

    def setupUI(self):
        self.resize(1200, 800)
        self.setWindowTitle('YOLOv10+Qt 演示')

        # central Widget
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)

        # central Widget 里面的 主 layout
        mainLayout = QtWidgets.QVBoxLayout(centralWidget)

        # 界面的上半部分 : 图形展示部分
        topLayout = QtWidgets.QHBoxLayout()
        self.label_ori_video = QtWidgets.QLabel(self)
        self.label_treated = QtWidgets.QLabel(self)
        self.label_ori_video.setMinimumSize(520, 400)
        self.label_treated.setMinimumSize(520, 400)
        self.label_ori_video.setStyleSheet('border:1px solid #D7E2F9;')
        self.label_treated.setStyleSheet('border:1px solid #D7E2F9;')

        topLayout.addWidget(self.label_ori_video)
        topLayout.addWidget(self.label_treated)

        mainLayout.addLayout(topLayout)

        # 界面下半部分： 输出框 和 按钮
        groupBox = QtWidgets.QGroupBox(self)
        bottomLayout = QtWidgets.QHBoxLayout(groupBox)
        self.textLog = QtWidgets.QTextBrowser()
        bottomLayout.addWidget(self.textLog)

        mainLayout.addWidget(groupBox)

        btnLayout = QtWidgets.QVBoxLayout()
        self.videoBtn = QtWidgets.QPushButton('🎞️视频文件')
        self.camBtn = QtWidgets.QPushButton('📹摄像头')
        self.imageBtn = QtWidgets.QPushButton('🏞图片')
        self.stopBtn = QtWidgets.QPushButton('🛑停止')
        btnLayout.addWidget(self.videoBtn)
        btnLayout.addWidget(self.camBtn)
        btnLayout.addWidget(self.imageBtn)
        btnLayout.addWidget(self.stopBtn)
        bottomLayout.addLayout(btnLayout)

    def log(self, message):
        self.textLog.append(message)
        self.textLog.ensureCursorVisible()

    def startCamera(self):
        self.log("Starting camera...")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.log("1号摄像头不能打开")
            return

        if not self.timer_camera.isActive():  # 若定时器未启动
            self.timer_camera.start(33)  # 设置为每秒约30帧
            self.log("Camera started.")

    def openVideoFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择视频文件", "", "Video Files (*.mp4 *.avi *.mkv)",
                                                            options=options)
        if fileName:
            self.log(f"Opening video file: {fileName}")
            self.cap = cv2.VideoCapture(fileName)
            if not self.cap.isOpened():
                self.log("视频文件不能打开")
                return

            # 获取视频的帧率
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            if not self.timer_camera.isActive():  # 若定时器未启动
                self.timer_camera.start(int(1000 / fps))  # 根据视频帧率设置定时器
                self.log("Video file started.")

    def openImageFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择图片文件", "",
                                                            "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if fileName:
            self.log(f"Opening image file: {fileName}")
            img = cv2.imread(fileName)
            if img is None:
                self.log("图片文件不能打开")
                return

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.imageToAnalyze.append((img, fileName))  # 存储图片及文件名
            self.show_image(img)

    def show_image(self, img):
        qImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label_ori_video.setPixmap(QtGui.QPixmap.fromImage(qImage))
        self.analyze_frame(img, is_image=True)

    def show_camera(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()  # 从视频流中读取
        if not ret:
            return

        # 把读到的16:10帧的大小重新设置
        frame = cv2.resize(frame, (520, 400))
        # 视频色彩转换回RGB，OpenCV images as BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImage = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)  # 变成QImage形式
        # 往显示视频的Label里 显示QImage
        self.label_ori_video.setPixmap(QtGui.QPixmap.fromImage(qImage))

        # 如果当前没有处理任务
        if not self.frameToAnalyze:
            self.frameToAnalyze.append(frame)

    def frameAnalyzeThreadFunc(self):
        while self.processing_active:
            if self.frameToAnalyze:
                frame = self.frameToAnalyze.pop(0)
                self.analyze_frame(frame, is_image=False)
            if self.imageToAnalyze:
                img, fileName = self.imageToAnalyze.pop(0)
                self.analyze_frame(img, is_image=True, fileName=fileName)
            time.sleep(0.05)  # Yield control to keep UI responsive

    def analyze_frame(self, frame, is_image, fileName=None):
        results = self.model(frame)
        img = results[0].plot(line_width=1)
        qImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)  # 变成QImage形式

        if is_image:
            self.label_treated.setPixmap(QtGui.QPixmap.fromImage(qImage))
        else:
            self.label_treated.setPixmap(QtGui.QPixmap.fromImage(qImage))  # 往显示Label里 显示QImage

        self.log_detection_results(results[0], fileName=fileName)

    # 修改 log_detection_results 方法
    def log_detection_results(self, results, fileName=None):
        boxes = results.boxes
        class_counts = Counter(box.cls.item() for box in boxes) if boxes is not None else {}

        # 构建当前帧的日志信息
        log_message = ""
        if fileName:
            log_message += f"{fileName}\n"

        for cls, count in class_counts.items():
            if cls in self.last_detection_results:
                if count != self.last_detection_results[cls]:
                    log_message += f"{results.names[int(cls)]}: {self.last_detection_results[cls]} —> {count}\n"
                    self.last_detection_results[cls] = count
            else:
                log_message += f"{results.names[int(cls)]}: {count}\n"
                self.last_detection_results[cls] = count

        if log_message:
            self.log(log_message)  # 输出日志信息

    def stop(self):
        self.log("Stopping...")
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()  # 释放视频流
            self.cap = None
        self.timer_camera.stop()  # 关闭定时器
        self.label_ori_video.clear()  # 清空视频显示区域（仅当视频停止）
        if not self.imageToAnalyze:  # 如果没有图像正在分析，则清空检测显示区域
            self.label_treated.clear()  # 清空视频显示区域
        self.processing_active = False
        self.log("Stopped.")


app = QtWidgets.QApplication()
window = MWindow()
window.show()
app.exec()
