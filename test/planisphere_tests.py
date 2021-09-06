from nose.tools import *
from gothonweb.planisphere import *


def test_room():
    gold = Room("GoldRoom",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert_equal(gold.name, "GoldRoom")
    assert_equal(gold.paths, {})

def test_room_paths():
    center = Room("Center", "Test room in the center.")
    north = Room("North", "Test room in the north.")
    south = Room("South", "Test room in the south.")

    center.add_paths({'north': north, 'south': south})
    assert_equal(center.go('north'), north)
    assert_equal(center.go('south'), south)

def test_map():
    start = Room("Start", "You can go west and down a hole.")
    west = Room("Trees", "There are trees here, you can go east.")
    down = Room("Dungeon", "It's dark down here, you can go up.")

    start.add_paths({'west': west, 'down': down})
    west.add_paths({'east': start})
    down.add_paths({"up": start})

    assert_equal(start.go('west'), west)
    assert_equal(start.go('west').go('east'), start)
    assert_equal(start.go('down').go('up'), start)

def test_gothon_game_map():
    start_room = load_room(START)
    # проверка смертельных путей
    assert_equal(start_room.go('shoot'), cor_shoot_death)
    assert_equal(start_room.go('dodge'), cor_dodge_death)
    # проверка возврата при вводе несуществующих вариантов
    assert_equal(start_room.go('hgh123'), None)

    # переход в оружейную
    laser_room = start_room.go('tell a joke')
    # проверка того, что перешли в верную комнату
    assert_equal(laser_room, laser_weapon_armory)

    # переход на мост
    bridge_room = laser_room.go('0132')
    # проверка того, что перешли в верную комнату
    assert_equal(bridge_room, the_bridge)
    # проверка смертельных путей
    assert_equal(bridge_room.go('throw the bomb'), bridge_death)

    # переход к спастельным капсулам
    pod_room = bridge_room.go('slowly place the bomb')
    # проверка того, что перешли в верную комнату
    assert_equal(pod_room, escape_pod)
    # проверка выигрыша
    assert_equal(pod_room.go('2'), the_end_winner)
    # проверка проигрыша
    assert_equal(pod_room.go('1'), the_end_loser)
