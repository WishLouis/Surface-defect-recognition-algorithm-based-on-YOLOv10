from ultralytics import YOLOv10

if __name__ == '__main__':
    model = YOLOv10('yolov10n.yaml').load('yolov10n.pt')
    # Train the model
    results = model.train(data='GC10-DET.yaml',
                          epochs=200,
                          imgsz=640,
                          batch=16,
                          optimizer='SGD', lr0=0.01,device=0)

