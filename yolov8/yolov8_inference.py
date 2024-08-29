from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("yolov8\yolov8s-cls0829.pt")



def yolov8_inference(source):
    
    # Run inference on the source
    results = model.predict(source, imgsz=224)  # list of Results objects
    # Process results list
    for result in results:
        # boxes = result.boxes  # Boxes object for bounding box outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        # keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        # obb = result.obb  # Oriented boxes object for OBB outputs
        # result.show()  # display to screen
        # result.save(filename="result.jpg")  # save to disk
    # if boxes.cls.numel() == 0:
    #     return None
    # return result.names[boxes.cls.item()],boxes.conf.item()
    return result.names[probs.top1],probs.top1conf
    
    





