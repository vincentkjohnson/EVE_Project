import random
import sys
from numpy.random import choice

FLEET_SIZE = 20;


def main() -> int:
    simulation()


def simulation():
    fleet1 = generate_fleet()
    fleet2 = generate_fleet()
    print(fleet1)
    print('Damage:' + str(fleet1.count('D')) + ' Logistics:' + str(fleet1.count('L')) + ' EWAR:' + str(fleet1.count('E')))
    print('\n')
    print(fleet2)
    print('Damage:' + str(fleet2.count('D')) + ' Logistics:' + str(fleet2.count('L')) + ' EWAR:' + str(fleet2.count('E')))
    score = game_match(fleet1, fleet2)
    if score < 0:
        print('\nFleet1')
    elif score == 0:
        print('\nTie')
    else:
        print('\nFleet 2')


def game_match(fleet1, fleet2):
    score = 0;
    for x in range(FLEET_SIZE):
        ship1 = fleet1.pop()
        ship2 = fleet2.pop()
        result = dle(ship1, ship2)
        score += result
    return score


def dle(ship1, ship2):
    if ship1 == ship2:
        return 0
    elif ship1 + ship2 in ['EL', 'LD', 'DE']:
        return -1
    else:
        return 1


def generate_fleet():
    return random.choices(['D', 'L', 'E'], [60, 40, 20], k=FLEET_SIZE)


if __name__ == '__main__':
    sys.exit(main())
