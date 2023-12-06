from ursina import *
from ursina import Ursina, Entity
from ursina import Tooltip

app = Ursina()


from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

d = DropdownMenu('Object list', buttons=(
	DropdownMenuButton('chair'),
	DropdownMenuButton('clock'),
	), parent=Draggable(model=Quad(), scale_x=.3,scale_y=.1), scale_x=2, scale_y=1, position=window.center_on_screen)

d.position = d.position+Vec2(1.5,0)

'''
d = DropdownMenu('Object list', buttons=(
	DropdownMenuButton('chair'),
	DropdownMenuButton('clock'),
	))

'''

EditorCamera(rotation=(30,10,0))
app.run()
