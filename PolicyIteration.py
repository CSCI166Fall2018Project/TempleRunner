from GameEngine import *

#Player always starts at bottom left corner and exit is always at top right corner
#Follow a policy where the player will only travel North and East

class PolicyIterationAgent:

    def __init__(self, engine, discount=0.5, iterations=100):

        # Keep a reference to the GameEngine
            self.engine = engine
            # Set our Value Iteration vars
            self.values = {}
            self.discount = discount
            self.iterations = iterations