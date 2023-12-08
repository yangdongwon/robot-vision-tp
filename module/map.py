import os
from functools import partial
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

class VirtualRoom:
	def __init__(self, width, length, height, objectList):
		self.app = Ursina()
		'''
		self.width = width
		self.length = length
		self.height = height
		self.objectList = objectList
		'''

		self.width = 11.65*100
		self.length = 7.25*100
		self.height = 2.7*100
		self.objectList = ['chair', 'clock', 'desk']

		self.objectPath = "../object/"
		self.existObjectList = [f for f in os.listdir(self.objectPath) if os.path.isdir(os.path.join(self.objectPath, f))]

		self.ground = None
		self.wall = None

		self.objectMenu = None
		self.listUI = None
		self.deleteObjectButton = None
		self.currentClickObject = None
		self.count = 0
		self.currentHoldObject = None

		EditorCamera(rotation=(30,10,0))


	def run(self):
		window.size = window.fullscreen_size

		self.createRoom()

		self.setObjectListUi()
		self.setDeleteObjectButton()

		self.setObjectMenu()
#temp = Draggable(parent=scene, model=self.objectPath+"desk/1/desk.obj", scale=.065, position=(0, 0), collider='box')

		self.app.run()


	def createRoom(self):
		#scale (가로,두께,세로)
		self.ground = Entity(model='plane', scale=(self.length,1,self.width), color=color.white, texture='white_cube', texture_scale=(0,0), collider='box')

		#scale (두께,높이,길이)
		self.wall = Entity(model='cube', scale=(1,self.height,self.width), color=color.light_gray, x=self.length/2, y=self.height/2, z=0, rotation_y=0, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.length), color=color.light_gray, x=0, y=self.height/2, z=self.width/2, rotation_y=90, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.width), color=color.light_gray, x=-self.length/2, y=self.height/2, z=0, rotation_y=180, collider='box', texture='white_cube', texture_scale=(0,0))
		self.wall = Entity(model='cube', scale=(1,self.height,self.length), color=color.light_gray, x=0, y=self.height/2, z=-self.width/2, rotation_y=270, collider='box', texture='white_cube', texture_scale=(0,0))

	def setObjectMenu(self):
		temp = []
		for obj in self.objectList:
			if obj in self.existObjectList:
				temp.append(DropdownMenuButton(obj, on_click=self.listClick))

		self.objectMenu = DropdownMenu(
				'object list',
				buttons=(temp),
				parent=Draggable(model=Quad(), scale_x=.15,scale_y=.05, position=window.top_right/2),
				scale_x=1.2,
				scale_y=1,
				)
		self.objectMenu.position = self.objectMenu.position+Vec2(.4,0)

	def setObjectListUi(self):
		self.listUI = Draggable(
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

	def setDeleteObjectButton(self):
		self.deleteObjectButton = Draggable(
				name = "deleteObjectButton",
				parent = camera.ui,
				model = 'quad',
				text = 'delete\nobject',
				scale = (.1, .1),
				origin = (0,0),
				position = window.top_right/2 - Vec2(.2,0),
				texture = 'white_cube',
				color = color.dark_gray)

	def hideUi(self):
		self.listUI.visible=False

	def initList(self):
		for child in self.listUI.children:
			destroy(child)

	def listClick(self):
		self.hideUi()
		self.initList()
		self.currentClickObject = mouse.hovered_entity.text
		invoke(self.selectObject, delay=0.1)

	def selectObject(self):
		self.listUI.visible=True
		self.setObjectList()
	
	def findFreeSpace(self):
		for y in range(3):
			for x in range(2):
				grid_positions = [(int(e.x*self.listUI.texture_scale[0]), int(e.y*self.listUI.texture_scale[1])) for e in self.listUI.children]

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

	def setObjectList(self):
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
					on_click=self.createObject)

			icon_path = Text(text=obj,
					parent=icon,
					visible=False)

	def createObject(self):
		obj = mouse.hovered_entity
		objChild = obj.children[0]
		objPath = objChild.text

		path = self.objectPath + self.currentClickObject
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
		draggableObject.update = partial(self.rotateObject, draggableObject.update)
		self.count += 1

	def holdObject(self):
		self.currentHoldObject = mouse.hovered_entity

	def rotateObject(self, func):
		func()
		if self.currentHoldObject and self.currentHoldObject == mouse.hovered_entity:
			if self.currentHoldObject.hovered and mouse.right:
				self.currentHoldObject.rotation_y += 1

	def deleteObject(self):
		if self.deleteObjectButton.hovered and self.currentHoldObject:
			for child in scene.entities:
				if child == self.currentHoldObject:
					self.currentHoldObject = None
					destroy(child)

vroom = VirtualRoom(25,25,30,None)
vroom.run()
