import cv2
import numpy as np
import os
import itertools

from . import PreProcessing
from . import MessageShow
from . import YoloModel

class FindRoomFeature:
	def __init__(self, gradientThreshold, predictThreshold):
		self.gradientThreshold = gradientThreshold

		self.preProcessingInstance = PreProcessing.PreProcessing()
		self.yoloModelInstance = YoloModel.YoloModel(predictThreshold)

		self.objectList = []
		self.paperLength = []
		self.widthImgPath = []
		self.widthLength = []
		self.heightImgPath = None
		self.heightLength = None

		wImgPath = "./width_img/"
		hImgPath = "./height_img/"
		for f in os.listdir(wImgPath):
			self.widthImgPath.append(wImgPath + f)

		for f in os.listdir(hImgPath):
			self.heightImgPath = hImgPath + f



	def run(self):
		for wPath in self.widthImgPath:
			self.objectList.append(self.findObject(wPath))
			wImg = self.selectPreProcessing(wPath)
			self.widthLength.append(self.calWidthLength(wImg))

		hImg = self.selectPreProcessing(self.heightImgPath)
		self.heightLength = self.calHeightLength(hImg)

		self.objectList = list(dict.fromkeys(list(itertools.chain.from_iterable(self.objectList))))
		print(self.widthLength)
		print(self.heightLength)
		print(self.objectList)
			


	def readImg(self, path):
		return cv2.imread(path, cv2.IMREAD_COLOR)
	
	def preProcessing(self, path):
		return self.preProcessingInstance.transformImg(path)

	def selectPreProcessing(self, path):
		img = self.readImg(path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))

		result = MessageShow.messageShow(img)
		if result == "yes":
			return self.preProcessing(path)
		else:
			return img

	def findObject(self, path):
		return self.yoloModelInstance.predict(path)
		
	def setRoi(self, img, direction):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5,5), 0)
		h, w = gray.shape[:2]
		roi_x, roi_y = int(w/8), int(h/8)

		roi, length = [], None
		if direction == 'w':
			roi.append(gray[roi_y*2:roi_y*6, 0:roi_x])
			roi.append(gray[roi_y*2:roi_y*6, roi_x*7:w])
			roi.append(gray[roi_y*3:roi_y*5, roi_x*3:roi_x*5])
			length = w

		elif direction == 'h':
			roi.append(gray[0:roi_y, roi_x*2:roi_x*6])
			roi.append(gray[roi_y*7:h, roi_x*2:roi_x*6])
			roi.append(gray[roi_y*3:roi_y*5, roi_x*3:roi_x*5])
			length = h

		return roi, length

	def findLine(self, img):
		lineImg = []
		for rImg in img:
			canny = cv2.Canny(rImg, 15, 30)
			hough = cv2.HoughLinesP(canny, 1, np.pi/180, 30, None, 40, 5)
			lineImg.append(hough)

		return lineImg

	def calHeightLength(self, img):
		roiImg, length = self.setRoi(img, 'h')
		lineImg = self.findLine(roiImg)

		upper_line = []
		under_line = []
		for line in lineImg[0]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[0], (x1, y1), (x2, y2), (255,0,0), 1)
			if gradient < 1/self.gradientThreshold:
				upper_line.append([gradient, x1, x2, y1, y2])	

		for line in lineImg[1]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[1], (x1, y1), (x2, y2), (255,0,0), 1)
			if gradient < 1/self.gradientThreshold:
				under_line.append([gradient, x1, x2, y1, y2])	

		for line in lineImg[-1]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[-1], (x1, y1), (x2, y2), (255,0,0), 1)
			'''
			if gradient < 1/self.gradientThreshold:
				under_line.append([gradient, x1, x2, y1, y2])	
			'''
		upper_line.sort(key = lambda x: (-x[3], x[0]))
		under_line.sort(key = lambda x: (x[4], x[0]))

		hPixel = length - upper_line[0][3] - (length/8 - under_line[0][4])
		#hLength = hPixel / paperPixel

		cv2.imshow("upper_line", roiImg[0])
		cv2.imshow("under_line", roiImg[1])
		cv2.imshow("paper_line", roiImg[-1])
		cv2.waitKey(10000)
	
#return hLength

	def calWidthLength(self, img):
		roiImg, length = self.setRoi(img, 'w')
		lineImg = self.findLine(roiImg)
		
		left_line = []
		right_line = []
		paper_line = []
		for line in lineImg[0]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[0], (x1, y1), (x2, y2), (255,0,0), 1)
			if gradient > self.gradientThreshold:
				left_line.append([gradient, x1, x2, y1, y2])	

		for line in lineImg[1]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[1], (x1, y1), (x2, y2), (255,0,0), 1)
			if gradient > self.gradientThreshold:
				right_line.append([gradient, x1, x2, y1, y2])	

		for line in lineImg[-1]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			cv2.line(roiImg[-1], (x1, y1), (x2, y2), (255,0,0), 1)
			'''
			if gradient > self.gradientThreshold:
				right_line.append([gradient, x1, x2, y1, y2])	
			'''
		left_line.sort(key = lambda x: (x[1], -x[0]))
		right_line.sort(key = lambda x: (-x[2], -x[0]))

		wPixel = length - left_line[0][1] - (length/8 - right_line[0][2])
		#wLength = wPixel / paperPixel

		cv2.imshow("left_line", roiImg[0])
		cv2.imshow("right_line", roiImg[1])
		cv2.imshow("paper_line", roiImg[-1])
		cv2.waitKey(10000)

#return wLength

	def getLength(self):
		return self.widthLength, self.heightLength, self.objectList
