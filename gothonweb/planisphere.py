class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}

    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)


central_corridor = Room("Central Corridor",
"""
The Gothons of Planet Percal #25 have invaded your ship and destroyed
your entire crew/ You are the last surviving member and your last
mission is to get the neutron destruct bomb from the Weapons Armory, put
it in the bridge, and blow the ship up after getting into an escape pod.

You're running down the central corridor to the Weapons Armory when a
Gothon jumps out, red scaly skin, dark grimy teeth, and evil clown
costume flowing around his hate filled body. He's blocking the door to
the Armory and about to pull a weapon to blast you.
""")


laser_weapon_armory = Room("Laser Weapon Armory",
"""
Lucky for you they made you learn Gothon insults in the academy. You
tell the one Gothon joke you know: Lbhe zbgure vf fb sng, jura fur fvgf
nebhaq gur ubhfr, fur fvgf nebhaq gur ubhfr. The Gothon stops, tries
not to laugh, then busts out laughing and can't move. While he's
laughing you run up and shoot him square in the head putting him down,
then jump through the Weapon Armory door.

You do a dive roll into the Weapon Armory, crouch and scan the room for
more Gothons that might be hiding. It's dead quiet, too quiet. You
stand up and run to the far side of the room and find the neutron bomb
in its container. There's a keypad lock on the box and you need the
code to get the bomb out. Nearby the container you found a note:
    zero minutes for meditations:
    one person will change everything,
    he will have three attempts to choice -
    life or death. just two ways
If you get the code wrong three times then the lock closes forever
and you can't get the bomb. The code is 4 digits.
""")


the_bridge = Room("The Bridge",
"""
The container clicks open and the seal breaks, letting gas out. You
grab the neutron bomb and run as fast as you can to the bridge where you
must place it in the right spot.

You burst onto the Bridge with the netron destruct bomb under your arm
and surprise 5 Gothons who are trying to take control of the ship. Each
of them has an even uglier clown costume than the last. They haven't
pulled their weapons out yet, as they see the active bomb under your arm
and don't want to set it off.
""")


escape_pod = Room("Escape Pod",
"""
You point your blaster at the bomb under your arm and the Gothons put
their hands up and start to sweat. You inch backward to the door, open
it, and then carefully place the bomb on the floor, pointing your
blaster at it. You then jump back through the door, punch the close
button and blast the lock so the Gothons can't get out. Now that the
bomb is placed you run to the escape pod to get off this tin can.

You rush through the ship desperately trying to make it to the escape
pod before the whole ship explodes. It seems like hardly any Gothons
are on the ship, so your run is clear of interference. You get to the
chamber with the escape pods, and now need to pick one to take. Some of
them could be damaged but you don't have time to look. There's 5 pods,
which one do you take?
""")


the_end_winner = Room("The End",
"""
You jump into pod 2 and hit the eject button. The pod easily slides out
into space heading to the planet below. As it flies to the planet, you
look back and see your ship implode then explode like a bright star,
taking out the Gothon ship at the same time. You won!
""")


the_end_loser = Room("The End",
"""
You jump into a random pod and hit the eject button. The pod escapes
out into the void of space, then implodes as the hull ruptures, crushing
your body into jam jelly.
""")


escape_pod.add_paths({
    '2': the_end_winner,
    '1': the_end_loser,
    '3': the_end_loser,
    '4': the_end_loser,
    '5': the_end_loser
})


bridge_death = Room("death",
"""
You're using all your strength to get that bomb up in the air. Veins
swell. I have only one thought in my head: I will be able to escape.
You throw a bomb and it goes off at the same time. Your pieces are
scattered colorfully in space.
""")


the_bridge.add_paths({
    'throw the bomb': bridge_death,
    'slowly place the bomb': escape_pod
})


armory_death = Room("death",
"""
Sweat broke out on your forehead. You've wasted your last attempt.
Something clicked inside the chest. Can it?! No, the lid didn't
open... And that means only one thing: it didn't work out. After
a couple of minutes, the laughter outside the door ended, as did
your time. One shot - one kill.
""")


laser_weapon_armory.add_paths({
    '0132': the_bridge,
    #'*': armory_death
})


cor_shoot_death = Room("death",
"""
The wrong man was attacked! Remembering the battle Academy, you
quickly pulls out a gun and a shot sounds. I wish you had fired
the shot.
""")


cor_dodge_death = Room("death",
"""
The wrong man was attacked! Remembering the battle Academy, you
performed a lightning roll forward and dodged bullets. Well,
that's what you thought at the time. In fact, you stumbled and
just fell, although you still dodged the shot. The first shot.
But you didn't hear the second one.
""")


central_corridor.add_paths({
    'shoot': cor_shoot_death,
    'dodge': cor_dodge_death,
    'tell a joke': laser_weapon_armory
})


START = 'central_corridor'

def load_room(name): #?????????????????? ?????? ??????????????
    """
    There is a potential security problem here.
    Who gets to set name? Can that expose a variable?
    """
    return globals().get(name) #???????????????????? ???????????? ???????????? Room

def name_room(room): # ?????????????????? ???????????? ???????????? Room
    """
    Same possible security problem. Can you trust room?
    What's a better solution than this globals lookup?
    """
    for key, value in globals().items():
        # value - ???????????? ????????????; key - ????????????????????, ???? ?????????????? ?????????????????? ????????????
        if value == room:
            return key # ???????????????????? ?????? ????????????????????
