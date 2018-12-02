import Utils

# ================================
#       Class Definitions
# Create new Classes here
# ================================

# Enums
# Use these classes to represent single values,
class EnumCadence:
    SNEAK = 0
    WALK = 1
    RUN = 2
    STR_SNEAK = "SNEAK"
    STR_WALK = "WALK"
    STR_RUN = "RUN"



class EnumDirection:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    STR_NORTH = "NORTH"
    STR_EAST = "EAST"
    STR_SOUTH = "SOUTH"
    STR_WEST = "WEST"

class EnumGameState:
    PLAYER_ALIVE = 0
    PLAYER_DEAD = 1
    PLAYER_WON = 2


# Tile Class is the basic floor tile.
class Tile:
    def __init__(self, x, y):
        self.Name = "Tile"
        self.posX = x
        self.posY = y
        # Chances are separated by [SNEAK, WALK, RUN]
        self.TransitionChance = [1.0, 1.0, 1.0]

    # When you use str() on a Tile object, this function is called
    def __str__(self):
        x, y = self.GetCoords()
        return self.Name + " (" + str(x) + "," + str(y) + ")"

    def GetCoords(self):
        return self.posX, self.posY

    def GetTile(self):
        return "[ ]"

    def Describe(self, dir):
        r = Utils.RandBetween(0, 2)
        if r is 0:
            return "To your "+dir+" lies more plain clay tiles. Appears to be safe."
        if r is 1:
            return dir+"-bound you see a clear passageway to the next room."
        if r is 2:
            return "You gaze "+dir+"-ward to see a well worn passage."


# Wall to block player movement
class Wall(Tile):
    def __init__(self, x, y):
        self.Name = "Wall"
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.0, 0.0, 0.0]

    def GetTile(self):
        return "[#]"

    def Describe(self, dir):
        r = Utils.RandBetween(0, 2)
        if r is 0:
            return "Examining to room, you look to the "+dir+" to see a solid wall."
        if r is 1:
            return "Rubble has collapsed and closed the tunnel leading "+dir+"."
        if r is 2:
            return "You try to squeeze through a hole in the "+dir+" wall, but cannot fit through. It's impassable."

# Dart Trap to kill player unless ran over
class TrapDarts(Tile):
    def __init__(self, x, y):
        self.Name = "TrapDarts"
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.6, 0.1, 1.0]

    def GetTile(self):
        return "[!]"

    def Describe(self, dir):
        r = Utils.RandBetween(0, 2)
        if r is 0:
            return "While looking "+dir+", you notice the ceiling has open holes..."
        if r is 1:
            return dir+"-bound you see a passage, occupied by a corpse with a several darts embedded in him."
        if r is 2:
            return "You look toward the "+dir+" hallway to see a many raised tiles and small dart-sized openings in the walls..."

# Trap Door with increased chance to kill player
class TrapDoor(Tile):
    def __init__(self, x, y):
        self.Name = "TrapDoor"
        self.posX = x
        self.posY = y
        self.TransitionChance = [0.5, 0.2, 0.7]

    def GetTile(self):
        return "[/]"

    def Describe(self, dir):
        r = Utils.RandBetween(0, 2)
        if r is 0:
            return "You decide to inspect " + dir + "-ward, and notice the floor has a single slit in the middle.\n\rThe floor tile feels shaky..."
        if r is 1:
            return "Taking a cautious step towards the "+dir+" passage, the floor gives under your feet.\n\rRecoiling, you see the floor rise back into position.."
        if r is 2:
            return "The " + dir + "-bound hallway is narrow, and some of the floor tiles appear to be barely suspended in place..."

# Exit Door, player wins if they reach the exit
class ExitDoor(Tile):
    def __init__(self, x, y):
        self.Name = "Exit Door"
        self.posX = x
        self.posY = y
        self.TransitionChance = [1.0, 1.0, 1.0]

    def GetTile(self):
        return "[E]"

    def Describe(self, dir):
        return "Looking " + dir + "-ward, you see light shining through an archway that appears to lead outside."

class Player:
    def __init__(self, X, Y):
        self.posX = X
        self.posY = Y
        self.Tired = False
        self.Exhausted = False
        self.ChanceToExhaust = 0.05
        self.ExhaustedTurns = 0
        self.Cadence = EnumCadence.WALK
        self.DebugMode = True

    def isTired(self):
        return self.IsTired

    def isExhausted(self):
        return self.Exhausted

    def GetCoords(self):
        return self.posX, self.posY

    def SetCoords(self, x, y):
        self.posX = x
        self.posY = y

    def GetTile(self):
        return "[P]"

    def WalkOrSneak(self):
        # Remove an exhausted turn
        if self.ExhaustedTurns > 0:
            self.ExhaustedTurns -= 1
        # If finished being exhausted, return to Normal State
        if self.ExhaustedTurns is 0:
            self.Tired = False
            self.Exhausted = False

    def TryRun(self):
        # State change from Ready to Tired after first run
        if self.Tired is False:
            self.Tired = True
        else:
            # Testing exhausion chance
            exhaust = Utils.TryChance(self.ChanceToExhaust)
            if exhaust:
                self.Exhausted = True
                self.ExhaustedTurns = 5
            else:
                # Increase the Chance to Exhaust up to 0.5
                if self.ChanceToExhaust <= 0.5:
                    # Keep the Chance to exhaust rounded to 2 decimal points
                    self.ChanceToExhaust = round(self.ChanceToExhaust + 0.05, 2)
                    if self.DebugMode:
                        print("Player has chance: " + str(self.ChanceToExhaust) + " to Exhaust.")

    def Run(self):
        # Test if we exhausted the player
        self.TryRun()


class GameGrid:
    def __init__(self, show_desc=True):
        # Size of the grid
        self.Size = 5

        # Total number of blocks
        self.Dimensions = self.Size * self.Size

        # Arrays of Tiles, Walls, and Traps
        self.Tiles = []
        self.Walls = []
        self.TrapDarts = []
        self.TrapDoors = []

        # Player starts at (0, 0)
        self.Player = Player(0, 0)

        # Exit door is the goal (self.Size, self.Size)
        self.ExitDoor = ExitDoor(self.Size-1, self.Size-1)

        # Set if we describe the environment at each step
        self.ShowDescriptions = show_desc

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

                # 35% of Darts
                dartChance = Utils.TryChance(0.35)
                if dartChance:
                    self.TrapDarts.append(TrapDarts(x, y))
                    continue

                # 30% chance of a wall
                wallChance = Utils.TryChance(0.3)
                if wallChance:
                    self.Walls.append(Wall(x, y))
                    continue

                # 40% chance to place a tile
                self.Tiles.append(Tile(x, y))
                continue

    # Prints out all the objects in a long list
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
    def GetTileAt(self, pX, pY, skipPlayer=False):
        # Skip the player when processing through AI agents
        if not skipPlayer:
            # Try to find the player
            playerX, playerY = self.Player.GetCoords()
            if playerX == pX and playerY == pY:
                return self.Player
        # Then check the exit door
        exitX, exitY = self.ExitDoor.GetCoords()
        if exitX == pX and exitY == pY:
            return self.ExitDoor
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

    def GetTileFromPlayerDirection(self, dir):
        # Try to find the player
        playerX, playerY = self.Player.GetCoords()

        if dir is EnumDirection.STR_NORTH:
            return self.GetTileAt(playerX, playerY + 1)
        elif dir is EnumDirection.STR_EAST:
            return self.GetTileAt(playerX + 1,playerY)
        elif dir is EnumDirection.STR_SOUTH:
            return self.GetTileAt(playerX,playerY - 1)
        elif dir is EnumDirection.STR_WEST:
            return self.GetTileAt(playerX - 1, playerY)
        else:
            return


    # Displays the Whole grid by accessing GetTile() from all tiles
    def ShowGrid(self):
        finalString = ""
        # Handle Columns
        for y in range(self.Size-1, -1, -1):
            # Handle Rows
            for x in range(0, self.Size, 1):
                tile = self.GetTileAt(x, y)
                if tile:
                    finalString += tile.GetTile()
            finalString += "\n\r"
        print(finalString)

    def HasPlayerReachedExit(self):
        # Check if we won by examining the Exit door
        exitX, exitY = self.ExitDoor.GetCoords()
        playerX, playerY = self.Player.GetCoords()

        if exitX is playerX and exitY is playerY:
            return True
        else:
            return False

    def GetAllTiles(self):
        # Create array of all tiles
        allTiles = []
        # Handle Columns
        for y in range(0, self.Size, 1):
            # Handle Rows
            for x in range(0, self.Size, 1):
                # Skip the player tile, not factored
                tile = self.GetTileAt(x, y, True)
                allTiles.append(tile)
        return allTiles