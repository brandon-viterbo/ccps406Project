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


"""Each statement below is followed by the expected output"""

print(pix.locationObject.entryCutscene) # Entry cutscene
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}\n".format(pix.locationObject.items)) #Item id for torch

pix.take(torch) # Pix takes torch
print("Pix's inventory: {}".format(pix.inventory)) #Torch
print("Items in current room: {}".format(pix.locationObject.items)) #Empty
print("Pix is wielding a {}\n".format(pix.wieldedItem)) # NULL

pix.wield(torch)
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}".format(pix.locationObject.items)) #Empty
print("Pix is wielding a {}\n".format(pix.wieldedItem)) # Torch

pix.drop(torch) # Pix drops torch
print("Pix's inventory: {}".format(pix.inventory)) #Empty
print("Items in current room: {}".format(pix.locationObject.items)) #Item id for torch
print("Pix is wielding a {}\n".format(pix.wieldedItem)) # Empty

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
print("\n")
pix.move("W")
pix.take(torch)
pix.take(key)
pix.move("N")
pix.take(torch)
pix.move("S")
pix.move("W")
pix.take(key)
print("Pix's inventory: {}".format(pix.inventory)) #Torch, key
print("Items in current room: {}".format(pix.locationObject.items)) #Empty
print("Pix is wielding a {}\n".format(pix.wieldedItem)) # Empty
pix.wield(torch)
print("Pix's inventory: {}".format(pix.inventory)) #Key
print("Items in current room: {}".format(pix.locationObject.items)) #Empty
print("Pix is wielding a {}\n".format(Item._registry[pix.wieldedItem].name)) # Empty
pix.wield(key)
print("Pix's inventory: {}".format(pix.inventory)) #Torch, key
print("Items in current room: {}".format(pix.locationObject.items)) #Empty
print("Pix is wielding a {}\n".format(Item._registry[pix.wieldedItem].name)) # Empty

"""Next few lines, Pix goes to Centre Room and tries unlocking rooms in all 
directions. It doesn't work because there are no rooms to unlock."""
pix.move("E")
pix.unlock("N")
pix.unlock("S")
pix.unlock("E")
pix.unlock("W")
print("Rooms and if they're not locked: {}".format(pix.locationObject.adjRoomOpen))
print("Rooms and their keys (if any): {}\n".format(pix.locationObject.adjRoomKeys))

"""Next few lines, Pix goes to West Room, which has a room to the west of it that
is locked and needs the item key to unlock it. They unlock the door then move back
and forth between West Room and Secret Room.
"""
pix.move("W") # Pix entered West Room
pix.move("W") # Pix can't go W
print("Pix is in {}.".format(pix.locationObject.name)) # Pix is still in West Room
print("Adjacent rooms and if they're not locked: {}".format(pix.locationObject.adjRoomOpen)) # Room to west is Locked (False)
print("Adjacent rooms and their keys (if any): {}\n".format(pix.locationObject.adjRoomKeys)) # Room to west has "key" as key

pix.unlock("N") # Invalid
pix.unlock("S") # Invalid
pix.unlock("E") # Invalid
pix.unlock("W") # Valid! Room to the west is now unlocked
print("Pix is in {}.".format(pix.locationObject.name)) # Pix still in West Room, unlocking a room doesn't automatically move you.
print("Adjacent rooms and if they're not locked: {}".format(pix.locationObject.adjRoomOpen)) # Room to west is Open (True)
print("Adjacent rooms and their keys (if any): {}\n".format(pix.locationObject.adjRoomKeys)) # Room to west has "key" as key

pix.move("W") # Pix enters Secret Room, cutscene plays
pix.move("E") #Pix can go back to West Room, the Locked Room is not locked from the inside
pix.move("W") #No need to unlock again if you wanna go to an unlocked room.

print("\n")
pix.move("W") #bat room has a swarm of bats that can be scared by the torch. 
pix.move("W") #bats act as a lock preventing progress
pix.activate(torch) #invalid, wielding key not torch
pix.wield(torch) #wield torch
pix.activate(torch) #activate torch scare the bats
pix.move("W") #Pix can now move west
pix.activate(torch) #the torch wont do anything in this room

pix.activeCharacter(1) #Pix is now the active player who will do the players actions
print (boulderRoom.characters) #print all the characters present in the room
pix.talk(marine) #talk to marine
pix.talk(pix) #invalid talking to self
marine.emotionState("angry") #make marine angry
pix.talk(marine) #angry dialogue
pix.recruit(marine) #add marine to pix's party and vice versa
print(pix.party)  
print(marine.party)
print (pix.locationObject.characters)
pix.move("W") #pix doesn't have enough strength to move west
marine.move("W")  #marine has enough strength to move west
print (marine.locationObject.characters) #all characters in party moved west