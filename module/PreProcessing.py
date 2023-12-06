import sys
import numpy as np
import cv2

class PreProcessing:
	srcQuad = None
	dstQuad = None
	dragSrc = None
	ptOld = None
	src = None

	width = None
	height = None
	
	def drawROI(self, img):
		cpy = img.copy()
		corners = self.srcQuad

		c1 = (192, 192, 255)
		c2 = (128, 128, 255)

		for pt in corners:
			cv2.circle(cpy, tuple(pt.astype(int)), 9, c1, -1, cv2.LINE_AA)

		cv2.line(cpy, tuple(corners[0].astype(int)), tuple(corners[1].astype(int)), c2, 2, cv2.LINE_AA)
		cv2.line(cpy, tuple(corners[1].astype(int)), tuple(corners[2].astype(int)), c2, 2, cv2.LINE_AA)
		cv2.line(cpy, tuple(corners[2].astype(int)), tuple(corners[3].astype(int)), c2, 2, cv2.LINE_AA)
		cv2.line(cpy, tuple(corners[3].astype(int)), tuple(corners[0].astype(int)), c2, 2, cv2.LINE_AA)

		disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

		return disp


	def onMouse(self, event, x, y, flags, param):
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

                			cpy = self.drawROI(self.src)
                			cv2.imshow('img', cpy)
                			self.ptOld = (x, y)
                			break

	def calDistQuad(self):
		    # 좌표 4개 중 상하좌우 찾기
            sm = self.srcQuad.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(self.srcQuad, axis=1)  # 4쌍의 좌표 각각 x-y 계산

            topLeft = self.srcQuad[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
            bottomRight = self.srcQuad[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
            topRight = self.srcQuad[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = self.srcQuad[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

            # 변환 전 4개 좌표
            self.srcQuad = np.float32([topLeft, topRight, bottomRight, bottomLeft])

            # 변환 후 영상에 사용할 서류의 폭과 높이 계산
            w1 = abs(bottomRight[0] - bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            self.width = int(max([w1, w2]))  # 두 좌우 거리간의 최대값이 서류의 폭
            self.height = int(max([h1, h2]))  # 두 상하 거리간의 최대값이 서류의 높이

            # 변환 후 4개 좌표
            self.dstQuad = np.float32([[0, 0], [self.width - 1, 0], [self.width - 1, self.height - 1], [0, self.height - 1]])

# 입력 이미지 불러오기
	def transformImg(self, path):
		src = cv2.imread(path, cv2.IMREAD_COLOR)
		src = cv2.resize(src, (int(src.shape[1]/4), int(src.shape[0]/4)))
		self.src = src

		if src is None:
    			print('Image open failed!')
    			sys.exit()

		# 입력 영상 크기 및 출력 영상 크기
		h, w = src.shape[:2]
		dw = w
		dh = h

		# 모서리 점들의 좌표, 드래그 상태 여부
		self.srcQuad = np.array([[int(w/4), int(h/4)], [int(w/4), int(h/4*3)], [int(w/4*3), int(h/4*3)], [int(w/4*3), int(h/4)]], np.float32)
		self.dragSrc = [False, False, False, False]

		# 모서리점, 사각형 그리기
		disp = self.drawROI(src)

		cv2.imshow('img', disp)
		cv2.setMouseCallback('img', self.onMouse)

		while True:
    			key = cv2.waitKey()
    			if key == 13:  # ENTER 키
        			break
    			elif key == 27:  # ESC 키
        			cv2.destroyWindow('img')
        			sys.exit()

		self.calDistQuad()
		# 투시 변환
		pers = cv2.getPerspectiveTransform(self.srcQuad, self.dstQuad)
		dst = cv2.warpPerspective(src, pers, (self.width, self.height), flags=cv2.INTER_CUBIC)

		'''
		# 결과 영상 출력
		cv2.imshow('dst', dst)
		cv2.waitKey()
		'''
		cv2.destroyAllWindows()
		return dst
