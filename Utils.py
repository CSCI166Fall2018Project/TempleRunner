
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