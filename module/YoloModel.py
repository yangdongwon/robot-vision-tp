from ultralytics import YOLO
import cv2

from . import MessageShow 

class YoloModel:
	def __init__(self, predictThreshold):
		self.model = YOLO('./module/yolov8n.pt')  
		self.predictThreshold = predictThreshold

	def predict(self, path, direction):
		results = self.model(path)
		obj_list = []
		obj_list_threshold = []


		for result in results:
			boxes = result.boxes.cpu().numpy()
			for box in boxes:
				obj_name = result.names[int(box.cls[0])]
				obj_list.append(obj_name)
				if (box.conf[0] > self.predictThreshold):
					obj_list_threshold.append(obj_name)
		
		resultImg = results[0].plot()
		if direction == 'h':
			resultImg = cv2.resize(resultImg, (int(resultImg.shape[1]/6), int(resultImg.shape[0]/6)))
		else :
			resultImg = cv2.resize(resultImg, (int(resultImg.shape[1]/4), int(resultImg.shape[0]/4)))
		MessageShow.foundObjectMessageShow(resultImg, obj_list, obj_list_threshold, self.predictThreshold)

		return obj_list_threshold
