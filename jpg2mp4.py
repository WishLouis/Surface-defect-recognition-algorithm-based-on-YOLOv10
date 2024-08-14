import cv2
import os
import random

# 图像文件夹路径
image_folder = 'C:\\Users\\86198\\yolov10\\yolov10-main\\NEU-DET\\test\\images'

# 获取所有图像文件的路径
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]

# 打乱图像顺序
random.shuffle(images)

# 确定视频的帧率和输出路径
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video_name = 'test_1fps.mp4'
fps = 1  # 帧率

# 创建视频写入对象
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

# 释放视频写入对象
video.release()
