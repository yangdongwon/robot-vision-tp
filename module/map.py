import os
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

		self.width = 100.0
		self.length = 100.0
		self.height = 30.0
		self.objectList = ['chair', 'clock']

		self.objectPath = "../object/"
		self.existObjectList = [f for f in os.listdir(self.objectPath) if os.path.isdir(os.path.join(self.objectPath, f))]

		self.ground = None
		self.wall = None

		self.currentObject = None
		self.objectMenu = None
		self.listUI = None

		EditorCamera(rotation=(30,10,0))


	def run(self):
		self.createRoom()

		self.setObjectListUi()

		self.setObjectMenu()
#temp = Draggable(parent=scene, scale=1, model=self.objectPath+"clock/Clock.c4d", position=(0, 0))

		self.app.run()


	def createRoom(self):
		#scale (가로,두께,세로)
		self.ground = Entity(model='plane', scale=(self.length,1,self.width), color=color.white, texture='white_cube', texture_scale=(50,50), collider='box')

		#scale (두께,높이,길이)
		self.wall = Entity(model='cube', scale=(.01,self.height,self.width), x=self.length/2, y=self.height/2, z=0, rotation_y=0, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.length), x=0, y=self.height/2, z=self.width/2, rotation_y=90, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.width), x=-self.length/2, y=self.height/2, z=0, rotation_y=180, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.length), x=0, y=self.height/2, z=-self.width/2, rotation_y=270, collider='box', texture='white_cube')

		self.wall.texture_scale = (self.wall.scale_z, self.wall.scale_y)

	def setObjectMenu(self):
		temp = []
		for obj in self.objectList:
			if obj in self.existObjectList:
				temp.append(DropdownMenuButton(obj, on_click=self.listClick))

		self.objectMenu = DropdownMenu('object list', buttons=(temp), parent=Draggable(model=Quad(), scale_x=.2,scale_y=.1, position=window.top_right/2), scale_x=1.5, scale_y=1)
		self.objectMenu.position = self.objectMenu.position+Vec2(.4,0)

	def setObjectListUi(self):
		self.listUI = Draggable(parent = camera.ui, model = 'quad', scale = (.4, .3), origin = (-.5, .5), position = (-.2,.2), texture = 'white_cube', texture_scale = (3,2), color = color.light_gray, visible=False)

	def initList(self):
		for child in self.listUI.children:
			destroy(child)

	def listClick(self):
		self.listUI.visible=False
		self.initList()
		self.currentObject = mouse.hovered_entity.text
		invoke(self.selectObject, delay=0.1)

	def selectObject(self):
		self.listUI.visible=True
		self.setObjectList()
	
	def findFreeSpace(self):
		for y in range(2):
			for x in range(3):
				grid_positions = [(int(e.x*self.listUI.texture_scale[0]), int(e.y*self.listUI.texture_scale[1])) for e in self.listUI.children]

				if not (x,-y) in grid_positions:
					return x, y

	def findFolder(self):
		path = self.objectPath+self.currentObject
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

			icon = Button(name = ''.join(img.split('/')[-3:-1]), parent = self.listUI, model = 'quad', texture = img, color = color.white, scale_x = 1/self.listUI.texture_scale[0], scale_y = 1/self.listUI.texture_scale[1], origin = (-.5,.5), x = x * 1/self.listUI.texture_scale[0], y = -y * 1/self.listUI.texture_scale[1], z = -.5, on_click=self.createObject)

	def createObject(self):
		print(mouse.hovered_entity.name)
		#temp = Draggable(parent=scene, scale=1, model=self.objectPath+"chair/chair_01.obj", position=(0, 0))

	def deleteObject(self):
		pass

vroom = VirtualRoom(25,25,30,None)
vroom.run()
