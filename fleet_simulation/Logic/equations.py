import math
import random


def jam_result(self, target):
    return random.random() <= self.jam_strength / target.sensor_strength


# def lock_time(self, target):
#     return 40000 / (self.scan_res * (math.asinh(target.signature) * math.asinh(target.signature)))


def effective_hp(self, damage_type):
    if "em" in damage_type:
        return [self.shield_resistances_hp[4] / (1 - self.shield_resistances_hp[0]) , self.armor_resistances_hp[4] / (
                1 - self.armor_resistances_hp[0]) , self.hull_resistances_hp[4] / (
                       1 - self.hull_resistances_hp[0])]
    elif "thermal" in damage_type:
        return [self.shield_resistances_hp[4] / (1 - self.shield_resistances_hp[1]) , self.armor_resistances_hp[4] / (
                1 - self.armor_resistances_hp[1]) , self.hull_resistances_hp[4] / (
                       1 - self.hull_resistances_hp[1])]
    elif "kinetic" in damage_type:
        return [self.shield_resistances_hp[4] / (1 - self.shield_resistances_hp[2]) , self.armor_resistances_hp[4] / (
                1 - self.armor_resistances_hp[2]) , self.hull_resistances_hp[4] / (
                       1 - self.hull_resistances_hp[2])]
    elif "explosive" in damage_type:
        return [self.shield_resistances_hp[4] / (1 - self.shield_resistances_hp[3]) , self.armor_resistances_hp[4] / (
                1 - self.armor_resistances_hp[3]) , self.hull_resistances_hp[4] / (
                       1 - self.hull_resistances_hp[3])]


def effective_dps(self, damage_type):
    if "em" in damage_type:
        return self.em_dps
    elif "thermal" in damage_type:
        return self.thermal_dps
    elif "kinetic" in damage_type:
        return self.kinetic_dps
    elif "explosive" in damage_type:
        return self.explosive_dps
    else:
        return 0
