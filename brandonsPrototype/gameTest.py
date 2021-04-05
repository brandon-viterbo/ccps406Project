import gameClasses

centreRoom = gameClasses.Room("r000")
northRoom = gameClasses.Room("r001")
southRoom = gameClasses.Room("r002")
eastRoom = gameClasses.Room("r003")
westRoom = gameClasses.Room("r004")
lockedRoom = gameClasses.Room("r005")
batRoom = gameClasses.Room("r006")
boulderRoom = gameClasses.Room("r007")
finalRoom = gameClasses.Room("r008")

door = gameClasses.Obstacle("o000_door")
bats = gameClasses.Obstacle("o001_bats")
boulder = gameClasses.Obstacle("o002_boulder")

torch = gameClasses.Item("i000_torch")
key = gameClasses.Item("i001_key")

pix = gameClasses.Character("c000_pix")
marine = gameClasses.Character("c001_marine")


pix.activeCharacter(1)
print("Pix's inventory has: ", pix.inventory) # Nothing
print("This room has: ", pix.locationObject.items) # Torch
pix.take(torch) # Takes the torch
print("Pix's inventory has: ", pix.inventory) # Torch
print("This room has: ", pix.locationObject.items, "\n") # Nothing

pix.move("W") # Entered West Room, followed by cutscene
print("Pix's inventory has: ", pix.inventory) # Torch
print("This room has: ", pix.locationObject.items) # Key
pix.drop(torch) # Dropped the torch
print("Pix's inventory has: ", pix.inventory) # Nothing
print("This room has: ", pix.locationObject.items, "\n") # Key and torch

pix.move("E") # Enter Centre Room, no cutscene
print("Pix's inventory has: ", pix.inventory) # Nothing
print("This room has: ", pix.locationObject.items, "\n") # Nothing

pix.move("W") # Enter West Room, no cutscene
print("Pix's inventory has: ", pix.inventory) # Nothing
print("This room has: ", pix.locationObject.items) # key, torch
pix.take(torch) # Pix takes torch
pix.take(key) # Pix takes key
print("Pix's inventory has: ", pix.inventory) # Torch and key
print("This room has: ", pix.locationObject.items, "\n") # Nothing

pix.move("W") # Door blocks way, still in West Room
pix.move("W") # Door blocks way, still in West Room
print("Pix's inventory has: ", pix.inventory) # Torch and key
pix.wield(torch) # Pix wields Torch
print("Pix's inventory has: ", pix.inventory) # Key
pix.move("W") # Door blocks way, still in West Room
pix.wield(key) # Pix wields key
print("Pix's inventory has: ", pix.inventory, "\n") # Torch

pix.wield(torch) # Pix wields torch
print("Is torch activated? {}".format(torch.activated)) # False
pix.activate("eat", torch) # Pix doesn't know how to do that
pix.activate("LIGHT", torch) # Pix lights the torch
print("Is torch activated? {}".format(torch.activated)) # True
pix.activate("LIGHT", torch) # Torch is already lit
print("Is torch activated? {}".format(torch.activated), "\n") # True

pix.activate("EXTINGUISH", torch) # Pix puts out torch
print("Is torch activated? {}".format(torch.activated)) # False
pix.activate("eat", torch) # Pix doesn't know how to do that
print("Is torch activated? {}".format(torch.activated)) # False
pix.activate("LIGHT", torch) # Pix lights torch
print("Is torch activated? {}".format(torch.activated), "\n") # True

pix.wield(key) # Pix wields key
print("Is key activated? {}".format(key.activated)) # False
pix.activate("eat", key) # Pix doesn't know how to do that
print("Is key activated? {}".format(key.activated)) # False
pix.activate("NULL", key) # Pix doesn't know how to do that
print("Is key activated? {}".format(key.activated)) # False
pix.wield(torch) # Pix wields torch
print("Is torch activated? {}".format(torch.activated)) # True
pix.wield(torch)
pix.move("W")
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles) # Door to the west
pix.removeObstacle("UNLOCK", door) # Failed to unlock, the torch isn't a key
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles, "\n") # Door to the west

pix.wield(key)
pix.move("W")
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles) # Door to the west
pix.removeObstacle("UNLOCK", door) # Unlocks door
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles) # None
pix.move("W")
print("\n")

pix.move("W")
pix.move("N")
pix.move("S")
pix.move("E")
pix.move("W")
pix.move("W")
pix.removeObstacle("SCARE", bats)
pix.wield(torch)
pix.activate("EXTINGUISH", torch)
pix.removeObstacle("SCARE", bats)
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles)
pix.activate("LIGHT", torch)
pix.removeObstacle("SCARE", bats)
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles, "\n")

pix.move("W")
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles)
print("Characters in this room: ", pix.locationObject.characters)
pix.removeObstacle("PUSH", boulder)
pix.move("N")
marine.removeObstacle("politely talk with", boulder)
pix.move("N")
marine.removeObstacle("PUSH", boulder)
pix.recruit(marine) #add marine to pix's party and vice versa
print(pix.party)  
print(marine.party)
print("Obstacles in this room: ", pix.locationObject.adjRoomObstacles)
print("Characters in this room: ", pix.locationObject.characters, "\n")

pix.move("N")
print("Characters in this room: ", pix.locationObject.characters)
pix.move("S")
print("Characters in this room: ", pix.locationObject.characters)
pix.talk(marine)