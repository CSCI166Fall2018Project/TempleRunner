# Import other Python files
from GameEngine import *
from ValueIterationAgent import *
from PolicyIteration import *
from QLearningAgents import *
from AgentRunner import *

def main():

    choosenCorrectly = False
    while not choosenCorrectly:
        print("Play the game, test, or run agents?")
        choice = raw_input("Choose: play | test | run\n\r|> ")

        # Check for correct responses
        if "PLAY" in choice.upper() or "TEST" in choice.upper() or "RUN" in choice.upper():
            # Has choosen correctly
            choosenCorrectly = True

            # Choose to play
            if "PLAY" in choice.upper():
                game_eng = GameEngine()
                game_eng.StartGame()

            if "TEST" in choice.upper():
                print("Test Value Iteration, Policy Iteration, or Q-Learning?")
                choice = raw_input("Choose from: value, policy, qlearning \n\r|> ")
                if "VALUE" in choice.upper():
                    game_eng = GameEngine()
                    agentConfigured = False
                    while not agentConfigured:
                        discountChoice = input("Discount: ")
                        iterationsChoice = input("Iterations: ")
                        if discountChoice > 0.0 and discountChoice <= 1.0 and iterationsChoice > 0 and iterationsChoice < 9999:
                            agentConfigured = True

                    iterationAgent = ValueIterationAgent(game_eng, discountChoice, iterationsChoice)

                    print("Values Generated! Would you like to see the Values, or the Policy extract from them?")
                    choice = raw_input("Choose from: values, policy or both.\n\r|> ")
                    if "VALUES" in choice.upper() or "POLICY" in choice.upper() or "BOTH" in choice.upper():
                        if "VALUES" in choice.upper():
                            # Show the game Grid
                            print("Game Grid:")
                            game_eng.Grid.ShowGrid()
                            iterationAgent.ShowValuesInGrid()
                        if "POLICY" in choice.upper():
                            # Show the game Grid
                            print("Game Grid:")
                            game_eng.Grid.ShowGrid()
                            iterationAgent.ShowPolicyFromValues()
                        if "BOTH" in choice.upper():
                            # Show the game Grid
                            print("Game Grid:")
                            game_eng.Grid.ShowGrid()
                            iterationAgent.ShowValuesInGrid()
                            iterationAgent.ShowPolicyFromValues()
                if "POLICY" in choice.upper():
                    game_eng = GameEngine()
                    policyIterationAgent = PolicyIterationAgent(game_eng)
                if "QLEARN" in choice.upper():
                    game_eng = GameEngine()
                    qlearningAgent = QLearningAgent(game_eng)
            elif "RUN" in choice.upper():
                game_eng = GameEngine()
                print("Value Iteration Agent will play the game")
                print("Show Graphics? (yes | no)")
                showGraphics = raw_input("Choice: ")
                if "YES" in showGraphics.upper() or "NO" in showGraphics.upper():
                    if "YES" in showGraphics.upper():
                        showGraphics = True
                    else:
                        showGraphics = False
                # Agent configuration
                agentConfigured = False
                while not agentConfigured:
                    discountChoice = input("Discount: ")
                    iterationsChoice = input("Iterations: ")
                    if discountChoice > 0.0 and discountChoice <= 1.0 and iterationsChoice > 0 and iterationsChoice < 9999:
                        agentConfigured = True
                # Create Agent
                iterationAgent = ValueIterationAgent(game_eng, discountChoice, iterationsChoice)
                print("Value Iteration complete!")
                # Create the agent runner to test the policy extracted by the ValueIterationAgent
                agentRunner = AgentRunner(iterationAgent, game_eng, showGraphics)
                # Run the agent through the game 100 times
                agentRunner.RunGames(100)

        else:
            # Tell them to choose again
            print("Incorrect choice.")


""" Run the Main function """
main()
