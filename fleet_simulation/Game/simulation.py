import sys
import random
import time
from collections import Counter

from fleet_simulation.Models import dps_ships, logi_ships, ecm_ships
from fleet_simulation.Logic import equations

FLEET_SIZE = 10
BATTLE_TIME = 5000


def main() -> int:
    # do something
    fleet1 = generate_fleet(FLEET_SIZE)
    fleet2 = generate_fleet(FLEET_SIZE)
    # print(str(len(fleet1)))
    fleet1_comp = count_ship_types(fleet1)
    print('Damage: ' + str(fleet1_comp[0]) + ' Logistics: ' + str(fleet1_comp[1])
          + ' EWAR: ' + str(fleet1_comp[2]))
    fleet2_comp = count_ship_types(fleet2)
    print('Damage: ' + str(fleet2_comp[0]) + ' Logistics: ' + str(fleet2_comp[1])
          + ' EWAR: ' + str(fleet2_comp[2]))
    battle_space(fleet1, fleet2, generate_damage_type(), generate_damage_type())


def battle_space(fleet1, fleet2, fleet1_damage, fleet2_damage):
    fleet1_score = 0
    fleet2_score = 0
    tick = 0

    while tick < BATTLE_TIME:
        # Select Primary for Fleet1
        primary1 = generate_damage_target(fleet1)
        # Select Primary for Fleet2
        primary2 = generate_damage_target(fleet2)

        # Fleet1 begin applying damage
        dps_wing1 = generate_sub_fleet(fleet1, "Damage")
        for x in range(len(dps_wing1)):
            if not dps_wing1[x].destroyed:
                if primary2 is not None:
                    primary2.armor_damage += equations.effective_dps(dps_wing1[x], fleet1_damage)
        # print("Fleet2 Target: " + str(primary2.armor_damage))

        # Fleet2 begin applying damage
        dps_wing2 = generate_sub_fleet(fleet2, "Damage")
        for y in range(len(dps_wing2)):
            if not dps_wing2[y].destroyed:
                if primary1 is not None:
                    primary1.armor_damage += equations.effective_dps(dps_wing2[y], fleet2_damage)
        # print("Fleet1 Target: " + str(primary1.armor_damage))

        # Check Fleet1 for Destroyed Ships
        # print(equations.effective_hp(primary1, fleet2_damage)[1])
        if primary1 is not None:
            if primary1.armor_damage > equations.effective_hp(primary1, fleet2_damage)[1]:
                primary1.target_destroyed()
                fleet2_score += 1
                print("Fleet1 Loses a " + str(primary1.name) + " at minute " + str(tick / 60))

        # Check Fleet2 for Destroyed Ships
        if primary2 is not None:
            if primary2.armor_damage > equations.effective_hp(primary2, fleet1_damage)[1]:
                primary2.target_destroyed()
                fleet1_score += 1
                print("Fleet2 Loses a " + str(primary2.name) + " at minute " + str(tick / 60))

        if tick % 20 == 0:
            # Select first jam targets for Fleet1
            generate_jammed_targets(fleet1, tick)
            # Select first jam targets for Fleet2
            generate_jammed_targets(fleet2, tick)

        # Select
        broadcast1 = generate_logistics_target(fleet1)
        broadcast2 = generate_logistics_target(fleet2)

        # Fleet1 begin attempting to repair damage
        logi_wing1 = generate_sub_fleet(fleet1, "Logistics")
        for z in range(len(logi_wing1)):
            if not logi_wing1[z].destroyed and not logi_wing1[z].jammed:
                if broadcast1 is not None:
                    broadcast1.armor_damage -= logi_wing1[z].remote_armor
        # print(broadcast1.armor_damage)

        # Fleet1 begin attempting to repair damage
        logi_wing2 = generate_sub_fleet(fleet2, "Logistics")

        for a in range(len(logi_wing2)):
            if not logi_wing2[a].destroyed and not logi_wing2[a].jammed:
                if broadcast2 is not None:
                    broadcast2.armor_damage -= logi_wing2[a].remote_armor
        # print(broadcast2.armor_damage)

        tick += 1

    if fleet1_score < fleet2_score:
        print("Fleet2 Wins!")
    elif fleet1_score > fleet2_score:
        print("Fleet1 Wins!")
    else:
        print("Tie")


# Helper Functions

def generate_fleet(fleet_size):
    return [dps_ships.Damnation(), dps_ships.Damnation(), dps_ships.Damnation(), dps_ships.Damnation(),
            logi_ships.Guardian(), logi_ships.Guardian(), logi_ships.Guardian(), logi_ships.Guardian(),
            ecm_ships.ArmorScorpion()]
    # return random.choices([dps_ships.Damnation(), logi_ships.Guardian(), ecm_ships.ArmorScorpion()],
    #                       [3, 2, 1], k=fleet_size - len(minimum)) + minimum


def generate_damage_type():
    # return random.choices(['em', 'thermal', 'kinetic', 'explosive'])
    return 'em'


def generate_damage_target(target_fleet):
    for x in range(len(target_fleet)):
        if not target_fleet[x].destroyed:
            return target_fleet[x]


def generate_logistics_target(fleet):
    for x in range(len(fleet)):
        if not fleet[x].destroyed and fleet[x].armor_damage > 0:
            return fleet[x]


def generate_jammed_targets(fleet, tick):
    ecm_wing = generate_sub_fleet(fleet, "Electronic Attack Ship")
    logi_wing = generate_sub_fleet(fleet, "Logistics")
    target = 0
    jams = 0
    for x in range(len(ecm_wing)):
        for y in range(ecm_wing[x].jam_modules):
            # Check to see if target is jammed
            if target < len(logi_wing):
                logi_wing[target].jammed = False
                if not logi_wing[target].jammed and not logi_wing[target].destroyed:
                    # If not jammed, attempt to jam target.
                    if equations.jam_result(ecm_wing[x], logi_wing[target]):
                        logi_wing[target].target_jammed()
                        target += 1
                        jams += 1
    if jams >= 3: print("BREAK!!!: " + str(tick / 60))


def generate_ship_loss(fleet):
    for x in range(len(fleet)):
        if fleet[x].armor_damage >= fleet[x].armor_resistances[4] and not fleet[x].destroyed:
            fleet[x].target_destoryed()


def generate_sub_fleet(fleet, ship_type):
    type_fleet = []
    for x in range(len(fleet)):
        if ship_type == fleet[x].ship_type:
            type_fleet.append(fleet[x])
    return type_fleet


def count_ship_types(fleet):
    dps_count = 0
    logi_count = 0
    ecm_count = 0
    for x in range(len(fleet)):
        if fleet[x].ship_type == "Damage":
            dps_count += 1
        elif fleet[x].ship_type == "Logistics":
            logi_count += 1
        elif fleet[x].ship_type == "Electronic Attack Ship":
            ecm_count += 1
    return [dps_count, logi_count, ecm_count]


def count_destroyed_ships(fleet):
    losses = 0
    for x in range(len(fleet)):
        if fleet[x].destroyed:
            losses += 1
    return losses


if __name__ == '__main__':
    sys.exit(main())
