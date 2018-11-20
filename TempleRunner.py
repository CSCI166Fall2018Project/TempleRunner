# Import other Python files
from Objects import *
from GameEngine import *
import Utils

def main():
    testingMode = 3
    game_eng = GameEngine()
    if testingMode == 0:
        # Test generating a random level and picking a tile at random
        print("Testing a random grid, and a random tile in that grid.")
        game_eng.Grid.RandomizeLevel()
        tile = game_eng.Grid.GetTileAt(6, 6)
        # All Tiles
        print("Got a tile at 6,6: " + str(tile))
    elif testingMode == 1:
        # Testing how far the Player Agent can run before he becomes exhausted
        print("Testing how long it will take the Agent to become Exhausted.")
        game_eng.Grid.RandomizeLevel()
        game_eng.Grid.ShowGrid()
        count = 0
        while not game_eng.Grid.Player.Exhausted:
            game_eng.Grid.Player.Run()
            count += 1
        print("Player exhausted after " + str(count) + " turns")
    elif testingMode == 2:
        print("Testing a players legal moves in a random grid.")
        game_eng.Grid.RandomizeLevel()
        game_eng.Grid.ShowGrid()
        moves = game_eng.GetValidDirections()
        print(moves)
    elif testingMode == 3:
        print("Testing starting a new game, and displaying the interface")
        game_eng.StartGame()
        game_eng.DisplayGameState()

""" Run the Main function """
main()



"""
    Code Graveyard - Remove after several commits if not used
    
def TestingCode():
    print("Hello World!")

    # Created an Object and print it out
    tile = Tile()
    tile.Name = "Test Tile"
    print(" I just made a tile named: " + tile.Name)

    # Get a random number between 0 and 10
    r = Utils.RandBetween(0, 10)
    print("Random Number: " + str(r))

    # Testing a coin flip
    flipResult = Utils.TryChance(0.5)
    coin = ""

    if flipResult:
        coin = "Heads"
    else:
        coin = "Tails"
    print("Coin Result: " + coin)


"""