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

def validateItem(itemName):
    for i in gameClasses.Item._names:
        if itemName == i:
            itemID = gameClasses.Item._names[itemName]
            item = gameClasses.Item._registry[itemID]
            return item
    return None

GENERAL_ITEM_COMMANDS = {
    "TAKE": playerCharacter.take,
    "WIELD": playerCharacter.wield,
    "DROP": playerCharacter.drop
}

while(1):
    userIn = input()
    inputArgs = userIn.split()
    argLen = len(inputArgs)

    count = 0
    for i in inputArgs:
    	inputArgs[count] = i.upper()
    	count += 1

    if argLen == 1:
        if (inputArgs[0] in gameClasses.DIRECTIONS):
            playerCharacter.move(inputArgs[0])
    elif argLen == 2:
        item = validateItem(inputArgs[1])
        if item != None:
            if (inputArgs[0] in GENERAL_ITEM_COMMANDS):
                if item != None:
        	        GENERAL_ITEM_COMMANDS[inputArgs[0]](item)
            else:
        	    playerCharacter.activate(inputArgs[0], item)
        else:
        	print(gameClasses.objActionInvalid.format(
        		playerCharacter.name, inputArgs[0], inputArgs[1]))
    else:
        print("{} mind wandered and didn't do anything.".format(playerCharacter.name))

    print("\n")