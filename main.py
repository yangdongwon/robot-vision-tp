from module import FindRoomFeature, Room

f = FindRoomFeature.FindRoomFeature(10.0, 0.6)
f.run()

width, length, height, object_list = f.getParameter()
#r = Room.Room(1165, 725, 270, f.objectList)
print(object_list)
r = Room.Room(width, length, height, object_list)
r.run()
