import json

GAMEPLAY_MESSAGES_RAW = "gameplayMessages.json"
CHARACTERS_RAW = "characters.json"
ROOMS_RAW = "rooms.json"
ITEMS_RAW = "items.json"

DIRECTIONS = ["N", "S", "E", "W"]

HAPPY = "happy"
CONCERNED = "concerned"
IDLE = "idle"
FOCUSED = "focused"
ANGRY = "angry"
CHARACTER_EMOTIONAL_STATES = [HAPPY, CONCERNED, IDLE, FOCUSED, ANGRY]

NULL_TAG = "NULL"

with open(GAMEPLAY_MESSAGES_RAW, "r") as readFile:
    gameplayMessages = json.load(readFile)
    enteringRoomSuccessful = gameplayMessages["enteringRoom"]["successfulText"]
    enteringRoomUnsuccessful = gameplayMessages["enteringRoom"]["unsuccessfulText"]
    enteringRoomInvalid = gameplayMessages["enteringRoom"]["messageInvalid"]
    objActionSuccessful = gameplayMessages["objAction"]["successfulText"]
    objActionUnsuccessful = gameplayMessages["objAction"]["unsuccessfulText"]
    objActionInvalid = gameplayMessages["objAction"]["messageInvalid"]

with open(CHARACTERS_RAW, "r") as readFile:
    allCharacterData = json.load(readFile)

with open(ROOMS_RAW, "r") as readFile:
    allRoomData = json.load(readFile)

with open(ITEMS_RAW, "r") as readFile:
    allItemData = json.load(readFile)


class Character():
    _registry = {}

    def __init__(self, charID):
        self._registry[charID] = self
        self.charID = charID
        thisCharacterData = allCharacterData[charID]

        self.name = thisCharacterData["name"]
        self.dialogue = thisCharacterData["dialogue"]
        self.strength = thisCharacterData["strength"]
        self.weight = thisCharacterData["weight"]
        self.inventory = thisCharacterData["inventory"]
        self.wieldedItem = thisCharacterData["wieldedItem"]
        self.locationID = thisCharacterData["locationID"]
        self.locationObject = Room._registry[self.locationID]


    def take(self, item):
        """Action Type: objAction"""
        verb = "took"
        count = 0

        if item.itemID not in self.locationObject.items:
            print(objActionInvalid.format(self.name, verb, item.name))

        for i in self.inventory:
            if i == NULL_TAG:
                self.inventory[count] = item.itemID
                print(objActionSuccessful.format(self.name, verb, item.name))
                self.locationObject.items.remove(item.itemID)
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, verb, item.name))


    def drop(self, item):
        """Type: objAction"""
        verb = "dropped"
        count = 0
        for i in self.inventory:
            if i != NULL_TAG:
                if i == item.itemID:
                    print(objActionSuccessful.format(self.name, verb, 
                        item.name))
                    self.inventory[count] = NULL_TAG
                    self.locationObject.items.append(item.itemID)
                    return
            count += 1
        print(objActionInvalid.format(self.name, verb, item.name))


    def wield(self, item):
        pass


    def move(self, direction):
        """Action Type: Entering Room"""
        nextRoomID = self.locationObject.adjRooms[direction]
        if nextRoomID == NULL_TAG:
            print(enteringRoomInvalid.format(direction, self.name, 
                self.locationObject.name))
            return

        nextRoomObject = Room._registry[nextRoomID]
        if self.locationObject.adjRoomOpen[direction] == False:
            print(enteringRoomUnsuccessful.format(self.name, direction, 
                self.name, self.locationObject.name))
            return

        self.locationObject.characters.remove(self.charID)
        self.locationObject = nextRoomObject
        self.locationID = nextRoomID
        self.locationObject.characters.append(self.charID)
        print(enteringRoomSuccessful.format(self.name, self.locationObject.name))
        if self.locationObject.playerVisited == False:
            print(self.locationObject.entryCutscene)
            self.locationObject.playerVisited = True



class Item():
    _registry = {}

    def __init__(self, itemID):
        self._registry[itemID] = self
        self.itemID = itemID
        thisItemData = allItemData[itemID]

        self.name = thisItemData["name"]
        self.messages = thisItemData["messages"]
        self.weight = thisItemData["weight"]
        self.activated = thisItemData["activated"]



class Room():
    _registry = {}

    def __init__(self, roomID):
        self._registry[roomID] = self
        self.roomID = roomID
        thisRoomData = allRoomData[roomID]

        self.name = thisRoomData["name"]
        self.adjRooms = thisRoomData["adjRooms"]
        self.adjRoomOpen = thisRoomData["adjRoomOpen"]

        # List of instances of Item class inside of self
        self.items = thisRoomData["items"]
        # List of instances of Character class inside of self
        self.characters = thisRoomData["characters"]

        self.playerVisited = thisRoomData["playerVisited"]
        self.entryCutscene = thisRoomData["entryCutscene"]


    def set_room_id(self, roomID):
        self.roomID = roomID
    def get_room_id(self):
        return self.roomID



centreRoom = Room("r000")
northRoom = Room("r001")
southRoom = Room("r002")
eastRoom = Room("r003")
westRoom = Room("r004")
lockedRoom = Room("r005")

torch = Item("i000")

pix = Character("c000")


"""Each statement below is followed by the expected output"""

print(pix.locationObject.entryCutscene) # Entry cutscene
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}\n".format(pix.locationObject.items)) #Item id for torch

pix.take(torch) # Pix takes torch
print("Pix's inventory: {}".format(pix.inventory)) #Torch
print("Items in current room: {}\n".format(pix.locationObject.items)) #Empty

pix.drop(torch) # Pix drops torch
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}\n".format(pix.locationObject.items)) #Item id for torch

pix.drop(torch) # Invalid item message
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}\n".format(pix.locationObject.items)) #Item id for torch

pix.take(torch) # Pix takes torch
print("Pix's inventory: {}".format(pix.inventory)) #Torch
print("Items in current room: {}\n".format(pix.locationObject.items)) #Empty
previousRoom = pix.locationObject

pix.move("N") # "Pix entered North Room", followed by entry cutscene
pix.move("N") # Nowhere north to go
pix.drop(torch) # Pix dropped the torch
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}".format(pix.locationObject.items)) #Item ID for torch
print("Items in previous room: {}\n".format(previousRoom.items)) #Empty, refer to lines 192-195

pix.move("S") # Pix entered Centre Room
pix.move("W") # "Pix entered West Room", followed by entry cutscene
pix.move("W") # Can't enter the area to the W.
pix.move("E") # Pix entered Centre Room
pix.move("W") # "Pix entered West Room", NOT followed by entry cutscene
pix.move("E") # Pix entered Centre Room
pix.move("E") # Pix entered East Room, followed by entry cutscene