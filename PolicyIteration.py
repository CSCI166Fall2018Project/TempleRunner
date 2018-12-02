from GameEngine import *

#Player always starts at bottom left corner and exit is always at top right corner
#Follow a policy where the player will only travel as far East as possible then as far North as Possible,
#if agent can't go either North or East go South then repeat 

class PolicyIterationAgent:

    def __init__(self, engine):

        # Keep a reference to the GameEngine
            self.engine = engine
            # Set our Value Iteration vars
            self.values = {}
            self.discount = discount
            self.iterations = iterations