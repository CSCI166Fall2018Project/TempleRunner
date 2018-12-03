# Import other Python files
from GameEngine import *
from ValueIterationAgent import *
from PolicyIteration import *
from QLearningAgents import *

def main():

    choosenCorrectly = False
    while not choosenCorrectly:
        print("Play the game, or test agents?")
        choice = raw_input("Choose: play or test\n\r|> ")

        # Check for correct responses
        if "PLAY" in choice.upper() or "TEST" in choice.upper():
            # Has choosen correctly
            choosenCorrectly = True

            # Choose to play
            if "PLAY" in choice.upper():
                game_eng = GameEngine()
                game_eng.StartGame()

            if "TEST" in choice.upper():
                print("Test Value Iteration, Policy Iteration, or Q-Learning?")
                choice = raw_input("Choose from: value, policy, qlearn \n\r|> ")
                if "VALUE" in choice.upper():
                    game_eng = GameEngine()
                    iterationAgent = ValueIterationAgent(game_eng, 0.75, 100)
                    print("Values Generated! Would you like to see the Values, or the Policy extract from them?")
                    choice = raw_input("Choose from: values, policy or both.\n\r|> ")
                    if "VALUES" in choice.upper() or "POLICY" in choice.upper():
                        if "VALUES" in choice.upper():
                            iterationAgent.ShowValuesInGrid()
                        if "POLICY" in choice.upper():
                            iterationAgent.ShowPolicyFromValues()
                        if "BOTH" in choice.upper():
                            iterationAgent.ShowValuesInGrid()
                            iterationAgent.ShowPolicyFromValues()
                if "POLICY" in choice.upper():
                    game_eng = GameEngine()
                    policyIterationAgent = PolicyIterationAgent(game_eng)
                if "QLEARN" in choice.upper():
                    game_eng = GameEngine()
                    qlearningAgent = QLearningAgent(game_eng)
        else:
            # Tell them to choose again
            print("Incorrect choice.")


""" Run the Main function """
main()
