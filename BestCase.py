import random
import sys
from collections import namedtuple
from itertools import groupby

# The number of targets (e.g Guards) being jammed and their sensor strength.
NUM_TARGETS = 5
TARGET_STRENGTH = 112

# A list of jam strength for jams set and then forgotten about (e.g. Damnations
# or Kitsunes).
# The program will assume they evenly distributed amongst targets by jam type
# and then forgotten about. So e.g. they will not try to jam a different target
# if the first jam lands.

#>>LAZY JAMS<<
DAMNATION_JAMS = [6.21 for _ in range(0)]  # [5 for _ in range(10)]
KITSUNE_JAMS = [13.4 for _ in range(8)]

# A list of jam strength on active ships (e.g. Scorpion) and their jam strength.
# The program will assume these are perfectly distributed amongst ships as jams
# land (e.g. so it will not double-jam a target unless it has more successful
# jams than targets)
SCORPION_JAMS = [8.5 for _ in range(7)]
TENGU_JAMS = [10.6 for _ in range(5)]

# How many cycles will happen in the battle.
NUM_CYCLES = 90  # 90 cycles corresponds to a 30 minute fight

# Number of jams that will result in something bad (e.g a ship dying)
CRIT_THRESHOLD = 4

# How many simulations to do.
SIMULATION_RUNS = 10000

BattleAnalysis = namedtuple("BattleAnalysis",
                            [
                                "averageJamsPerCycle",
                                "maxJams",
                                "minJams",
                                "critCycles",
                                "longestCritStreak"
                            ])


def main() -> int:
    jam_dist = list(distribute_lazy_jams())
    battle_results = list(run_simulation(jam_dist))

    average_jams = sum([x.averageJamsPerCycle for x in battle_results]) / SIMULATION_RUNS
    average_max_jams = sum([x.maxJams for x in battle_results]) / SIMULATION_RUNS
    average_min_jams = sum([x.minJams for x in battle_results]) / SIMULATION_RUNS
    average_crit_cycles = sum([x.critCycles for x in battle_results]) / SIMULATION_RUNS
    average_longest_crit_streak = sum([x.longestCritStreak for x in battle_results]) / SIMULATION_RUNS

    print("Average Jams/Cycle:            {}".format(average_jams))
    print("Average Max Jams:              {}".format(average_max_jams))
    print("Average Min Jams:              {}".format(average_min_jams))
    print("Average Number of Crit Cycles: {}".format(average_crit_cycles))
    print("Average Longest Crit Streak:   {}".format(average_longest_crit_streak))


def run_simulation(jam_dist):
    for i in range(SIMULATION_RUNS):
        results = [single_cycle(jam_dist) for _ in range(NUM_CYCLES)]
        yield battle_analysis(results)


def battle_analysis(results):
    average_jams = sum(results) / NUM_CYCLES
    max_jams = max(results)
    min_jams = min(results)

    if CRIT_THRESHOLD is not None:
        crit_results = [x >= CRIT_THRESHOLD for x in results]
        crit_cycles = sum(crit_results)
        crit_streaks = [len(list(c)) for is_crit, c
                        in groupby(crit_results) if is_crit]
        longest_streak = max(crit_streaks) if crit_streaks else 0
    else:
        crit_cycles = None
        longest_streak = None

    return BattleAnalysis(average_jams, max_jams, min_jams, crit_cycles, longest_streak)


def single_cycle(jam_dist):
    active_jam_hits = sum([jam_result(x) for x in list(SCORPION_JAMS + TENGU_JAMS)])

    effective_jams = 0
    for target_id in range(NUM_TARGETS):
        if target_id < active_jam_hits:
            effective_jams += 1
        else:
            lazy_jam_hits = sum([jam_result(x) for x in jam_dist[target_id]])
            if lazy_jam_hits > 0:
                effective_jams += 1

    return effective_jams


def jam_result(jam_strength):
    return random.random() <= jam_strength / TARGET_STRENGTH


def distribute_lazy_jams():
    rand_jams = random.sample(list(DAMNATION_JAMS+KITSUNE_JAMS), len(list(DAMNATION_JAMS+KITSUNE_JAMS)))
    i = 0
    for target_id in range(NUM_TARGETS):
        num_jams = get_num_jams(target_id, len(rand_jams))
        yield rand_jams[i: i + num_jams]
        i += num_jams


def get_num_jams(target_id, jam_num):
    if jam_num == 0:
        return 0
    # Distribute jams as evenly as possible by type with remainder going to
    # "earlier" targets. This does mean that if you have both util and AFK jams,
    # they will disproportionately target the earlier targets.
    return (jam_num // NUM_TARGETS +
            (1 if jam_num % NUM_TARGETS > target_id else 0))


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
