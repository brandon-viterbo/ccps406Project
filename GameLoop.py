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
    singleActionSuccessful = gameplayMessages["singleAction"]["successfulText"]
    singleActionUnsuccessful = gameplayMessages["singleAction"]["unsuccessfulText"]
    singleActionInvalid = gameplayMessages["singleAction"]["messageInvalid"]

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
        self.playerCharacter = False
        self.emotionalState = "happy"

        self.name = thisCharacterData["name"]
        self.dialogue = thisCharacterData["dialogue"]
        self.strength = thisCharacterData["strength"]
        self.weight = thisCharacterData["weight"]
        self.inventory = thisCharacterData["inventory"]
        self.wieldedItem = thisCharacterData["wieldedItem"]
        self.locationID = thisCharacterData["locationID"]
        self.locationObject = Room._registry[self.locationID]
        self.party = thisCharacterData["party"]


    def take(self, item):
        """Action Type: objAction"""
        verb = "took"
        count = 0

        if item.itemID not in self.locationObject.items:
            print(objActionInvalid.format(self.name, verb, item.name))
            return

        for i in self.inventory:
            if i == NULL_TAG:
                self.inventory[count] = item.itemID
                print(objActionSuccessful.format(self.name, verb, item.name))
                self.locationObject.items.remove(item.itemID)
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, verb, item.name))
    
    def recruit(self, charName):
      count = 0
      if charName.charID not in self.locationObject.characters:
            print("That character can't join you right now.")
            return 

      for i in self.party:
            if i == NULL_TAG:
                self.party[count] = charName
                charName.party[count] = self
                print(charName.name + " joined the party!")
                return
            count += 1
      print("That character can't join you right now.")


    def drop(self, item):
        """Type: objAction"""
        verb = "dropped"
        count = 0
        if self.wieldedItem == item.itemID:
            self.wieldedItem = NULL_TAG
            self.locationObject.items.append(item.itemID)
            print(objActionSuccessful.format(self.name, verb, item.name))
            return

        for i in self.inventory:
            if i == item.itemID:
                print(objActionSuccessful.format(self.name, verb, 
                    item.name))
                self.inventory[count] = NULL_TAG
                self.locationObject.items.append(item.itemID)
                return
            count += 1
        print(objActionInvalid.format(self.name, verb, item.name))
        return


    def wield(self, item):
        count = 0
        for i in self.inventory:
            if i == item.itemID:
                if self.wieldedItem != NULL_TAG:
                    self.inventory[count] = self.wieldedItem
                else:
                    self.inventory[count] = NULL_TAG
                self.wieldedItem = item.itemID
                print(objActionSuccessful.format(
                    self.name, "wielded", item.name)
                )
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, "wield", item.name))


    def activate(self, item):
      if item.itemID == self.wieldedItem:
        print(objActionSuccessful.format(self.name, "used", item.name))
        print(item.activatedText)
        pass
        if self.locationID == item.usableRooms:
          print(self.locationObject.itemUsed)
          self.unlock(item.unlockableRoomDirection)
        else:
          print("This item won't do anything here")
          print(item.deactivatedText)

      else:
        print(objActionUnsuccessful.format(self.name, "wield", item.name))
        pass

    def move(self, direction):
        """Action Type: Entering Room"""
        nextRoomID = self.locationObject.adjRooms[direction]
        if nextRoomID == NULL_TAG:
            print(enteringRoomInvalid.format(direction, self.name, 
                self.locationObject.name))
            return

        nextRoomObject = Room._registry[nextRoomID]

        if self.locationObject.skillRequirements[direction] != "NULL":
          if self.locationObject.skillRequirements[direction]["strength"] > self.strength:
            print("You are too weak to clear the obstacle!")
            return
          if self.locationObject.skillRequirements[direction]["weight"] > self.weight:
            print("You are too heavy to clear the obstacle!")
            return

        if self.locationObject.adjRoomOpen[direction] == False:
            print(enteringRoomUnsuccessful.format(self.name, direction, 
                self.name, self.locationObject.name))
            return

        self.locationObject.characters.remove(self.charID) 
        if self.party[0] != NULL_TAG:
          self.locationObject.characters.remove(self.party[0].charID)
        self.locationObject = nextRoomObject
        self.locationID = nextRoomID
        self.locationObject.characters.append(self.charID)
        if self.party[0] != NULL_TAG:
          self.locationObject.characters.append(self.party[0].charID)
        print(enteringRoomSuccessful.format(self.name, self.locationObject.name))
        if self.locationObject.playerVisited == False:
            print(self.locationObject.entryCutscene)
            self.locationObject.playerVisited = True  
        return


    def unlock(self, direction):
        nextRoomKey = self.locationObject.adjRoomKeys[direction]
        nextRoomOpen = self.locationObject.adjRoomOpen[direction]

        if (nextRoomKey == NULL_TAG) or (nextRoomKey != self.wieldedItem):
            print(singleActionInvalid.format(self.name, "do that"))
            return
        if (self.wieldedItem == nextRoomKey) and (nextRoomOpen == False):
            print("{} can now move {}.".format(self.name, direction))
            self.locationObject.adjRoomOpen[direction] = True
            return
    
    def activeCharacter(self, active):
      if active == 1:
        self.playerCharacter=True
        print (self.name + " is now the player character.")
      if active == 0:
        self.playerCharacter=False
        print (self.name + " is no longer the player character.")
    
    def emotionState(self, emotion):
      if emotion == "happy":
        self.emotionalState="happy"
      if emotion == "concerned":
        self.emotionalState="concerned"
      if emotion == "idle":
        self.emotionalState="idle"
      if emotion == "focused":
        self.emotionalState="focused"
      if emotion == "angry":
        self.emotionalState="angry"
 
    def talk (self, charName):
      if (charName.playerCharacter == False):
        print (charName.name + ": " + charName.dialogue[charName.emotionalState])
      else:
        print ("Why am I talking to myself?")
      



class Item():
    _registry = {}

    def __init__(self, itemID):
        self._registry[itemID] = self
        self.itemID = itemID
        thisItemData = allItemData[itemID]

        self.usableRooms = thisItemData["usableRooms"]
        self.unlockableRoomDirection = thisItemData["unlockableRoomDirection"]
        self.name = thisItemData["name"]
        self.messages = thisItemData["messages"]
        self.weight = thisItemData["weight"]
        self.activated = thisItemData["activated"]
        self.activatedText = thisItemData["messages"]["itemActivated"]
        self.deactivatedText = thisItemData["messages"]["itemDeactivated"]



class Room():
    _registry = {}

    def __init__(self, roomID):
        self._registry[roomID] = self
        self.roomID = roomID
        thisRoomData = allRoomData[roomID]

        self.name = thisRoomData["name"]
        self.adjRooms = thisRoomData["adjRooms"]
        self.adjRoomOpen = thisRoomData["adjRoomOpen"]
        self.adjRoomKeys = thisRoomData["adjRoomKeys"]

        # List of instances of Item class inside of self
        self.items = thisRoomData["items"]
        # List of instances of Character class inside of self
        self.characters = thisRoomData["characters"]

        self.playerVisited = thisRoomData["playerVisited"]
        self.entryCutscene = thisRoomData["entryCutscene"]

        self.itemUsed = thisRoomData["itemUsed"]
        self.skillRequirements = thisRoomData["skillRequirements"]

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
batRoom = Room("r006")
boulderRoom = Room("r007")
finalRoom = Room("r008")
torch = Item("i000")
key = Item("i001")
pix = Character("c000")
marine = Character("c001")
 
def take():
  arg = inputArgs[1]
  if arg == "torch":
    pix.take(torch)
  else:
    print("I can't take that!")
  pass
    
def check():
  arg = inputArgs[1]
  if arg == "inventory":
    print("Pix's inventory: {}".format(pix.inventory))
  elif arg == "items":
    print("Items in current room: {}\n".format(pix.locationObject.items))
  else:
    print("I can't check that.")
  pass

def north():
  pix.move("N")
    
def east():
  pix.move("E")
    
def south():
  pix.move("S")
    
def west():
  pix.move("W")

def wield():
  arg = inputArgs[1]
  if arg == "torch":
    pix.wield(torch)
  else:
    print("I can't wield that!")

def drop():
  arg = inputArgs[1]
  if arg == "torch":
    pix.drop(torch)
  else:
    print("I can't drop that!")

print(pix.locationObject.entryCutscene)
while(1):
  userIn = input()
  inputArgs = userIn.split()
        #print(inputArgs)

  switcher = {
    "take": take,
    "check": check,
    "N": north,
    "E": east,
    "S": south,
    "W": west,
    "wield": wield,
    "drop": drop
    }

  if (inputArgs[0] in switcher):
    switcher[inputArgs[0]]()
  else:
    print("I can't do that!")
