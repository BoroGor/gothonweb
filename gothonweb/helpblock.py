tips = {'Central Corridor': ['shoot', 'dodge', 'tell a joke'],
        'Laser Weapon Armory': ['ZERO ONE TREE TWO'],
        'The Bridge': ['throw the bomb', 'slowly place the bomb'],
        'Escape Pod': ['2'],
        }

def help(roomname):
    return tips.get(roomname)
