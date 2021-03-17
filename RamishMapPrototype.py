import json

startingMapID = 0
GAMEPLAY_MESSAGES_RAW = "gameplayMessages.json"
CHARACTER_RAW = "characters.json"
ROOMS_RAW = "rooms.json"
ROOM_DATA_RAW = "roomdata.json"


with open(GAMEPLAY_MESSAGES_RAW, "r") as readFile:
    gameplayMessages = json.load(readFile)
    textEnterRoom = gameplayMessages["enteringRoom"]["successfulText"]
    objActionSuccessful = gameplayMessages["objAction"]["successfulText"]
    objActionUnsuccessful = gameplayMessages["objAction"]["unsuccessfulText"]

with open(ROOMS_RAW, 'r') as readFile:
    roomMessages = json.load(readFile)
    roomName = roomMessages[startingMapID]["roomName"]

with open(ROOM_DATA_RAW, 'r') as readFile:
    roomData = json.load(readFile)


class Character():
    def __init__(self, name="", dialogue={}, strength=0, weight=0, 
        inventory=1, wieldedItem=None, location=None):
        """Integer "inventory" in arguments is the capactity of Character's
        inventory. The actual inventory is an array with that number of
        slots all initialized to None.
        """
        self.name = name
        self.dialogue = dialogue
        self.strength = strength
        self.weight = weight
        self.inventory = [None] * inventory
        self.wieldedItem = None
        self.location = location

    def take(self, item):
        """Type: objAction"""
        verb = "took"
        count = 0
        for i in self.inventory:
            if i == None:
                self.inventory[count] = item
                print(objActionSuccessful.format(self.name, verb, item.name))
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, verb, item.name))

    def drop(self, item):
        """Type: objAction"""
        verb = "dropped"
        count = 0
        for i in self.inventory:
            if i != None:
                if i.name == item.name:
                    print(objActionSuccessful.format(self.name, verb, 
                        item.name))
                    self.inventory[count] = None
                    return
            count += 1
        print(objActionUnsuccessful.format(self.name, verb, item.name))            

class Item():
    def __init__(self, name="", messages={}, weight=0):
        self.name = name
        self.messages = messages
        self.weight = weight

    def __str__():
    	print(self.name)


class Room():
    def __init__(self):
        self.roomID = 0
        self.roomPassable = roomData[str(self.roomID)]["passability"]
        self.adjRooms = roomData[str(self.roomID)]["adjacentRooms"]
        self.adjLockedRooms = roomData[str(self.roomID)]["adjacentLockedRooms"]
    def set_room_id(self,x):
        self.roomID = x
    def get_room_id(self):
        return self.roomID
    def changeRoom (self, direction):
        if(direction == "N" and self.roomPassable[0]==1):
          if(self.adjLockedRooms[0]==1):
            lockedRoomNorth = roomMessages[self.roomID]["lockedNorth"]
            return(lockedRoomNorth.format())
          unlockedRoomNorth = roomMessages[self.roomID]["lockedNorth"]
          self.set_room_id(self.adjRooms[0])
          return unlockedRoomNorth
        elif(direction == "E" and self.roomPassable[1]==1):
          if(self.adjLockedRooms[1]==1):
            lockedRoomEast = roomMessages[self.roomID]["lockedEast"]
            return(lockedRoomEast.format())
          unlockedRoomEast = roomMessages[self.roomID]["lockedEast"]
          self.set_room_id(self.adjRooms[1])
          return unlockedRoomEast
        elif(direction == "S" and self.roomPassable[2]==1):
          if(self.adjLockedRooms[2]==1):
            lockedRoomSouth = roomMessages[self.roomID]["lockedSouth"]
            return(lockedRoomSouth.format())
          unlockedRoomSouth = roomMessages[self.roomID]["lockedSouth"]
          self.set_room_id(self.adjRooms[2])
          return unlockedRoomSouth
        elif(direction == "W" and self.roomPassable[3]==1):
          if(self.adjLockedRooms[0]==1):
            lockedRoomWest = roomMessages[self.roomID]["lockedWest"]
            return(lockedRoomWest.format())
          unlockedRoomWest = roomMessages[self.roomID]["lockedWest"]
          self.set_room_id(self.adjRooms[3])
          return unlockedRoomWest
        else:
            retStr = ("Can't go in that direction!")
            return retStr

    def unlockRoom (self,direction):
      if(direction == "N"):
        self.adjLockedRooms[0]=0
        return ("Room was unlocked!")
      if(direction == "E"):
        self.adjLockedRooms[1]=0
        return ("Room was unlocked!")
      if(direction == "S"):
        self.adjLockedRooms[2]=0
        return ("Room was unlocked!")
      if(direction == "W"):
        self.adjLockedRooms[3]=0
        return ("Room was unlocked!")

    def firstEntryCutscene (self, mapID):
      firstEntryCutscene = roomMessages[mapID]["firstEntryCutscene"]
      return(firstEntryCutscene.format())
    def look (self, mapID):
      longDescription = roomMessages[startingMapID]["longDescription"]
      return(longDescription.format())

torch = Item(name="torch")

pix = Character(name="Pix", dialogue={}, strength=0, weight=0, inventory=5,
    wieldedItem=None, location=None)

x=Room()
print(x.firstEntryCutscene(0))
print(x.look(0))
print(x.changeRoom("S"))
print(x.unlockRoom("S"))
print(x.changeRoom("S"))