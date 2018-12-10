
# Import useful helper files
import random
import Objects

# Returns True when random number falls in chance percent
def TryChance(probability):

    # Test int between 0 and 100
    test = random.randint(0, 100)
    # Create split to see if Test is within that range
    split = probability * 100
    # If test lower than split, it's a hit
    if test <= split:
        return True
    else:
        return False


def RandBetween(x, y):
    return random.randint(x, y)


# Used to convert the string form of Cadence into the Integer form
def ConvertCadencetoInt(enum):
    if enum == Objects.EnumCadence.STR_SNEAK:
        return 0
    elif enum == Objects.EnumCadence.STR_WALK:
        return 1
    elif enum == Objects.EnumCadence.STR_RUN:
        return 2
    else:
        return


def ShowDeath():
    print("__   __           ______ _          _ ")
    print("\ \ / /           |  _  (_)        | |")
    print(" \ V /___  _   _  | | | |_  ___  __| |")
    print("  \ // _ \| | | | | | | | |/ _ \/ _` |")
    print("  | | (_) | |_| | | |/ /| |  __/ (_| |")
    print("  \_/\___/ \__,_| |___/ |_|\___|\__,_|")
    print("                                      ")

def ShowWin():
    print("__   __            _    _             _ ")
    print("\ \ / /           | |  | |           | |")
    print(" \ V /___  _   _  | |  | | ___  _ __ | |")
    print("  \ // _ \| | | | | |/\| |/ _ \| '_ \| |")
    print("  | | (_) | |_| | \  /\  / (_) | | | |_|")
    print("  \_/\___/ \__,_|  \/  \/ \___/|_| |_(_)")


