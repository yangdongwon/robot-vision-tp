import cv2
import numpy as np
import os
import natsort
import itertools

from . import PreProcessing 
from . import MessageShow 
from . import YoloModel
from . import SelfSelect

class FindRoomFeature:
	def __init__(self, gradientThreshold, predictThreshold):
		self.gradientThreshold = gradientThreshold

		self.preProcessingInstance = PreProcessing.PreProcessing()
		self.yoloModelInstance = YoloModel.YoloModel(predictThreshold)

		self.objectList = []
		self.paperLength = []
		self.widthImgPath = []
		self.widthLength = [] # 가로 
		self.widthlength_2 = [] #세로 
		self.heightImgPath = None
		self.heightLength = None
		self.objImgPath = None
		
		wImgPath = "./width_img/" 
		hImgPath = "./height_img/"
		objImgPath = "./object_img/"
		for f in natsort.natsorted(os.listdir(wImgPath)):
			self.widthImgPath.append(wImgPath + f)

		for f in natsort.natsorted(os.listdir(hImgPath)):
			self.heightImgPath = hImgPath + f
			
		for f in natsort.natsorted(os.listdir(objImgPath)):
			self.objImgPath = objImgPath + f
	
	def run(self):
		number = 0 
		for wPath in self.widthImgPath:
			wImg = self.selectPreProcessing(wPath, 'w')
			self.objectList.append(self.findObject(wPath, 'w'))
			if number % 2 ==0 :
				self.widthLength.append(self.calWidthLength(wImg))
			else: 
				self.widthlength_2.append(self.calWidthLength(wImg))
			number+=1
		hImg = self.selectPreProcessing(self.heightImgPath, 'h')
		self.heightLength = self.calHeightLength(hImg)
		self.objectList.append(self.findObject(self.objImgPath, 'h'))
		
		self.widthmean = np.mean(self.widthLength) #가로 평균 
		self.widthmean_2 = np.mean(self.widthlength_2) #세로 평균 
		
		self.objectList = list(dict.fromkeys(list(itertools.chain.from_iterable(self.objectList))))

		MessageShow.messageShow_length_mean(self.widthmean,self.widthmean_2,self.heightLength, self.objectList)

	def readImg(self, path):
		return cv2.imread(path, cv2.IMREAD_COLOR)
	
	# 전처리 
	def preProcessing(self, path):
		return self.preProcessingInstance.transformImg(path)
	
	#전처리 여부 결정
	def selectPreProcessing(self, path, direction):
		img = self.readImg(path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		if direction == 'h':
			img = cv2.resize(img, (int(img.shape[1]/6), int(img.shape[0]/6)))
		else :
			img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
		result = MessageShow.messageShow(img)
		if result == "yes":
			return self.preProcessing(path)
		else:
			return img
		
	#스스로 모서리 찍을 것인지 결정 
	def selectSelfcorner(self,img, direction):
		result = MessageShow.messageShow_self_choice()
		if result == "yes":
			length_result =self.setLine(img,direction)
			return length_result
		else:
			return 0
			
	# YOLO 사용한 객체 인식
	def findObject(self, path, direction):
		return self.yoloModelInstance.predict(path, direction)

	#ROI 설정(라인검출 전 전처리)
	def setRoi(self, img, direction):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (5,5), 0)
		h, w = gray.shape[:2]
		roi_x, roi_y = int(w/8), int(h/8)

		roi, length = [], None
		if direction == 'w':
			roi.append(gray[roi_y*2:roi_y*6, 0:roi_x])
			roi.append(gray[roi_y*2:roi_y*6, roi_x*7:w])
			roi.append(gray[roi_y*2:roi_y*6, roi_x*3:roi_x*5])
			length = w

		elif direction == 'h':
			roi.append(gray[0:roi_y, roi_x*2:roi_x*6])
			roi.append(gray[roi_y*7:h, roi_x*2:roi_x*6])
			roi.append(gray[roi_y*3:roi_y*5, roi_x*3:roi_x*5])
			length = h

		return roi, length

	# canny edge detection과 hough transform을 사용하여 모서리 추출, 그 중  직선 추출 
	def findLine(self, img):
		lineImg = []
		for rImg in img:
			canny = cv2.Canny(rImg, 15, 30)
			hough = cv2.HoughLinesP(canny, 1, np.pi/180, 30, None, 25, 5)
			lineImg.append(hough)

		return lineImg
	
	#이미지에서 직접 벽 모서리, 종이 모서리 좌표 찍기 (벽모서리, 종이모서리 순으로 찍고 enter, 가로일 땐 가로 모서리들 세로일 땐 세로 모서리 찍기)
	def setLine(self,img,Direction): 
		pp = SelfSelect.SelfSelect(img,Direction)
		result = pp.SelfSelect_run()
		paper_pixel = abs(result[3]- result[2])
		pixel_length = 0.21/paper_pixel
		wall_Pixel = abs(result[1]- result[0])
		length = wall_Pixel*pixel_length
		#print(Direction, "Length ",length, "m")
		return length
	
	# 높이 측정, 각 직선의 기울기를 계산하여 높이의 경우 기울기가 가장 작은 직선으로 정렬 후 그 중 y좌표가 가장 높은 곳과 낮은 곳 추출
	def calHeightLength(self, img):
		roiImg, length = self.setRoi(img, 'h')
		direction = 'h'
		lineImg = self.findLine(roiImg)
		paper_h ,paper_w = roiImg[-1].shape[:2]
		upper_line = []
		under_line = []
		paper_line_left = []
		paper_line_right = []
		try:
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
				if gradient > self.gradientThreshold and x1 > paper_w/2:
					paper_line_right.append([gradient, x1, x2, y1, y2])
				elif gradient > self.gradientThreshold and x1 < paper_w/2:
					paper_line_left.append([gradient, x1, x2, y1, y2])
					
			upper_line.sort(key = lambda x: (-x[3], x[0]))
			under_line.sort(key = lambda x: (x[4], x[0]))
			paper_line_left.sort(key = lambda x: (x[1], -x[0]))
			paper_line_right.sort(key = lambda x: (x[1], -x[0]))
			hPixel = length - upper_line[0][3] - (length/8 - under_line[0][4])
			pixel_length = 0.21/(paper_line_right[0][1] - paper_line_left[0][1]) #a4 width를 paper가 차지하는 width pixel로 나누기 
			hlength = hPixel*pixel_length
			
			print("hWidth",hlength,"m")

			cv2.imshow("upper_line", roiImg[0])
			cv2.imshow("under_line", roiImg[1])
			cv2.imshow("paper_line", roiImg[-1])	
			cv2.waitKey(10000)
			MessageShow.messageShow_length(hlength,direction) #길이 출력 후 본인이 다시 모서리 찍어서 측정할 것인지 결정 
			selfwlength = self.selectSelfcorner(img,direction)
			if selfwlength != 0:
					hlength = selfwlength
			return hlength
		#모서리 미검출 시 에러처리 
		except TypeError as e:
				MessageShow.messageShow_error_run(e)
				hlength = self.setLine(img,direction)
				print("height",hlength, direction)
				MessageShow.messageShow_length(hlength,direction)
				return hlength
		except IndexError as e:
				MessageShow.messageShow_error_run(e)
				hlength = self.setLine(img,direction)
				print("height",hlength, direction)
				MessageShow.messageShow_length(hlength,direction)
				return hlength

	# 벽 모서리 계산, 위와 마찬가지로 추출된 직선 중 기울기가 큰 순서대로 정렬 후 x좌표가 가장 큰 것과 작은 것이 각 벽의 모서리로 판단하고 추출
	def calWidthLength(self, img):
		roiImg, length = self.setRoi(img, 'w')
		direction = 'w'
		lineImg = self.findLine(roiImg)
		paper_h ,paper_w = roiImg[-1].shape[:2]
		print("paper_w",paper_w)
		left_line = []
		right_line = []
		paper_line_left = []
		paper_line_right = []
	    
		
		try:
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
				gradient_prev = 0
				cv2.line(roiImg[-1], (x1, y1), (x2, y2), (255,0,0), 1)
				if gradient > self.gradientThreshold and x1 > paper_w/2:
					paper_line_right.append([gradient, x1, x2, y1, y2])
				elif gradient > self.gradientThreshold and x1 < paper_w/2:
					paper_line_left.append([gradient, x1, x2, y1, y2])

			left_line.sort(key = lambda x: (x[1], -x[0]))
			right_line.sort(key = lambda x: (-x[2], -x[0]))
			paper_line_left.sort(key = lambda x: (-x[1], -x[0]))
			paper_line_right.sort(key = lambda x: (x[1], -x[0]))
			wPixel = length - left_line[0][1] - (length/8 - right_line[0][2])
			if len(paper_line_right) ==0 or len(paper_line_left) == 0:
				print("종이가 인식되지 않습니다.")
				cv2.imshow("left_line", roiImg[0])
				cv2.imshow("right_line", roiImg[1])
				cv2.imshow("paper_line", roiImg[-1])
				cv2.waitKey(10000)
				MessageShow.messageShow_error_paper()
				wlength = self.setLine(img,direction)
				MessageShow.messageShow_length(wlength,direction)
				return wlength
			else:
				pixel_length = 0.21/(paper_line_right[0][1] - paper_line_left[0][1]) #a4 width를 paper가 차지하는 width pixel로 나누기 
				wlength = wPixel*pixel_length
				print("width",wlength, "m")
				cv2.imshow("left_line", roiImg[0])
				cv2.imshow("right_line", roiImg[1])
				cv2.imshow("paper_line", roiImg[-1])
				cv2.waitKey(10000)
				MessageShow.messageShow_length(wlength,direction)
				selfwlength = self.selectSelfcorner(img,direction)
				if selfwlength != 0:
					wlength = selfwlength
					MessageShow.messageShow_length(wlength,direction)
					print("width",wlength, "m")
				return wlength
			
		#모서리 미검출 시 에러처리
		except TypeError as e:
				MessageShow.messageShow_error_run(e)
				wlength = self.setLine(img,direction)
				print("width",wlength, direction)
				MessageShow.messageShow_length(wlength,direction)
				return wlength
		except IndexError as e:
				MessageShow.messageShow_error_run(e)
				wlength = self.setLine(img,direction)
				print("width",wlength, direction)
				MessageShow.messageShow_length(wlength,direction)
				return wlength

	#측정된 파라미터 getter
	def getParameter(self):
		return self.widthmean, self.widthmean_2, self.heightLength, self.objectList
