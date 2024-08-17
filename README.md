# [Surface-defect-recognition-algorithm-based-on-YOLOv10]

## Project Overview
This project focuses on developing an advanced surface defect detection system using the YOLOv10 object detection algorithm. The primary objective is to detect surface defects in industrial materials, specifically strip steel, with high accuracy and efficiency.


## Key Components
### 1. YOLOv10 Training
#### Algorithm: YOLOv10, a state-of-the-art object detection model, is trained to identify and classify various types of surface defects.
####  Data: The training dataset consists of labeled images representing different defect types on strip steel surfaces.
####  Outcome: The trained model is capable of real-time detection, providing precise localization and classification of surface defects.

### 2. UI Design with PyQt
#### Interface: A user-friendly graphical user interface (GUI) is designed using PyQt to enhance the visualization of detection results.
#### Features: The interface allows users to upload test images, view real-time detection results, and interact with the model's parameters.
#### Visualization: The UI displays both the input images and the detected defects, making it accessible for operators in industrial settings.

### 3. Dynamic Video Simulation with OpenCV
#### Video Synthesis: OpenCV is utilized to combine the test images into a dynamic video sequence. This simulates the real-time detection process in a strip steel production environment.
#### Simulation: The video output provides a realistic representation of how the detection system would perform during actual steel production, ensuring that the system meets industrial requirements.


## YOLOv10

[YOLOv10: Real-Time End-to-End Object Detection](https://arxiv.org/abs/2405.14458).\
Ao Wang, Hui Chen, Lihao Liu, Kai Chen, Zijia Lin, Jungong Han, and Guiguang Ding\
[![arXiv](https://img.shields.io/badge/arXiv-2405.14458-b31b1b.svg)](https://arxiv.org/abs/2405.14458) <a href="https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolov10-object-detection-on-custom-dataset.ipynb#scrollTo=SaKTSzSWnG7s"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-blue)](https://huggingface.co/collections/jameslahm/yolov10-665b0d90b0b5bb85129460c2) [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/jameslahm/YOLOv10)  [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/kadirnar/Yolov10)  [![Transformers.js Demo](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers.js-blue)](https://huggingface.co/spaces/Xenova/yolov10-web) [![LearnOpenCV](https://img.shields.io/badge/BlogPost-blue?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAMAAAC67D%2BPAAAALVBMVEX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F6%2Bfn6%2Bvq3y%2BJ8rOFSne9Jm%2FQcOlr5DJ7GAAAAB3RSTlMAB2LM94H1yMxlvwAAADNJREFUCFtjZGAEAob%2FQMDIyAJl%2FmFkYmEGM%2F%2F%2BYWRmYWYCMv8BmSxYmUgKkLQhGYawAgApySgfFDPqowAAAABJRU5ErkJggg%3D%3D&logoColor=black&labelColor=gray)](https://learnopencv.com/yolov10/) [![Openbayes Demo](https://img.shields.io/static/v1?label=Demo&message=OpenBayes%E8%B4%9D%E5%BC%8F%E8%AE%A1%E7%AE%97&color=green)](https://openbayes.com/console/public/tutorials/im29uYrnIoz) 

Please refer to the specific code of YOLOv10："https://github.com/THU-MIG/yolov10"

## UI Design with PyQt
The UI is divided into two main sections. The upper section features a visualization window, where the left side displays the original image and the right side shows the detection results after processing by the model. The lower section consists of four functional buttons and a log output window. The log window provides real-time updates on the current detection information. The four buttons include an **Image Detection** button for processing selected images, a **Video Detection** button for video analysis, a  Camera Detection button for live feed analysis, and a **Stop** button to halt the detection process.

<p align="center">
  <img src="figures/Detection.png">
  UI interface diagram
</p>

### Button
The Image Detection button allows users to select and analyze a single image for surface defects. The Video Detection button enables the processing of a video file, detecting and highlighting defects frame by frame. The Real-time Camera Detection button initiates live feed analysis from a connected camera, providing real-time detection results. The Stop button is designed to halt any ongoing detection process, offering users control over the detection workflow.
<p align="left">
  <img src="figures/b1.png" width="90">
  The Video Detection button
</p>

<p align="left">
  <img src="figures/b2.png"width="90">
  The Real-time Camera Detection button
</p>

<p align="left">
  <img src="figures/b3.png"width="90">
  The Image Detection button
</p>

<p align="left">
  <img src="figures/b4.png"width="90">
   The Stop button
</p>


### Log window
The log window provides real-time feedback by displaying detailed information about each detection operation, including timestamps, detected defect types, and processing status. This feature helps users monitor the system's performance and review the results of each detection task.
<p align="center">
  <img src="figures/log.png">
   The Stop button
</p>


## Conclusion
This project not only advances the detection capabilities for surface defects but also integrates a high-level visual interface and realistic simulation to ensure practical applicability in industrial environments. The combination of YOLOv10, PyQt, and OpenCV offers a comprehensive solution for surface defect detection, paving the way for more efficient and accurate quality control processes in the steel industry.