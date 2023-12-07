from ursina import *

from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

path = "../object/"
app = Ursina()
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

'''
Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20,20))

drag_object = Draggable(parent=scene, scale=.1, model=path+"chair_1.obj", position=(0, 0))

EditorCamera(rotation=(30,10,0))
'''

'''
from ursina import Ursina, Sky, load_model, color, Text, window, Button
app = Ursina(vsync=False, use_ingame_console=True)

e = Entity(model=load_model('cube', use_deepcopy=True), color=color.white, collider='box')
e.model.colorize()

ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=(32,32), collider='box')
box = Entity(model='cube', collider='box', texture='white_cube', scale=(10,2,2), position=(2,1,5), color=color.light_gray)

b = Button(position=window.top_left, scale=.05)
ec = EditorCamera(ignore_scroll_on_ui=True)
rotation_info = Text(position=window.top_left)

def update():
    rotation_info.text = str(int(ec.rotation_y)) + '\n' + str(int(ec.rotation_x))

ground =  Entity(model='plane', scale=32, texture='brick', rotation_x=-90)

'''
#scale (가로,두께,세로)
ground = Entity(model='plane', scale=(50,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(50,50), collider='box')

#scale (두께,높이,길이)
e = Entity(model='cube', scale=(.01,30,100), x=25, y=15, z=0, rotation_y=0, collider='box', texture='white_cube')

e = Entity(model='cube', scale=(.01,30,50), x=0, y=15, z=50, rotation_y=90, collider='box', texture='white_cube')

e = Entity(model='cube', scale=(.01,30,100), x=-25, y=15, z=0, rotation_y=180, collider='box', texture='white_cube')

e = Entity(model='cube', scale=(.01,30,50), x=0, y=15, z=-50, rotation_y=270, collider='box', texture='white_cube')

drag_object = Draggable(parent=scene, scale=1, model=path+"chair_1.obj", position=(0, 0))

e.texture_scale = (e.scale_z, e.scale_y)
EditorCamera(rotation=(30,10,0))

app.run()
