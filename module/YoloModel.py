from ultralytics import YOLO

class YoloModel:
	def __init__(self, predictThreshold):
		self.model = YOLO('./module/yolov8n.pt')  
		self.predictThreshold = predictThreshold

	def predict(self, path):
		results = self.model(path)
		obj_list = []

		for result in results:
			boxes = result.boxes.cpu().numpy()
			for box in boxes:
				if (box.conf[0] > self.predictThreshold):
					obj_name = result.names[int(box.cls[0])]
					obj_list.append(obj_name)
		
		return obj_list
