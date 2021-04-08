import gameClasses
import json
import time

NULL_TAG = "NULL"
CHAPTERS = "chapters.json"

with open(CHAPTERS, "r") as readFile:
    chapters = json.load(readFile)


shore = gameClasses.Room("r000")
valley = gameClasses.Room("r001")
villageSquare = gameClasses.Room("r002")
familyHome = gameClasses.Room("r003")
lake = gameClasses.Room("r004")
templeEntrance = gameClasses.Room("r005")
antechamber = gameClasses.Room("r006")
antechamberA1 = gameClasses.Room("r007")
tinyHole = gameClasses.Room("r008")
antechamberA2 = gameClasses.Room("r009")
templeArrowRoom = gameClasses.Room("r010")
templeChasm = gameClasses.Room("r011")
eyeOfTheTemple = gameClasses.Room("r012")
borisHaven = gameClasses.Room("r013")

alfredo = gameClasses.Obstacle("o008_alfredo")
door = gameClasses.Obstacle("o000_door")
bats = gameClasses.Obstacle("o001_bats")
hole = gameClasses.Obstacle("o004_hole")
boulder = gameClasses.Obstacle("o002_boulder")
gate = gameClasses.Obstacle("o003_gate")
arrows = gameClasses.Obstacle("o005_arrows")
chasm = gameClasses.Obstacle("o006_chasm")
eye = gameClasses.Obstacle("o007_eye")

fish = gameClasses.Item("i010_fish")
torch = gameClasses.Item("i000_torch")
shield = gameClasses.Item("i002_shield")
key = gameClasses.Item("i003_key")
fan = gameClasses.Item("i004_fan")
flag = gameClasses.Item("i005_flag")
trident = gameClasses.Item("i006_trident")
violin = gameClasses.Item("i007_violin")
octobass = gameClasses.Item("i008_octobass")
gem = gameClasses.Item("i009_gem")

pix = gameClasses.Character("c000_pix")
marine = gameClasses.Character("c001_marine")
boris = gameClasses.Character("c002_boris")

pix.activeCharacter(1)
playerCharacter = pix

invalidInputMessage = "{} mind wandered and didn't do anything.".format(playerCharacter.name)

#One word inputs
LOOK_COMMAND = "LOOK"
DISPLAY_INVENTORY = "INVENTORY"

GENERAL_COMMANDS = {
    "LOOK": playerCharacter.look
}

CHARACTER_COMMANDS = {
    "RECRUIT": playerCharacter.recruit,
    "TALK": playerCharacter.talk
}


def main():
    print("\n\n")
    print("\n".join(chapters["chapter1"]))
    print("\n".join(chapters["chapter2"]))
    
    def itemTutorialEndCond():
        return familyHome.adjRoomObstacles["N"] == NULL_TAG
    inputLoop(playerCharacter, itemTutorialEndCond)

    print("\n".join(chapters["chapter3"]))
    pix.wieldedItem = NULL_TAG
    pix.recruit(marine)
    print("\n")

    def movementTutorialEndCond():
        return playerCharacter.locationObject == villageSquare
    inputLoop(playerCharacter, movementTutorialEndCond)

    def templeFirstLegEndCond():
        return ((pix.locationObject == templeChasm) and 
            (marine.locationObject == templeChasm) and
            (templeChasm.adjRoomObstacles["S"] == NULL_TAG))
    inputLoop(playerCharacter, templeFirstLegEndCond)
    
    time.sleep(3)
    if fan.objID in templeChasm.items:
        marine.take(fan)
    if fan.objID != marine.wieldedItem:
        marine.wield(fan)
    print("\n")
    print("\n".join(chapters["chapter4"]))
    print("\n")

    def epicentreEndCond():
        return (pix.locationObject == eyeOfTheTemple and
            marine.locationObject == eyeOfTheTemple)
    inputLoop(playerCharacter, epicentreEndCond)

    marine.take(trident)
    marine.wield(trident)
    marine.removeObstacle("STRIKE", eye)
    print("\n".join(chapters["pause"]))
    time.sleep(3)
    eyeOfTheTemple.characters.remove(pix.objID)
    eyeOfTheTemple.characters.remove(marine.objID)
    pix.locationObject = borisHaven
    pix.locationID = borisHaven.objID
    marine.locationObject = borisHaven
    marine.locationID = borisHaven.objID
    borisHaven.characters.append(pix.objID)
    borisHaven.characters.append(marine.objID)
    time.sleep(3)
    print("\n".join(chapters["chapter5"]))
    boris.drop(violin)
    boris.drop(octobass)

    def finale():
        return (pix.wieldedItem == violin.objID and
            violin.activated == True)
    inputLoop(playerCharacter, finale)
    time.sleep(3)
    print("\n".join(chapters["chapter6"]))
    time.sleep(3)
    if octobass.objID in borisHaven.items:
        marine.take(octobass)
    if marine.wieldedItem != octobass.objID:
        marine.wield(octobass)
    if not octobass.activated:
        marine.activate("PLAY", octobass)
    pix.activate("STOP", violin)
    marine.activate("STOP", octobass)
    print("\n".join(chapters["pause"]))
    time.sleep(3) 
    print("\n".join(chapters["finale"]))


def inputLoop(playerCharacter, endCondFunc):
    ITEM_COMMANDS = {
        "TAKE": playerCharacter.take,
        "WIELD": playerCharacter.wield,
        "DROP": playerCharacter.drop
    }

    while(endCondFunc()==False):
        userIn = input()
        inputArgs = userIn.split()
        argLen = len(inputArgs)

        count = 0
        for i in inputArgs:
            inputArgs[count] = i.upper()
            count += 1

        if argLen == 1:
            character = verifyObject(gameClasses.Character, inputArgs[0])
            if (inputArgs[0] in gameClasses.DIRECTIONS):
                playerCharacter.move(inputArgs[0])
            elif inputArgs[0] == LOOK_COMMAND:
                playerCharacter.look(playerCharacter.locationObject)
            elif inputArgs[0] == DISPLAY_INVENTORY:
                playerCharacter.displayInventory()
            elif playerCharacter.playerCharacter and character != None:
                shiftPlayerControl(playerCharacter, character)
            else:
                print(invalidInputMessage)
        elif argLen == 2:
            item = verifyObject(gameClasses.Item, inputArgs[1])
            character = verifyObject(gameClasses.Character, inputArgs[1])
            obstacle = verifyObject(gameClasses.Obstacle, inputArgs[1])
            generalObject = None
            for i in [item, character, obstacle]:
                if i != None:
                    generalObject = i
                    break
            if ((inputArgs[0] in GENERAL_COMMANDS) and (generalObject != None)):
                GENERAL_COMMANDS[inputArgs[0]](generalObject)
            elif item != None:
                if (inputArgs[0] in ITEM_COMMANDS):
                    ITEM_COMMANDS[inputArgs[0]](item)
                else:
                    playerCharacter.activate(inputArgs[0], item)
            elif obstacle != None:
                playerCharacter.removeObstacle(inputArgs[0], obstacle)
            elif inputArgs[0] in CHARACTER_COMMANDS and character != None:
                CHARACTER_COMMANDS[inputArgs[0]](character)
            else:
                print(gameClasses.objActionInvalid.format(
                playerCharacter.name, inputArgs[0], inputArgs[1]))
        else:
            print(invalidInputMessage)
        print("\n")
        if (not playerCharacter.playerCharacter):
            break


def verifyObject(C, inputName):
    # C should be gameClasses.X, where X is any class in gameClasses.py
    for i in C._names:
        if inputName == i:
            objID = C._names[inputName]
            obj = C._registry[objID]
            return obj
    return None


def shiftPlayerControl(playerCharacter, character):
    if playerCharacter.objID == character.objID:
        print("{} wondered what they should do.".format(playerCharacter.name))
    elif character.objID not in playerCharacter.party:
        print("{} is not in {}'s party.".format(
            character.name, playerCharacter.name))
    else:
        print("{} says, 'What should I do?'".format(character.name))
        def endCondFunc():
            return False
        inputLoop(character, endCondFunc)


main()