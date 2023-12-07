import cv2

class SelfSelect:
    def __init__(self,img,Direction): 
        self.Direction = Direction
        self.img = img
        self.wallline = []
        self.paperline = []
        self.times = 0
    # 마우스 클릭 이벤트 콜백 함수
    def mouse_callback(self, event, x, y, flags, param):
        # 마우스 왼쪽 버튼을 클릭할 때
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"마우스 좌클릭: ({x}, {y})")
            if self.times < 2: 
                self.wallline.append((x, y))
            else:
                self.paperline.append((x, y))
            self.times += 1

    # 이미지 파일 읽기
    def SelfSelect_run(self):
        image = self.img
        # 윈도우 생성 및 이미지 표시
        cv2.namedWindow("image")
        cv2.imshow("image", image)

        # 마우스 이벤트 콜백 함수 등록
        cv2.setMouseCallback("image", self.mouse_callback)

        # 키 입력 대기
        cv2.waitKey(0)
    
        if self.times == 4: 
            # 윈도우 종료
            cv2.destroyAllWindows()
        print("Wall Line:", self.wallline)
        print("Paper Line:", self.paperline)
        if self.Direction == 'w':
            return self.wallline[0][0], self.wallline[1][0], self.paperline[0][0], self.paperline[1][0]
        elif self.Direction == 'h':
            return self.wallline[0][1], self.wallline[1][1], self.paperline[0][1], self.paperline[1][1]
# Create an instance of the class
