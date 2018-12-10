from Objects import *
from time import *
from Utils import *

class AgentRunner:

    def __init__(self, pAgent, pEngine, graphics=False):
        self.agent = pAgent
        self.engine = pEngine
        self.showGraphics = graphics
        self.wins = 0
        self.loses = 0


    # Run the agent X times
    def RunGames(self, iterations=100):
        for i in range(0, iterations, 1):
            self.PlayGame()

        print("Out of " + str(iterations) + " games, the Agent won " + str(self.wins) + " games.")
        percent = float(self.wins) / float(iterations)
        winRate = round(percent, 2) * 100
        print("Agent Win Rate: " + str(winRate) + "%")

    # Function to use the Agent to play the game
    def PlayGame(self):
        while self.engine.GameState == EnumGameState.PLAYER_ALIVE:

            # Get a reference to the player
            player = self.engine.Grid.Player

            # Valid directions to take
            validDirections = self.engine.GetValidDirections()

            # Let the player know they cannot run
            if player.Exhausted:
                if self.showGraphics:
                    print("You are tired, and only WALK or SNEAK. In " + str(
                player.ExhaustedTurns) + " turns you can run again.")

            validCadences = []
            # Handle when the player is exhausted
            if player.Exhausted:
                validCadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK]
            else:
                validCadences = [EnumCadence.STR_SNEAK, EnumCadence.STR_WALK, EnumCadence.STR_RUN]

            # Update the Player choice with the Agents choice
            pX, pY = self.engine.Grid.Player.GetCoords()
            currentTile = self.engine.Grid.GetTileAt(pX, pY, True)
            self.engine.PlayerChoice = self.agent.GetActionFromState(currentTile)


            # Process the move, collisions, and possible change of game state
            self.engine.ProcessPlayerMove()

            if self.showGraphics:
                sleep(0.5)
                # Show the grid locations
                self.engine.DisplayGameState(False)

        if self.engine.GameState == EnumGameState.PLAYER_DEAD:
            self.loses += 1
            if self.showGraphics:
                ShowDeath()
            self.ResetGame()

        if self.engine.GameState == EnumGameState.PLAYER_WON:
            self.wins += 1
            if self.showGraphics:
                ShowWin()
            self.ResetGame()

    def ResetGame(self):

        # Reset the game state
        self.engine.GameState = EnumGameState.PLAYER_ALIVE

        # move the player back to start
        startPos = 0, 0
        self.engine.PlacePlayer(startPos)

        # Reset the players exhaustion
        self.engine.Grid.Player.Exhausted = False
        self.engine.Grid.Player.ChanceToExhaust = 0.05
