from GameEngine import *


class ValueIterationAgent:

    def __init__(self, engine, discount=0.5, iterations=100):

        # Keep a reference to the GameEngine
        self.engine = engine
        # Set our Value Iteration vars
        self.values = {}
        self.discount = discount
        self.iterations = iterations

        # Value Iteration Code BEGINS HERE

        # Make sure the engine passed in is the GameEngine
        if isinstance(engine, GameEngine):
            # Get all States
            gameStates = self.engine.GetAllStates()

            # Loop through interations
            for i in range(0, self.iterations):
                # Create a copy of previous state values
                values_prime = self.values.copy()
                #Loop through all states
                for state in gameStates:
                    prime_values = []
                    # If the state is a wall, it's terminal. Assign it 0
                    if isinstance(state, Wall):
                        self.values[state] = 0.00
                        continue
                    # Place the player at this state to test their actions
                    self.engine.PlacePlayer(state.GetCoords())
                    # print("Testing at state:" + str(state))
                    for direction, cadence in self.engine.GetAllPossibleActions():
                        # print("Direction: " + direction + " | Cadence: " + cadence)
                        val_prime = 0
                        statePrime, probability = self.engine.GetTransitionStateAndProb(direction, cadence)
                        # Obtain the sum of Reward(s) + Discount * (P(s'| s,a)*R(s'))
                        reward = engine.GetReward(state, cadence)
                        # For the first run, sometimes the state is not in the array
                        stateKeys = values_prime.keys()
                        if statePrime not in stateKeys:
                            values_prime[statePrime] = 0.0
                        oldValPrime = values_prime[statePrime]
                        val_prime = probability * (reward + (self.discount * oldValPrime))
                        prime_values.append(val_prime)
                    if len(prime_values) > 0:
                        self.values[state] = round(max(prime_values), 2)
                    else:
                        self.values[state] = 0

        else:
            print(" Please use the GameEngine as the first argument")
            return

        # End Value iteration code

        # Reset the Player Position
        self.engine.PlacePlayer((0, 0))

        return

    # Show the values of each tile in a list form
    def ListValues(self):

        for key in self.values.keys():
            print(str(key)),
            if (str(key).startswith('Wall')):
                print("    "),
            elif (str(key).startswith('Tile')):
                print("    "),
            elif (str(key).startswith('TrapDoor')):
                print(""),
            print(" | " + str(self.values[key]))

    # Displays the values in a Grid form
    def ShowValuesInGrid(self):

        # Show the game Grid
        print("Game Grid:")
        self.engine.Grid.ShowGrid()

        finalString = ""
        # Handle Columns
        for y in range(self.engine.Grid.Size-1, -1, -1):
            # Handle Rows
            for x in range(0, self.engine.Grid.Size, 1):
                tile = self.engine.Grid.GetTileAt(x, y, True)
                if tile:
                    finalString += "[" + str(self.GetValue(tile)) + "]\t"
            finalString += "\n\r"
        print("Discount: " + str(self.discount) + " | Iterations: " + str(self.iterations))
        print("Iteration Agent Values:")
        print(finalString)


    # Incoming State should be the tile object itself
    def GetValue(self, state):
        return self.values[state]


    def ShowPolicyFromValues(self):
        # Show the game Grid
        print("Game Grid:")
        self.engine.Grid.ShowGrid()

        finalString = ""
        # Handle Columns
        for y in range(self.engine.Grid.Size - 1, -1, -1):
            # Handle Rows
            for x in range(0, self.engine.Grid.Size, 1):
                tile = self.engine.Grid.GetTileAt(x, y, True)
                # Place the player at this state to test their actions
                self.engine.PlacePlayer(tile.GetCoords())
                if tile:
                    finalString += "[" + self.GetActionFromValues(tile) + "]"
            finalString += "\n\r"
        print("Discount: " + str(self.discount) + " | Iterations: " + str(self.iterations))
        print("Legend: [ {Cadence} {Direction} ]")
        print(" S = Sneak, W = Walk, R = Run ")
        print(" N = North, E = East, S = South, W = West ")
        print("Optimal Policy:")
        print(finalString)
        # Reset the Player Position
        self.engine.PlacePlayer((0, 0))

    def GetActionFromValues(self, state):
        # If the state is a wall, it's terminal.
        if isinstance(state, Wall):
            return "##"
        elif isinstance(state, ExitDoor):
            return "EX"
        else:
            # Get all possible actions from this state, and find the best one
            bestAction = None
            bestValue = -9999999999
            for direction, cadence in self.engine.GetAllPossibleActions():
                valPrime = 0
                statePrime, probability = self.engine.GetTransitionStateAndProb(direction, cadence)
                # Obtain the sum of Reward(s) + Discount * (P(s'| s,a)*R(s'))
                reward = self.engine.GetReward(state, cadence)
                # For the first run, sometimes the state is not in the array
                val_prime = probability * (reward + (self.discount * self.values[statePrime]))

                if val_prime > bestValue:
                    bestValue = val_prime
                    bestAction = cadence[0] + direction[0]
            return bestAction