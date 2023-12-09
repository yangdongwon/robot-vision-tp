from module import FindRoomFeature, Room

f = FindRoomFeature.FindRoomFeature(10.0, 0.8)
f.run()

#r = Room.Room(f.getParameter())
r = Room.Room(1165, 725, 270, f.objectList)
r.run()
