from Objects import *
from os import *

class GameEngine:
    def __init__(self):
        # Grid contains all tiles, and the player
        self.Grid = GameGrid()

        # Game State
        self.GameState = EnumGameState.PLAYER_ALIVE

        # Save the players choice of cadence and direction
        self.PlayerChoice = ()

        # Create a Random grid to start
        self.Grid.Level1()

    def StartGame(self):

        # Gameplay Loop
        while self.GameState == EnumGameState.PLAYER_ALIVE:
            # Show the grid locations
            self.DisplayGameState()
            # Ask player what they want to do
            self.GetPlayerMove()
            # Process the move, collisions, and possible change of game state
            self.ProcessPlayerMove()
            # Reset the player choice
            self.PlayerChoice = ()

        if self.GameState == EnumGameState.PLAYER_DEAD:
            print("You have died! Game Over.")

        if self.GameState == EnumGameState.PLAYER_WON:
            print("You have escaped with the treasure!")


    def DisplayGameState(self):
        self.Grid.ShowGrid()
        if self.Grid.ShowDescriptions:
            self.DescribeSurroundings()

    def GetAllStates(self):
        return self.Grid.GetAllTiles()

    # Examines the state of the game, and
    # returns a reward based on if the player has won or not
    def GetReward(self, state, cadence):
        finalReward = 0

        # Player rewarded for reaching the exit door
        if isinstance(state, ExitDoor):
            finalReward += 100

        return finalReward

    def GetSurroundingTiles(self):
        tiles = []
        # Get player Coordinates
        pX, pY = self.Grid.Player.GetCoords()
        # Get Tiles around player
        nBlock = self.Grid.GetTileAt(pX, pY+1)
        eBlock = self.Grid.GetTileAt(pX+1, pY)
        sBlock = self.Grid.GetTileAt(pX, pY-1)
        wBlock = self.Grid.GetTileAt(pX-1, pY)
        if nBlock:
            tiles.append(nBlock)
        if eBlock:
            tiles.append(eBlock)
        if sBlock:
            tiles.append(sBlock)
        if wBlock:
            tiles.append(wBlock)
        # Return the tiles array
        return tiles

    # Retrieves all directions and cadences from the players position
    def GetAllPossibleActions(self):
        allPossible = []

        # Get all the directions we can go
        directions = self.GetValidDirections()

        # Handle when the player is exhausted
        if self.Grid.Player.Exhausted:
            cadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK]
        else:
            cadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK, EnumCadence.STR_RUN]

        # For all directions
        for dir in directions:
            # For all Cadences
            for cad in cadences:
                # Append the ( Direction, Cadence )
                allPossible.append((dir, cad))

        return allPossible


    # Returns the next state when taking the action, along with the probability of getting there
    def GetTransitionStateAndProb(self, direction, cadence):

        # If the player has reached the Exit Door, they may take no actions
        if self.Grid.Player.GetCoords() == self.Grid.ExitDoor.GetCoords():
            return None, 1.0

        # Get the Destination Tile
        destTile = self.Grid.GetTileFromPlayerDirection(direction)

        # Get the cadence index of the tile
        cadenceIndex = Utils.ConvertCadencetoInt(cadence)
        chance = destTile.TransitionChance[cadenceIndex]

        return destTile, chance

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
        if nBlock and not isinstance(nBlock, Wall):
            valid.append(EnumDirection.STR_NORTH)
        if eBlock and not isinstance(eBlock, Wall):
            valid.append(EnumDirection.STR_EAST)
        if sBlock and not isinstance(sBlock, Wall):
            valid.append(EnumDirection.STR_SOUTH)
        if wBlock and not isinstance(wBlock, Wall):
            valid.append(EnumDirection.STR_WEST)
        # Return the valid moves array
        return valid

    # Gets the directions of tiles for descriptive purposes
    def GetDescriptiveDirections(self):

        valid = []
        # Get player Coordinates
        pX, pY = self.Grid.Player.GetCoords()
        # Get Tiles around player
        nBlock = self.Grid.GetTileAt(pX,pY+1)
        eBlock = self.Grid.GetTileAt(pX+1,pY)
        sBlock = self.Grid.GetTileAt(pX,pY-1)
        wBlock = self.Grid.GetTileAt(pX-1,pY)
        # Test for walls
        if nBlock:
            valid.append(EnumDirection.STR_NORTH)
        if eBlock:
            valid.append(EnumDirection.STR_EAST)
        if sBlock:
            valid.append(EnumDirection.STR_SOUTH)
        if wBlock:
            valid.append(EnumDirection.STR_WEST)
        # Return the valid moves array
        return valid

    def DescribeSurroundings(self):
        count = 0
        directions = self.GetDescriptiveDirections()
        tiles = self.GetSurroundingTiles()
        for t in tiles:
            if len(directions) >= count:
                if t.__class__.__name__ != "Wall":
                    print(t.Describe(directions[count]))
            count += 1

    def GetPlayerMove(self):

        # Get a reference to the player
        player = self.Grid.Player

        # Flow control, ensure player makes a valid choice
        validChoice = False
        
        # Space out lines to preserve grid location in terminal window
        i = 4 - len(self.GetValidDirections())
        while i > 0:
            print("")
            i -= 1

        # Let the player know they cannot run
        if player.Exhausted:
            print("You are tired, and only WALK or SNEAK. In " + str(player.ExhaustedTurns) + " turns you can run again.")
        else:
            print("")

        print("How would you like to proceed?  \n\r")

        validCadences = []
        # Handle when the player is exhausted
        if player.Exhausted:
            print("Cadences: [SNEAK, WALK]")
            validCadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK ]
        else:
            print("Cadences: [SNEAK, WALK, RUN]")
            validCadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK, EnumCadence.STR_RUN ]

        validDirections = self.GetValidDirections()
        directionsString = "Directions: ["
        for i in range(len(validDirections)):
            if i is len(validDirections)-1:
                directionsString += validDirections[i]
            else:
                directionsString += validDirections[i] + ", "
        directionsString += "]\n\r"
        print(directionsString)

        # Only exit the loop when choice is validated
        while not validChoice:
            # Get the input from player
            tempChoice = raw_input("Type the Cadence and Direction, ex. run north, sneak east, or walk west \n\r|>")

            # Check input against valid inputs
            choiceString = tempChoice.split(" ")

            playerCandece = ""
            playerDirection = ""

            for cad in validCadences:
                if choiceString[0].upper() in cad:
                    # Selected Cadence
                    playerCandece = cad

            for dir in validDirections:
                if choiceString[1].upper() in dir:
                    #Selected Direction
                    playerDirection = dir;

            if playerCandece is not "" and playerDirection is not "":
                # Entered a valid choice for both
                validChoice = True
                # Set the choice at class level to operate
                self.PlayerChoice = (playerCandece, playerDirection)
            else:
                print("Unable to parse your choice, try again.")

        print("You decide to " + self.PlayerChoice[0] + " in the direction of " + self.PlayerChoice[1])


    def ProcessPlayerMove(self, doMove=True):

        # Split the tuple into parts
        playerCadance, playerDirection = self.PlayerChoice

        # Get the Destination Tile
        destTile = self.Grid.GetTileFromPlayerDirection(playerDirection)

        # Get the cadence index of the tile
        cadenceIndex = Utils.ConvertCadencetoInt(playerCadance)
        chance = destTile.TransitionChance[cadenceIndex]

        # Test the players luck against the tile
        success = Utils.TryChance(chance)

        # Success means moving the player
        if success:
            # If the player ran, instruct the player object to update itself.
            if playerCadance is EnumCadence.STR_RUN:
                self.Grid.Player.Run()
            else:
                self.Grid.Player.WalkOrSneak()

            # Move the player unless the agent calls this function
            # In that case, do not move the player.
            if doMove:
                # Finally move the player
                self.MovePlayer(playerDirection)

            # Check if the player has won
            if self.Grid.HasPlayerReachedExit():
                self.GameState = EnumGameState.PLAYER_WON
        else:
            # Not successful, the player has died
            self.GameState = EnumGameState.PLAYER_DEAD

    # Moves the player according to the direction
    def MovePlayer(self, direction):
        if direction == EnumDirection.STR_NORTH:
            # Go North
            xPos, yPos = self.Grid.Player.GetCoords()
            yPos += 1
            self.Grid.Player.SetCoords(xPos, yPos)
        elif direction == EnumDirection.STR_EAST:
            # Go North
            xPos, yPos = self.Grid.Player.GetCoords()
            xPos += 1
            self.Grid.Player.SetCoords(xPos, yPos)
        elif direction == EnumDirection.STR_SOUTH:
            # Go North
            xPos, yPos = self.Grid.Player.GetCoords()
            yPos -= 1
            self.Grid.Player.SetCoords(xPos, yPos)
        elif direction == EnumDirection.STR_WEST:
            # Go North
            xPos, yPos = self.Grid.Player.GetCoords()
            xPos -= 1
            self.Grid.Player.SetCoords(xPos, yPos)

    # Used by the AI Agent to shift the player while testing states
    def PlacePlayer(self, coords):
        # Split out the coordinates given
        newX, newY = coords
        # Directly update the player coordinates.
        self.Grid.Player.SetCoords(newX, newY)
