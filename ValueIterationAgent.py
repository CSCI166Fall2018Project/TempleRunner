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
            for i in range(0,self.iterations):
                # Create a copy of previous state values
                values_prime = self.values.copy()
                #Loop through all states
                for state in gameStates:
                    print(state)





        else:
            print(" Please use the GameEngine as the first argument")
            return







        # End Value iteration code
        return

    # Incoming State should be the tile coordinates
    # Ex. state = (4,6)
    def getValue(self, state):
        return self.values[state]
