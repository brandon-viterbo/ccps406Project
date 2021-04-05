import json

GAMEPLAY_MESSAGES_RAW = "gameplayMessages.json"
CHARACTERS_RAW = "characters.json"
ROOMS_RAW = "rooms.json"
ITEMS_RAW = "items.json"
OBSTACLES_RAW = "obstacles.json"

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
    skillCheckSuccessful = gameplayMessages["skillCheck"]["successfulText"]
    skillCheckUnsuccessful = gameplayMessages["skillCheck"]["unsuccessfulText"]

with open(CHARACTERS_RAW, "r") as readFile:
    allCharacterData = json.load(readFile)

with open(ROOMS_RAW, "r") as readFile:
    allRoomData = json.load(readFile)

with open(ITEMS_RAW, "r") as readFile:
    allItemData = json.load(readFile)

with open(OBSTACLES_RAW, "r") as readFile:
    allObstacleData = json.load(readFile)


class Character():
    _registry = {}
    _names = {}


    def __init__(self, objID):
        self._registry[objID] = self
        self.objID = objID
        thisCharacterData = allCharacterData[objID]
        self.playerCharacter = False
        self.emotionalState = "happy"

        self.name = thisCharacterData["name"]
        self._names[self.name.upper()] = self.objID
        self.dialogue = thisCharacterData["dialogue"]
        self.strength = thisCharacterData["strength"]
        self.weight = thisCharacterData["weight"]
        self.inventory = thisCharacterData["inventory"]
        self.wieldedItem = thisCharacterData["wieldedItem"]
        self.locationID = thisCharacterData["locationID"]
        self.locationObject = Room._registry[self.locationID]
        self.party = thisCharacterData["party"]
        self.lookDescription = thisCharacterData["lookDescription"]


    def look(self, obj):
        currentRoom = self.locationObject

        if obj == currentRoom:
            print(currentRoom.lookDescription)
            return
        elif ((obj.objID in currentRoom.items) or 
        (obj.objID in currentRoom.characters) or 
        (obj.objID in currentRoom.adjRoomObstacles.values()) or
        (obj.objID in self.inventory) or (obj.objID == self.wieldedItem)):
            print(obj.lookDescription)
            return
        print(objActionUnsuccessful.format(self.name, "see", obj.name))


    def take(self, item):
        """Action Type: objAction"""
        verb = "took"
        count = 0

        if item.objID not in self.locationObject.items:
            print(objActionInvalid.format(self.name, verb, item.name))
            return

        if item.weight > self.strength:
            print(skillCheckUnsuccessful.format(self.name, "strength"))
            return

        for i in self.inventory:
            if i == NULL_TAG:
                self.inventory[count] = item.objID
                print(objActionSuccessful.format(self.name, verb, item.name))
                self.locationObject.items.remove(item.objID)
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, verb, item.name))
    

    def recruit(self, charName):
        if charName.objID not in self.locationObject.characters:
            print("That character can't join you right now.")
            return 

        selfIndex = -1
        charIndex = -1
        count = 0
        for i, j in zip(self.party, charName.party):
            if i == NULL_TAG:
                selfIndex = count
            if j == NULL_TAG:
                charIndex = count
            count += 1

        if (selfIndex >= 0) and (charIndex >= 0):
            self.party[selfIndex] = charName.objID
            charName.party[charIndex] = self.objID
            print(charName.name + " joined the party!")
            return

        print("That character can't join you right now.")


    def drop(self, item):
        """Type: objAction"""
        verb = "dropped"
        count = 0
        if self.wieldedItem == item.objID:
            self.wieldedItem = NULL_TAG
            self.locationObject.items.append(item.objID)
            print(objActionSuccessful.format(self.name, verb, item.name))
            return

        for i in self.inventory:
            if i == item.objID:
                print(objActionSuccessful.format(self.name, verb, 
                    item.name))
                self.inventory[count] = NULL_TAG
                self.locationObject.items.append(item.objID)
                return
            count += 1
        print(objActionInvalid.format(self.name, verb, item.name))
        return


    def wield(self, item):
        count = 0
        if item.objID == self.wieldedItem:
            print("{} is already wielding that.".format(self.name))
            return
        for i in self.inventory:
            if i == item.objID:
                if self.wieldedItem != NULL_TAG:
                    self.inventory[count] = self.wieldedItem
                else:
                    self.inventory[count] = NULL_TAG
                self.wieldedItem = item.objID
                print(objActionSuccessful.format(
                    self.name, "wielded", item.name)
                )
                return
            count += 1
        print(objActionUnsuccessful.format(self.name, "wield", item.name))


    def activate(self, verb, item):
        # This method can also deativate items.
        if item.objID in self.inventory:
            print("Trying wielding an item before doing anything with it.")
            return
        elif (item.objID == self.wieldedItem):
            wieldedItem = Item._registry[item.objID]
            if wieldedItem.activateWord == NULL_TAG:
                # If item can't be activated, return.
                print(objActionInvalid.format(self.name, verb, wieldedItem.name))
                return
            if (wieldedItem.activateWord == verb) and (not wieldedItem.activated):
                # Activate item
                print(wieldedItem.messages["itemActivated"])
                wieldedItem.activated = True
            elif (wieldedItem.deactivateWord == verb) and (wieldedItem.activated):
                # Deactivate item
                print(wieldedItem.messages["itemDeactivated"])
                wieldedItem.activated = False
            elif (wieldedItem.activateWord == verb) and (wieldedItem.activated):
                # Can't activate item that's already activated
                print(wieldedItem.messages["itemAlreadyActive"])
            elif (wieldedItem.deactivateWord == verb) and (not wieldedItem.activated):
                # Can't deactivate item that's already deactivated
                print(wieldedItem.messages["itemAlreadyDeactive"])
            else:
                # Catch any other invalid cases within the outer if-statement
                print(objActionInvalid.format(self.name, verb, wieldedItem.name))
            return
        print(singleActionInvalid.format(self.name, "do that"))


    def move(self, direction):
        """Action Type: Entering Room"""
        nextobjID = self.locationObject.adjRooms[direction]
        if nextobjID == NULL_TAG:
            print(enteringRoomInvalid.format(direction, self.name, 
                self.locationObject.name))
            return

        nextRoomObject = Room._registry[nextobjID]
        objID = self.locationObject.adjRoomObstacles[direction]
        if objID != NULL_TAG:
            obstacle = Obstacle._registry[objID]
            print(obstacle.messages["blockedText"])
            print(enteringRoomUnsuccessful.format(self.name, direction, 
                self.name, self.locationObject.name))
            return

        self.locationObject.characters.remove(self.objID)
        self.locationObject = nextRoomObject
        self.locationID = nextobjID
        self.locationObject.characters.append(self.objID)

        for i in self.party:
            if i != NULL_TAG:
                member = Character._registry[i]
                member.move(direction)

        print(enteringRoomSuccessful.format(self.name, self.locationObject.name))
        if self.locationObject.playerVisited == False and self.playerCharacter:
            print(self.locationObject.lookDescription)
            print(self.locationObject.entryCutscene)
            self.locationObject.playerVisited = True  
        return


    def removeObstacle(self, verb, obstacle):
        if obstacle.objID not in self.locationObject.adjRoomObstacles.values():
            print(singleAction.format(self.name, "do that"))
            return

        if self.strength <= obstacle.strengthCheck:
            print(skillCheckUnsuccessful.format(self.name, "strength"))
            return
        elif self.strength <= obstacle.sizeCheck:
            print(skillCheckUnsuccessful.format(self.name, "size"))
            return
        elif (verb == obstacle.unblockKeyword) and (obstacle.key == NULL_TAG):
            # If the obstacle only require a skill check to remove
            print(obstacle.messages["unblockedText"])
            self.locationObject.removeObstacle(obstacle)
            return

        if (verb == obstacle.unblockKeyword
        ) and (obstacle.key != NULL_TAG):
            # If removing obstacle also requires key
            if (self.wieldedItem == obstacle.key) and (
            not obstacle.keyShouldBeActivated):
                print(obstacle.messages["unblockedText"])
                self.locationObject.removeObstacle(obstacle)
                return
            elif (self.wieldedItem == obstacle.key) and (
            obstacle.keyShouldBeActivated) and (
            Item._registry[self.wieldedItem].activated):
                print(obstacle.messages["unblockedText"])
                self.locationObject.removeObstacle(obstacle)
                return
        print(objActionInvalid.format(self.name, verb, obstacle.name))
    
    
    def activeCharacter(self, active):
      if active == 1:
        self.playerCharacter=True
        print (self.name + " is now the player character.")
      if active == 0:
        self.playerCharacter=False
        print (self.name + " is no longer the player character.")
    
    def emotionState(self, emotion):
      if emotion in CHARACTER_EMOTIONAL_STATES:
        self.emotionalState = emotion
      print("PROGRAMMING ERROR: INVALID VARIABLE")
 
    def talk (self, charName):
      if (charName.playerCharacter == False):
        print (charName.name + ": " + charName.dialogue[charName.emotionalState])
      else:
        print ("Why am I talking to myself?")      



class Item():
    _registry = {}
    _names = {}

    def __init__(self, objID):
        self._registry[objID] = self
        self.objID = objID
        thisItemData = allItemData[objID]

        self.name = thisItemData["name"]
        self._names[self.name.upper()] = self.objID
        self.messages = thisItemData["messages"]
        self.weight = thisItemData["weight"]
        self.activated = thisItemData["activated"]
        self.activatedText = thisItemData["messages"]["itemActivated"]
        self.deactivatedText = thisItemData["messages"]["itemDeactivated"]

        self.activateWord = thisItemData["activateWord"]
        self.deactivateWord = thisItemData["deactivateWord"]
        self.lookDescription = thisItemData["lookDescription"]



class Obstacle():
    _registry = {}
    _names = {}

    def __init__(self, objID):
        self._registry[objID] = self
        self.objID = objID
        thisObstacleData = allObstacleData[objID]

        self.name = thisObstacleData["name"]
        self._names[self.name.upper()] = self.objID
        self.unblockKeyword = thisObstacleData["unblockKeyword"]
        self.key = thisObstacleData["key"] 
        self.keyShouldBeActivated = thisObstacleData["keyShouldBeActivated"]
        self.strengthCheck = thisObstacleData["strengthCheck"]
        self.sizeCheck = thisObstacleData["sizeCheck"]
        self.messages = thisObstacleData["messages"]
        self.lookDescription = thisObstacleData["lookDescription"]



class Room():
    _registry = {}
    _names = {}

    def __init__(self, objID):
        self._registry[objID] = self
        self.objID = objID
        thisRoomData = allRoomData[objID]

        self.name = thisRoomData["name"]
        self._names[self.name.upper()] = self.objID
        self.adjRooms = thisRoomData["adjRooms"]
        self.adjRoomObstacles = thisRoomData["adjRoomObstacles"]

        # List of instances of Item class inside of self
        self.items = thisRoomData["items"]
        # List of instances of Character class inside of self
        self.characters = thisRoomData["characters"]

        self.playerVisited = thisRoomData["playerVisited"]
        self.entryCutscene = thisRoomData["entryCutscene"]
        self.lookDescription = thisRoomData["lookDescription"]

    def set_room_id(self, objID):
        self.objID = objID
    def get_room_id(self):
        return self.objID

    def removeObstacle(self, obstacle):
        for i in self.adjRoomObstacles:
            if self.adjRoomObstacles[i] == obstacle.objID:
                self.adjRoomObstacles[i] = NULL_TAG
                return
        print("PROGRAMMING ERROR: Tried removing obstacle not in current location")
        return

