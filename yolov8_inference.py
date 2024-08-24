from ultralytics import YOLO


# Load a pretrained YOLOv8n model
model = YOLO("yolov8s_0820.pt")


def yolov8_inference(source):

    # Run inference on the source
    results = model.predict(source, conf=0.4,iou=0.7,max_det=10,imgsz=640)  # list of Results objects
    boxes = results[0].boxes
    return results[0].names[boxes.cls.item()]
    
    





