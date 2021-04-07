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
print(pix.locationObject.entryCutscene)
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
    inputLoop(playerCharacter, False)


def inputLoop(playerCharacter, endCondition):
    while(not endCondition):
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
        if not playerCharacter.playerCharacter:
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