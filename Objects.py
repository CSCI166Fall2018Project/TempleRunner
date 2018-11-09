import Utils

# ================================
#       Class Definitions
# Create new Classes here
# ================================

# Tile Class is the basic floor tile.
class Tile:
    def __init__(self, x, y):
        self.Name = "Tile"
        self.posX = x
        self.posY = y
        # Chances are separated by [SNEAK, WALK, RUN]
        self.TransitionChance = [1.0, 1.0, 1.0]

    def __str__(self):
        x, y = self.GetCoords()
        return self.Name + " (" + str(x) + "," + str(y) + ")"

    def GetCoords(self):
        return self.posX, self.posY

    def GetTile(self):
        return "[ ]"


# Wall to block player movement
class Wall(Tile):
    def __init__(self, x, y):
        self.Name = "Wall"
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.0, 0.0, 0.0]

    def GetTile(self):
        return "[#]"

# Dart Trap to kill player unless ran over
class TrapDarts(Tile):
    def __init__(self, x, y):
        self.Name = "TrapDarts";
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.6, 0.1, 1.0]

    def GetTile(self):
        return "[!]"

# Trap Door with increased chance to kill player
class TrapDoor(Tile):
    def __init__(self, x, y):
        self.Name = "TrapDoor";
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.7, 0.2, 0.5]

    def GetTile(self):
        return "[/]"

class GameGrid:
    def __init__(self):
        # Size of the grid
        self.Size = 10

        # Total number of blocks
        self.Dimensions = self.Size * self.Size

        # Arrays of Tiles, Walls, and Traps
        self.Tiles = []
        self.Walls = []
        self.TrapDarts = []
        self.TrapDoors = []

    def RandomizeLevel(self):
        # Handle Columns
        for y in range(0, self.Size, 1):
            # Handle Rows
            for x in range(0, self.Size, 1):
                # print(str(x) + "," + str(y))
                # Test for what tile we should create at what position

                # 20% chance of Trap Door
                doorChance = Utils.TryChance(0.20)
                if doorChance:
                    self.TrapDoors.append(TrapDoor(x, y))
                    continue

                # 25% of Darts
                dartChance = Utils.TryChance(0.35)
                if dartChance:
                    self.TrapDarts.append(TrapDarts(x, y))
                    continue

                # 30% chance of a wall
                wallChance = Utils.TryChance(0.7)
                if wallChance:
                    self.Walls.append(Wall(x, y))
                    continue

                # 40% chance to place a tile
                self.Tiles.append(Tile(x, y))
                continue

    def ShowAllObjects(self):
        # Output all the objects
        print("Tiles: " + str(len(self.Tiles)))
        for obj in self.Tiles:
            print(obj.GetString())

        print("Walls: " + str(len(self.Walls)))
        for obj in self.Walls:
            print(obj.GetString())

        print("Darts: " + str(len(self.TrapDarts)))
        for obj in self.TrapDarts:
            print(obj.GetString())

        print("Doors: " + str(len(self.TrapDoors)))
        for obj in self.TrapDoors:
            print(obj.GetString())

    # Check all objects in the grid to find
    # the object at the given coordinates
    def GetTileAt(self, pX, pY):
        # Check the most likely culprits first
        for tile in self.Tiles:
            x, y = tile.GetCoords()
            if x == pX and y == pY:
                return tile
        for wall in self.Walls:
            x, y = wall.GetCoords()
            if x == pX and y == pY:
                return wall
        for door in self.TrapDoors:
            x, y = door.GetCoords()
            if x == pX and y == pY:
                return door
        for dart in self.TrapDarts:
            x, y = dart.GetCoords()
            if x == pX and y == pY:
                return dart

    def ShowGrid(self):
        finalString = ""
        # Handle Columns
        for y in range(0, self.Size, 1):
            # Handle Rows
            for x in range(0, self.Size, 1):
                tile = self.GetTileAt(x,y)
                finalString += tile.GetTile()
            finalString += "\n\r"
        print(finalString)
