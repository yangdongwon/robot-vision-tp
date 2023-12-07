import sys
import numpy as np
import cv2

class ImageProcessor:
    def __init__(self, image_path):
        self.src = cv2.imread(image_path)
        self.src = cv2.resize(self.src, (1080, 720))
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
                sys.exit()

        # 투시 변환
        pers = cv2.getPerspectiveTransform(self.srcQuad, self.dstQuad)
        dst = cv2.warpPerspective(self.src, pers, (self.dw, self.dh), flags=cv2.INTER_CUBIC)

        # 결과 영상 출력
        cv2.imshow('dst', dst)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return dst
        



if __name__ == "__main__":
    image_processor = ImageProcessor("/home/dohwan/python/tp/width_img/IMG_1189.jpeg")
    image_processor.process_image()
