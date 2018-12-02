# Import other Python files
from GameEngine import *
from ValueIterationAgent import *

def main():

    choosenCorrectly = False
    while not choosenCorrectly:
        print("Play the game, or test agents?")
        choice = raw_input("Choose: play or test\n\r|> ")

        # Check for correct responses
        if "PLAY" in choice.upper() or "TEST" in choice.upper():
            # Choose to play
            if "PLAY" in choice.upper():
                game_eng = GameEngine()
                game_eng.StartGame()

            if "TEST" in choice.upper():
                print("Test Value or Policy Iteration?")
                choice = raw_input("Choose from: value or policy \n\r|> ")
                if "VALUE" in choice.upper():
                    game_eng = GameEngine()
                    iterationAgent = ValueIterationAgent(game_eng)
                if "POLICY" in choice.upper():
                    game_eng = GameEngine()
                    policyIterationAgent = PolicyIteation(game_eng)
            
        else:
            # Tell them to choose again
            print("Incorrect choice.")


""" Run the Main function """
main()
