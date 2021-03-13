class GameMap():
  def __init__(self):
    self.mapID = 0
    self.mapPassable = [0,1,1,0]
    self.adjMaps = [None,2,3,None]
  def set_map_id(self,x):
    self.mapID = x
  def get_map_id(self):
    return self.mapID
  def changeMap (self, direction):
    if(direction == "N" and self.mapPassable[0]==1):
        self.set_map_id(self.adjMaps[0])
        retStr = (self.mapID)
        return retStr
    elif(direction == "E" and self.mapPassable[1]==1):
        self.set_map_id(self.adjMaps[1])
        retStr = (self.mapID)
        return retStr
    elif(direction == "S" and self.mapPassable[2]==1):
        self.set_map_id(self.adjMaps[2])
        retStr = (self.mapID)
        return retStr
    elif(direction == "W" and self.mapPassable[3]==1):
        self.set_map_id(self.adjMaps[3])
        retStr = (self.mapID)
        return retStr
    else:
      retStr = ("Can't go in that direction!")
      return retStr
    
x=GameMap()
print(x.get_map_id())
print(x.changeMap("N"))
print(x.changeMap("E"))
print(x.changeMap("S"))
print(x.changeMap("W"))