from module import FindRoomFeature, Room

f = FindRoomFeature.FindRoomFeature(10.0, 0.6)
f.run()

width, length, height, object_list = f.getParameter()
r = Room.Room(width, length, height, object_list)
r.run()
