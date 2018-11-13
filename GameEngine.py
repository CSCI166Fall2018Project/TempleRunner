from Objects import *

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
        # Player starts at (0,0)
        self.Player = Player(0, 0)

    def GetSize(self):
        return self.Size
    def GetDimensions(self):
        return self.Dimensions

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
        # Try to find the player
        playerX, playerY = self.Player.GetCoords()
        if playerX == pX and playerY == pY:
            return self.Player
        # then check the most likely culprits
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


class GameEngine:
    def __init__(self):
        # Grid contains all tiles, and the player
        self.Grid = GameGrid()

    def StartGame(self):
        # Create a Random grid to start
        self.Grid.RandomizeLevel()

    def GetValidMoves(self):

        valid = []
        # Get player Coordinates
        pX, pY = self.Grid.Player.Coords
        # Get Tiles around player
        nBlock = self.Grid.GetTileAt(pX,pY+1)
        eBlock = self.Grid.GetTileAt(pX+1,pY)
        sBlock = self.Grid.GetTileAt(pX,pY-1)
        wBlock = self.Grid.GetTileAt(pX-1,pY)
        # Test for walls
        if nBlock and nBlock is not Wall:
            valid.append(EnumDirection.NORTH)
        if eBlock and eBlock is not Wall:
            valid.append(EnumDirection.EAST)
        if sBlock and sBlock is not Wall:
            valid.append(EnumDirection.SOUTH)
        if wBlock and wBlock is not Wall:
            valid.append(EnumDirection.WEST)
        # Return the valid moves array
        return valid

    def GetValidDirections(self):

        valid = []
        # Get player Coordinates
        pX, pY = self.Grid.Player.GetCoords()
        # Get Tiles around player
        nBlock = self.Grid.GetTileAt(pX,pY+1)
        eBlock = self.Grid.GetTileAt(pX+1,pY)
        sBlock = self.Grid.GetTileAt(pX,pY-1)
        wBlock = self.Grid.GetTileAt(pX-1,pY)
        # Test for walls
        if nBlock and nBlock is not Wall:
            valid.append(EnumDirection.STR_NORTH)
        if eBlock and eBlock is not Wall:
            valid.append(EnumDirection.STR_EAST)
        if sBlock and sBlock is not Wall:
            valid.append(EnumDirection.STR_SOUTH)
        if wBlock and wBlock is not Wall:
            valid.append(EnumDirection.STR_WEST)
        # Return the valid moves array
        return valid

    def MovePlayer(self, direction):
        if direction == EnumDirection.NORTH:
            # Go North
            xPos, yPos = self.Player.Coords
            yPos += 1
            self.Player = (xPos, yPos)
        elif direction == EnumDirection.EAST:
            # Go North
            xPos, yPos = self.Player.Coords
            xPos += 1
            self.Player = (xPos, yPos)
        elif direction == EnumDirection.SOUTH:
            # Go North
            xPos, yPos = self.Player.Coords
            yPos -= 1
            self.Player = (xPos, yPos)
        elif direction == EnumDirection.WEST:
            # Go North
            xPos, yPos = self.Player.Coords
            xPos -= 1
            self.Player = (xPos, yPos)

