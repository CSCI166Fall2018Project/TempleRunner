import Utils

# ================================
#       Class Definitions
# Create new Classes here
# ================================

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
            return "Try to squeeze through a hole in the "+dir+" wall, but cannot fit through."

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
        self.TransitionChance = [0.7, 0.2, 0.5]

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
