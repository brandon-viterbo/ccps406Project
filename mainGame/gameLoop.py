import gameClasses
import json

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
borisBox = gameClasses.Room("r014")

alfredo = gameClasses.Obstacle("o008_alfredo")
door = gameClasses.Obstacle("o000_door")
bats = gameClasses.Obstacle("o001_bats")
boulder = gameClasses.Obstacle("o002_boulder")
gate = gameClasses.Obstacle("o003_gate")
hole= gameClasses.Obstacle("o004_hole")
arrows = gameClasses.Obstacle("o005_arrows")
chasm = gameClasses.Obstacle("o006_chasm")

fish = gameClasses.Item("i010_fish")
torch = gameClasses.Item("i000_torch")
stone = gameClasses.Item("i001_stone")
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

pix.activeCharacter(1)
playerCharacter = pix

invalidInputMessage = "{} mind wandered and didn't do anything.".format(playerCharacter.name)

#One word inputs
LOOK_COMMAND = "LOOK"
DISPLAY_INVENTORY = "INVENTORY"

GENERAL_COMMANDS = {
    "LOOK": playerCharacter.look
}

ITEM_COMMANDS = {
    "TAKE": playerCharacter.take,
    "WIELD": playerCharacter.wield,
    "DROP": playerCharacter.drop
}

CHARACTER_COMMANDS = {
    "RECRUIT": playerCharacter.recruit,
    "TALK": playerCharacter.talk
}


def main():
    section1()


def section1():
    print("\n".join(chapters["chapter1"]))
    print("\n".join(chapters["chapter2"]))
    
    def itemTutorialEndCond():
        return familyHome.adjRoomObstacles["N"] == NULL_TAG
    inputLoop(playerCharacter, itemTutorialEndCond)

    print("\n".join(chapters["chapter3"]))
    pix.wieldedItem = NULL_TAG
    pix.recruit(marine)

    def movementTutorialEndCond():
        return playerCharacter.locationObject == villageSquare
    inputLoop(playerCharacter, movementTutorialEndCond)


def inputLoop(playerCharacter, endCondFunc):
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
            elif character != None:
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
            elif character != None:
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
    if character.objID not in playerCharacter.party:
        print("{} is not in {}'s party.".format(
            character.name, playerCharacter.name))
    else:
        print("{} says, 'What should I do?'".format(character.name))
        inputLoop(character, False)


main()