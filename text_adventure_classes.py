import json

GAMEPLAY_MESSAGES_RAW = "gameplayMessages.json"
CHARACTER_RAW = "characters.json"


with open(GAMEPLAY_MESSAGES_RAW, "r") as readFile:
    gameplayMessages = json.load(readFile)
    textEnterRoom = gameplayMessages["enteringRoom"]["successfulText"]
    objActionSuccessful = gameplayMessages["objAction"]["successfulText"]
    objActionUnsuccessful = gameplayMessages["objAction"]["unsuccessfulText"]



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
        self.roomPassable = [0,1,1,0]
        self.adjRooms = [None,2,3,None]
    def set_room_id(self,x):
        self.roomID = x
    def get_room_id(self):
        return self.roomID
    def changeRoom (self, direction):
        if(direction == "N" and self.roomPassable[0]==1):
            self.set_room_id(self.adjRooms[0])
            retStr = (self.roomID)
            return retStr
        elif(direction == "E" and self.roomPassable[1]==1):
            self.set_room_id(self.adjRooms[1])
            retStr = (self.roomID)
            return retStr
        elif(direction == "S" and self.roomPassable[2]==1):
            self.set_room_id(self.adjRooms[2])
            retStr = (self.roomID)
            return retStr
        elif(direction == "W" and self.roomPassable[3]==1):
            self.set_room_id(self.adjRooms[3])
            retStr = (self.roomID)
            return retStr
        else:
            retStr = ("Can't go in that direction!")
            return retStr

torch = Item(name="torch")

pix = Character(name="Pix", dialogue={}, strength=0, weight=0, inventory=5,
    wieldedItem=None, location=None)

x=Room()
print(x.get_room_id())
print(x.changeRoom("N"))
print(x.changeRoom("E"))
print(x.changeRoom("S"))
print(x.changeRoom("W"))
