import random

def roll_d3():
    return random.randint(1, 3)

def roll_d6():
    return random.randint(1, 6)

def roll_2d6():
    return random.choices(
            range(2,13), weights=[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])[0]

def roll_3d6():
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

def roll_4d6():
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

def roll_5d6():
    return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
