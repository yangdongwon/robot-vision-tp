from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

class VirtualRoom:
	def __init__(self, width, length, height, objectList):
		'''
		self.width = width
		self.length = length
		self.height = height
		self.objectList = objectList
		'''

		self.width = 100.0
		self.length = 100.0
		self.height = 30.0
		self.objectList = ['chair']

		self.objectPath = "../object/"
		self.wallImgPath = "../width_img/"
		self.app = Ursina()

		self.ground = None
		self.wall = None
		self.draggableObjectList = ['chair']

		EditorCamera(rotation=(30,10,0))


	def run(self):
		self.modelRoom()

		self.setObjectMenu()

		self.app.run()


	def modelRoom(self):
		#scale (가로,두께,세로)
		self.ground = Entity(model='plane', scale=(self.length,1,self.width), color=color.white, texture='white_cube', texture_scale=(50,50), collider='box')

		#scale (두께,높이,길이)
#self.wall = Entity(model='cube', scale=(.01,self.height,self.width), x=self.length/2, y=self.height/2, z=0, rotation_y=0, collider='box', texture=self.wallImgPath+'IMG_1190')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.width), x=self.length/2, y=self.height/2, z=0, rotation_y=0, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.length), x=0, y=self.height/2, z=self.width/2, rotation_y=90, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.width), x=-self.length/2, y=self.height/2, z=0, rotation_y=180, collider='box', texture='white_cube')
		self.wall = Entity(model='cube', scale=(.01,self.height,self.length), x=0, y=self.height/2, z=-self.width/2, rotation_y=270, collider='box', texture='white_cube')

		self.wall.texture_scale = (self.wall.scale_z, self.wall.scale_y)

	def setObjectMenu(self):
		for obj in self.objectList:
			if obj in self.draggableObjectList:
				temp = (Draggable(parent=scene, scale=1, model=self.objectPath+obj+"_01.obj", position=(0, 0)))


'''
DropdownMenu('File', buttons=(
    DropdownMenuButton('New'),
    DropdownMenuButton('Open'),
    DropdownMenu('Reopen Project', buttons=(
        DropdownMenuButton('Project 1'),
        DropdownMenuButton('Project 2'),
        )),
    DropdownMenuButton('Save'),
    DropdownMenu('Options', buttons=(
        DropdownMenuButton('Option a'),
        DropdownMenuButton('Option b'),
        )),
    DropdownMenuButton('Exit'),
    ))
'''

vroom = VirtualRoom(25,25,30,None)
vroom.run()
