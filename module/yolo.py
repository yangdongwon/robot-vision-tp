from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # load a pretrained YOLOv8n detection model
results = model('/home/dohwan/python/tp/module/IMG_12.jpeg')  # predict on an image

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    print(boxes, masks, keypoints, probs)

list2 = [data for inner_list in list1 for data in inner_list]