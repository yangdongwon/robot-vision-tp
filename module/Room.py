import os
from functools import partial

from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

class Room:
	def __init__(self, width, length, height, objectList):
		self.app = Ursina()
		
		self.width = width*100 # cm
		self.length = length*100 # cm
		self.height = height*100 # cm
		self.objectList = objectList
		
		self.objectPath = "./object/"
		self.existObjectList = [f for f in os.listdir(self.objectPath) if os.path.isdir(os.path.join(self.objectPath, f))]

		self.ground = None
		self.wall = None

		self.objectMenu = None
		self.listUI = None
		self.deleteObjectButton = None
		self.currentClickObject = None
		self.count = 0
		self.currentHoldObject = None

		#1920 * 1080
		window.size = (1920,1080)
		EditorCamera(rotation=(30,10,0))


	def run(self):
		self.createRoom()

		self.setObjectMenu()
		self.setObjectListUi()
		self.setObjectList()
		self.setDeleteObjectButton()

		self.app.run()


	# 방 생성
	def createRoom(self):
		#scale (가로,두께,세로)
		self.ground = Entity(model='plane', scale=(self.length,1,self.width), color=color.white, texture='white_cube', texture_scale=(0,0), collider='box')

		#scale (두께,높이,길이)
		self.wall = Entity(model='cube', scale=(1,self.height,self.width), color=color.light_gray, x=self.length/2, y=self.height/2, z=0, rotation_y=0, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.length), color=color.light_gray, x=0, y=self.height/2, z=self.width/2, rotation_y=90, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.width), color=color.light_gray, x=-self.length/2, y=self.height/2, z=0, rotation_y=180, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.length), color=color.light_gray, x=0, y=self.height/2, z=-self.width/2, rotation_y=270, collider='box', texture='white_cube', texture_scale=(0,0))

	# 추출된 객체를 선택할 리스트 생성
	def setObjectMenu(self):
		temp = []
		for obj in self.objectList:
			if obj in self.existObjectList:
				temp.append(DropdownMenuButton(text=obj, on_click=self.listClick))

		self.objectMenu = DropdownMenu(
				'object list',
				parent=camera.ui,
				buttons=(temp),
				scale=(.2,.07),
				position=window.top_right-Vec2(.2,.1)
				)

	# 리스트에서 선택한 객체의 종류를 보여주는 리스트 생성
	def setObjectListUi(self):
		self.listUI = Button(
				name = "listUI",
				parent = camera.ui,
				model = 'quad',
				scale = (.2, .3),
				origin = (-.5, .5),
				position = (-.2,.2),
				texture = 'white_cube',
				texture_scale = (2,3),
				color = color.light_gray,
				visible=False)
		self.listUI.position = window.top_left - Vec2(0,.3)

	def hideUi(self):
		self.listUI.visible=False
		for child in self.listUI.children:
			child.visible = False
			child.disabled=True
			child.enabled=False

	def listClick(self):
		self.hideUi()
		self.currentClickObject = mouse.hovered_entity.text
		invoke(self.selectObject, delay=0.1)

	def selectObject(self):
		self.listUI.visible=True
		for child in self.listUI.children:
			if self.currentClickObject in child.name:
				child.visible = True
				child.disabled=False
				child.enabled=True
		
	def findFreeSpace(self):
		temp = [c for c in self.listUI.children if self.currentClickObject in c.name]
		for y in range(3):
			for x in range(2):
				grid_positions = [(int(e.x*self.listUI.texture_scale[0]), int(e.y*self.listUI.texture_scale[1])) for e in temp]

				if not (x,-y) in grid_positions:
					return x, y

	def findFolder(self):
		path = self.objectPath+self.currentClickObject
		imgFile = []
		objFile = []

		folder = []
		for name in os.listdir(path):
			folder.append(os.path.join(path, name))

		for f in folder:
			if os.path.isdir(f):
				for fn in os.listdir(f):
					fPath = os.path.join(f, fn)

					if fn.lower().endswith(('.jpg', '.jpeg', '.png')):
						imgFile.append(fPath)

					elif fn.lower().endswith('.obj'):
						objFile.append(fPath)

		return imgFile, objFile

	# 리스트에서 선택된 객체의 사진과 오브젝트 파일 로딩 
	def setObjectList(self):
		for objectButton in self.objectMenu.buttons:
			self.currentClickObject = objectButton.text
			imgFile, objFile = self.findFolder()
			
			for img, obj in zip(imgFile, objFile):
				x, y = self.findFreeSpace()

				icon = Button(name = ''.join(img.split('/')[-3:-1]),
						parent = self.listUI,
						model = 'quad',
						texture = img,
						color = color.white,
						scale_x = 1/self.listUI.texture_scale[0],
						scale_y = 1/self.listUI.texture_scale[1],
						origin = (-.5,.5),
						x = x * 1/self.listUI.texture_scale[0],
						y = -y * 1/self.listUI.texture_scale[1],
						z = -.5,
						disabled=True,
						on_click=self.createObject)

				icon_path = Text(text=obj,
						parent=icon,
						visible=False)

	# 선택된 객체 생성
	def createObject(self):
		obj = mouse.hovered_entity
		objChild = obj.children[0]
		objPath = objChild.text

		path = '/'.join(objPath.split('/')[:-2])
		objScale = None
		zPosition = None
		zLock = None
		with open(path+"/setting.txt", "r") as f:
			for line in f:
				string = line.strip().split()
				if string[0] == objPath.split('/')[-2]:
					objScale = float(string[1])
					zPosition = float(string[2])
					zLock = int(string[3])
					break
				if not line:
					print("no setting file in folder!")
					return
		
		draggableObject = Draggable(name=obj.name+"_"+str(self.count),
				parent=scene,
				scale=objScale,
				model=objPath,
				position=(0,zPosition,0),
				collider='box',
				plane_direction=(1,1,1),
				lock=(0,zLock,0),
				on_click=self.holdObject,
				drop=self.deleteObject)
		draggableObject.update = partial(self.update, draggableObject.update)
		draggableObject.input = partial(self.input, draggableObject.input)
		self.count += 1

	def holdObject(self):
		self.currentHoldObject = mouse.hovered_entity

	# 선택된 객체 오른쪽 버튼 클릭시 회전
	def update(self, func):
		func()
		if self.currentHoldObject and self.currentHoldObject == mouse.hovered_entity:
			if self.currentHoldObject.hovered and mouse.right:
				self.currentHoldObject.rotation_y += 0.5

	# 선택된 객체 키보드 위, 아래 화살표로 올리고 내리기
	def input(self, func, key):
		func(key)
		if self.currentHoldObject:
			if key == 'up arrow':
				self.currentHoldObject.position = self.currentHoldObject.position + Vec3(0,2,0)
			elif key == 'down arrow':
				self.currentHoldObject.position = self.currentHoldObject.position - Vec3(0,2,0)

	# 객체를 삭제 버튼으로 드래그시 삭제
	def deleteObject(self):
		if self.deleteObjectButton.hovered and self.currentHoldObject:
			for child in scene.entities:
				if child == self.currentHoldObject:
					destroy(child)
					self.currentHoldObject = None

	def setDeleteObjectButton(self):
		self.deleteObjectButton = Button(
				name = "deleteObjectButton",
				parent = camera.ui,
				model = 'quad',
				text = 'delete\nobject',
				scale = (.1, .1),
				origin = (0,0),
				position = self.objectMenu.position - Vec3(.07,.02,0),
				texture = 'white_cube',
				color = color.dark_gray)
