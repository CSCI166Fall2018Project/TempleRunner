from GameEngine import *


class QLearningAgent:
    
    def __init__(self, engine, discount=0.5, iterations=100):
        
        self.engine = engine
        self.qValues = {}
        
        if isinstance(engine, GameEngine):
            pass
                    
        else:
            print(" Please use the GameEngine as the first argument")
            return
        
    def getQValue(self, state, action):
        
        if (state, action) not in self.qValues:
            return 0.0
        else:
            return self.qValues[(state, action)]
