

# Import other Python files
import Objects
import Utils


def main():
    print("Hello World!")

    # Created an Object and print it out
    tile = Objects.Tile()
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



""" Run the Main function """
main()