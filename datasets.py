import os
import shutil

# 文件路径
val_file_path = r"C:\Users\86198\yolov10\yolov10-main\GC10-DET\val\GC10-DET_val.txt"
images_dir = r"C:\Users\86198\yolov10\GC10-DET\images"
labels_dir = r"C:\Users\86198\yolov10\GC10-DET\labels"
val_images_dir = r"C:\Users\86198\yolov10\yolov10-main\GC10-DET\val\images"
val_labels_dir = r"C:\Users\86198\yolov10\yolov10-main\GC10-DET\val\labels"
train_images_dir = r"C:\Users\86198\yolov10\yolov10-main\GC10-DET\train\images"
train_labels_dir = r"C:\Users\86198\yolov10\yolov10-main\GC10-DET\train\labels"

# 创建目标文件夹
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)

# 读取验证集文件名
val_image_names = set()
with open(val_file_path, 'r') as file:
    lines = file.readlines()
    for line in lines:
        image_name = line.split()[0]
        val_image_names.add(image_name)

# 移动文件到相应文件夹
for image_name in os.listdir(images_dir):
    image_path = os.path.join(images_dir, image_name)
    label_path = os.path.join(labels_dir, os.path.splitext(image_name)[0] + '.txt')

    if image_name in val_image_names:
        shutil.copy(image_path, val_images_dir)
        shutil.copy(label_path, val_labels_dir)
    else:
        shutil.copy(image_path, train_images_dir)
        shutil.copy(label_path, train_labels_dir)

print("文件移动完成。")
