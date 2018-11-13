# Import other Python files
from Objects import *
from GameEngine import *
import Utils

def main():
    testingMode = 1
    GameEng = GameEngine()
    if testingMode == 0:
        # Test generating a random level and picking a tile at random
        print("Testing a random grid, and a random tile in that grid.")
        GameEng.Grid.RandomizeLevel()
        tile = GameEng.Grid.GetTileAt(6, 6)
        # All Tiles
        print("Got a tile at 6,6: " + str(tile))
    elif testingMode == 1:
        # Testing how far the Player Agent can run before he becomes exhausted
        print("Testing how long it will take the Agent to become Exhausted.")
        GameEng.Grid.RandomizeLevel()
        GameEng.Grid.ShowGrid()
        count = 0
        while not GameEng.Grid.Player.Exhausted:
            GameEng.Grid.Player.Run()
            count += 1
        print("Player exhasted after " + str(count) + " turns")
    elif testingMode == 2:
        print("Testing a players legal moves in a random grid.")
        GameEng.Grid.RandomizeLevel()
        GameEng.Grid.ShowGrid()
        moves = GameEng.GetValidDirections()
        print(moves)


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