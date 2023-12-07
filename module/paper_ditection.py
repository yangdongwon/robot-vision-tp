import cv2
import numpy as np
import os
import sys

class ImageProcessor:
    def __init__(self, img):
        self.src = img
        if self.src is None:
            print('Image open failed!')
            sys.exit()

        # 입력 영상 크기 및 출력 영상 크기
        self.h, self.w = self.src.shape[:2]
        self.dw = 1200
        self.dh = 600

        # 모서리 점들의 좌표, 드래그 상태 여부
        self.srcQuad = np.array([[30, 30], [30, self.h-30], [self.w-30, self.h-30], [self.w-30, 30]], np.float32)
        self.dstQuad = np.array([[0, 0], [0, self.dh-1], [self.dw-1, self.dh-1], [self.dw-1, 0]], np.float32)
        self.dragSrc = [False, False, False, False]

    def draw_ROI(self, img, corners):
        cpy = img.copy()

        c1 = (192, 192, 255)
        c2 = (128, 128, 255)

        for pt in corners:
            cv2.circle(cpy, tuple(pt.astype(int)), 25, c1, -1, cv2.LINE_AA)

        cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2, cv2.LINE_AA)
        cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2, cv2.LINE_AA)

        disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

        return disp

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for i in range(4):
                if cv2.norm(self.srcQuad[i] - (x, y)) < 25:
                    self.dragSrc[i] = True
                    self.ptOld = (x, y)
                    break

        if event == cv2.EVENT_LBUTTONUP:
            for i in range(4):
                self.dragSrc[i] = False

        if event == cv2.EVENT_MOUSEMOVE:
            for i in range(4):
                if self.dragSrc[i]:
                    dx = x - self.ptOld[0]
                    dy = y - self.ptOld[1]

                    self.srcQuad[i] += (dx, dy)

                    cpy = self.draw_ROI(self.src, self.srcQuad)
                    cv2.imshow('img', cpy)
                    self.ptOld = (x, y)
                    break

    def process_image(self):
        # 모서리점, 사각형 그리기 
        disp = self.draw_ROI(self.src, self.srcQuad)
        cv2.imshow('img', disp)
        cv2.setMouseCallback('img', self.on_mouse)
		
        while True:
            key = cv2.waitKey()
            if key == 13:  # ENTER 키
                break
            elif key == 27:  # ESC 키
                cv2.destroyWindow('img')
                break 
				#sys.exit()

        # 투시 변환
        pers = cv2.getPerspectiveTransform(self.srcQuad, self.dstQuad)
        dst = cv2.warpPerspective(self.src, pers, (self.dw, self.dh), flags=cv2.INTER_CUBIC)

        # 결과 영상 출력
        cv2.imshow('dst', dst)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return dst
	
class findRoomFeature:
	def __init__(self, gradientThreshold):
		self.gradientThreshold = gradientThreshold

		self.paperLength = []
		self.widthImgPath = []
		self.widthLength = []
		self.heightImgPath = None
		self.heightLength = None

		wImgPath = "/home/dohwan/python/tp/width_img/" #./width_img/
		hImgPath = "/home/dohwan/python/tp/height_img/"#./height_img/
		for f in os.listdir(wImgPath):
			self.widthImgPath.append(wImgPath + f)

		for f in os.listdir(hImgPath): 
			self.heightImgPath = hImgPath + f
	
	def readImg(self, path):
		return cv2.imread(path, cv2.IMREAD_COLOR)
	
	def setRoi(self, img, direction):
		img = cv2.resize(img, (int(img.shape[1]/4), int(img.shape[0]/4)))
		image_processor = ImageProcessor(img)
		img = image_processor.process_image()
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
		paper_line = []
		upper_line = []
		under_line = []
		a4_paper_w = 0.21
		a4_paper_h = 0.297
		
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

		cv2.imshow("paper_line", roiImg[-1])
		cv2.waitKey(10000)
	
#return hLength

	def calWidthLength(self, img):
		roiImg, length = self.setRoi(img, 'w')
		lineImg = self.findLine(roiImg)
		paper_h ,paper_w = roiImg[-1].shape[:2]
		left_line = []
		right_line = []
		paper_line_left = []
		paper_line_right = []
		
		for line in lineImg[-1]:
			x1, y1, x2, y2 = line[0]
			gradient = abs((y2-y1)/(x2-x1))
			gradient_prev = 0
			cv2.line(roiImg[-1], (x1, y1), (x2, y2), (255,0,0), 1)
			if gradient > self.gradientThreshold and x1 > paper_w/2:
				paper_line_right.append([gradient, x1, x2, y1, y2])
			elif gradient > self.gradientThreshold and x1 < paper_w/2:
				paper_line_left.append([gradient, x1, x2, y1, y2])


		# paper_line_left.sort(key = lambda x: (x[1], -x[0]))
		# paper_line_right.sort(key = lambda x: (x[1], -x[0]))
	

		# pixel_length = 0.21/(paper_line_right[0][1] - paper_line_left[0][1]) #a4 width를 paper가 차지하는 width pixel로 나누기 
		# wLength = wPixel*pixel_length
		# print("wPixel",wPixel)
		# print("wlenbgth",wLength)

		cv2.imshow("paper_line", roiImg[-1])
		cv2.waitKey(10000)

#return wLength

	def getLength(self):
		return self.widthLength, self.heightLength, self.paperLength

	def run(self):
		for wPath in self.widthImgPath:
			wImg = self.readImg(wPath)
			self.widthLength.append(self.calWidthLength(wImg))

		hImg = self.readImg(self.heightImgPath)
		self.heightLength = self.calHeightLength(hImg)

		print(self.widthLength)
		print(self.heightLength)
			

p = findRoomFeature(10.0)
p.run()