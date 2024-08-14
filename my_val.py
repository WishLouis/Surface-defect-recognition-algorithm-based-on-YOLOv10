from ultralytics import YOLOv10

# Load a model
if __name__ == '__main__':
    model = YOLOv10('runs/detect/train2/weights/best.pt')  # load a custom model

    # Validate the model
    metrics = model.val(data='NEU-DET.yaml',
                        batch=16)  # no arguments needed, dataset and settings remembered
    metrics.box.map    # map50-95
    metrics.box.map50  # map50
    metrics.box.map75  # map75
    metrics.box.maps   # a list contains map50-95 of each category
