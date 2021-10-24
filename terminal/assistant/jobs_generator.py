# generate jobs between planets

from enum import Enum
import random
import dice

# todo give jobs a lifetime based on difficulty
# use starmap to find matching target

class Challenge(Enum):
    ROUTINE = 1
    EASY = 2
    NORMAL = 3
    DIFFICULT = 4

class Distance(Enum):
    WITHIN_SYSTEM = 1
    NEARBY = 2
    FARAWAY = 3

jobs = {
    11: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 0, lambda : (20 + dice.roll_d6()) * 1000, 0),
    12: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 0, lambda : (20 + dice.roll_d6()) * 1000, 0),

    13: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (20 + dice.roll_d6()) * 1000, 0),
    14: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (20 + dice.roll_d6()) * 1000, 0),
    15: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (20 + dice.roll_d6()) * 1000, 0),

    16: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (30 + dice.roll_d6()) * 1000, 0),
    21: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (30 + dice.roll_d6()) * 1000, 0),
    22: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (30 + dice.roll_d6()) * 1000, 0),
    23: (Challenge.ROUTINE, Distance.WITHIN_SYSTEM, 1, lambda : (30 + dice.roll_d6()) * 1000, 0),
    
    24: (Challenge.EASY, Distance.WITHIN_SYSTEM, 0, lambda : (20 + dice.roll_2d6()) * 1000, 0),
    25: (Challenge.EASY, Distance.WITHIN_SYSTEM, 0, lambda : (20 + dice.roll_2d6()) * 1000, 0),
    
    26: (Challenge.EASY, Distance.NEARBY, 1, lambda : (20 + dice.roll_2d6()) * 1000, 1),
    31: (Challenge.EASY, Distance.NEARBY, 1, lambda : (20 + dice.roll_2d6()) * 1000, 1),

    32: (Challenge.EASY, Distance.NEARBY, 1, lambda : (25 + dice.roll_2d6()) * 1000, 1),
    33: (Challenge.EASY, Distance.NEARBY, 1, lambda : (25 + dice.roll_2d6()) * 1000, 1),

    34: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    35: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    36: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    41: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    42: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    43: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    44: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),
    45: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 0),

    46: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 1),
    51: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (30 + dice.roll_3d6()) * 1000, 1),

    52: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (40 + dice.roll_3d6()) * 1000, 1),
    53: (Challenge.NORMAL, Distance.NEARBY, 1, lambda : (40 + dice.roll_3d6()) * 1000, 1),

    54: (Challenge.NORMAL, Distance.FARAWAY, 1, lambda : (50 + dice.roll_4d6()) * 1000, 0),

    55: (Challenge.NORMAL, Distance.FARAWAY, 1, lambda : (50 + dice.roll_4d6()) * 1000, 1),

    56: (Challenge.DIFFICULT, Distance.WITHIN_SYSTEM, 2, lambda : (60 + dice.roll_4d6()) * 1000, 1),
    61: (Challenge.DIFFICULT, Distance.WITHIN_SYSTEM, 2, lambda : (60 + dice.roll_4d6()) * 1000, 1),

    62: (Challenge.DIFFICULT, Distance.NEARBY, 2, lambda : (50 + dice.roll_4d6()) * 1000, 0),
    63: (Challenge.DIFFICULT, Distance.NEARBY, 2, lambda : (50 + dice.roll_4d6()) * 1000, 0),

    64: (Challenge.DIFFICULT, Distance.NEARBY, 2, lambda : (50 + dice.roll_4d6()) * 1000, 1),

    65: (Challenge.DIFFICULT, Distance.FARAWAY, 2, lambda : (50 + dice.roll_5d6()) * 1000, 1),

    66: (Challenge.DIFFICULT, Distance.FARAWAY, 3, lambda : (50 + dice.roll_5d6()) * 1000, 2),
}

cargo_employer = [
    ('Colony Representative', 6),
    ('Colonial Administration', 4),
    ('Mining Company', 7),
    ('Major Corporation', 7),
    ('Military Officer', 3),
    ('Shipping Corporation', 3),
    ('Finance Bank', 3),
    ('Wealthy Individual', 3)
]

cargo_rewards = [
    ('Discount Cargo', 3),
    ('Guaranteed Contract', 3),
    ('Monetary Bonus', 18),
    ('Ship Upgrade', 3),
    ('Faction Contract', 3),
    ('Debt cancellation (or credit)', 6)
]

cargo_destination = [
    ('only coordinates', 3),
    ('hostile wilderness', 3),
    ('mine', 6),
    ('spaceport', 3),
    ('asteroid/moon', 3),
    ('space station', 3),
    ('Earth', 3),
    ('Young Colony', 3),
    ('Established Colony', 3),
    ('Starship', 3),
    ('Outpost', 3),
]

cargo = [
    ('Industrial gases', 2),
    ('metals', 2),
    ('colonists', 2),
    ('timbers', 1),
    ('ice/water', 1),
    ('Industrial chemicals', 1),
    ('Fertilizers', 1),
    ('Oils', 2),
    ('Foodstuffs', 2),
    ('Ores', 3),
    ('Medical goods', 1),
    ('Technical parts', 2),
    ('Starship parts', 2),
    ('Spacesuits', 1),
    ('Oversized item', 1),
    ('Vehicles', 1),
    ('Weapons & armour', 2),
    ('Radioactives', 2),
    ('Colony modules', 2),
    ('Animal feed', 1),
    ('Livestock', 2),
    ('Salvage', 1),
]

cargo_complication = [
    ('Embargo/Quarantine', 3),
    ('Intermission', 3),
    ('Military', 6),
    ('Delay', 3),
    ('Maintenance', 6),
    ('Waiting game', 6),
    ('Cargo mishap', 3),
    ('Wreckage', 6),
]

military_reward = [
    ('Faction Contact', 3),
    ('Ship Upgrade', 3),
    ('Monetary Reward', 18),  # bonus or danger pay if employed
    ('New Gear', 3),
    ('New Weapon(s)', 3),
    ('Medals', 6),
]

military_mission = [
    ('recon', 3),
    ('assault', 2),
    ('defence', 2),
    ('combat patrol', 2),
    ('sabotage', 3),
    ('raid', 2),
    ('search and rescue', 3),
    ('peace-keeping', 3),
    ('bug hunt', 4),
    ('civil evacuation', 2),
    ('space assault', 2),
    ('space traffic security', 1),
    ('snatch and grab', 3),
    ('investigation', 4),
]

military_location = [
    ('colony', 9),
    ('outpost', 3),
    ('starship', 2),
    ('spacestation', 2),
    ('wilderness', 2),
    ('war zone', 3),
    ('isolated spaceport', 3),
    ('homesteads', 2),
    ('mine/refinery', 3),
    ('prison complex', 2),
    ('radar/sensor site', 2),
    ('impenetrable area', 3),
]

military_complication = [
    ('role reversal', 2),
    ('passengers', 3),
    ('observer', 1),
    ('company agent', 3),
    ('civilian advisor', 2),
    ('captured', 3),
    ('gear problems', 4),
    ('tough resistance', 4),
    ('trapped', 2),
    ('under fire', 3),
    ('glory hound', 2),
    ('traps', 2),
    ('tactical restrictions', 2),
    ('rookie commander', 2),
]

expedition_sponsor = [
    ('Colonial Administration', 6),
    ('Scientist', 6),
    ('Investors', 6),
    ('Corporatate Rep', 6),
    ('Company Mining Rep', 6),
    ('Government Rep', 6),
]

expedition_reward = [
    ('expedition funds', 3),
    ('ship upgrade', 3),
    ('monetary reward', 18),
    ('mining company contract', 3),
    ('gear', 3),
    ('knowledge', 6),
]

expedition_mission = [
    ('salvage', 6),
    ('survey', 4),
    ('mining', 4),
    ('colony assistance', 4),
    ('prospecting', 5),
    ('data collection', 3),
    ('courier', 3),
    ('anomaly research', 3),
    ('rescue', 4),
]

expedition_target = [
    ('abandoned station', 4),
    ('rogue asteroid', 3),
    ('abandoned mine', 3),
    ('moon', 3),
    ('asteroid belt', 4),
    ('colonized world', 1),
    ('terrestrial planet', 3),
    ('abandoned colony', 1),
    ('ice planet', 3),
    ('spaceship wreckage', 5),  # roll again
    ('comet', 3),
]

expedition_complication = [
    ('natural', 7),
    ('survey blues', 7),
    ('missing expedition', 3),
    ('rival expedition', 5),
    ('quarantine', 4),
    ('deadly treasure', 6),
    ('surveillance', 4),
]

job_twist = [
    ('mayday call', 5),
    ('bad intel', 3),
    ('sabotage', 3),
    ('secret plot', 6),
    ('murder', 4),
    ('solar flare', 3),
    ('malfunction', 5),
    ('time limit', 5),
    ('alien outbreak', 2),
]

def weighted_select(table, number=1):
    if number == 0:
        return None
    result = random.choices([t[0] for t in table], weights=[t[1] for t in table], k=number)
    if number == 1:
        return result[0]
    else:
        return result

def make_cargo_job():
    difficulty, distance, number_of_complications, payment_gen, number_of_rewards = jobs[dice.roll_d6() + 10 * dice.roll_d6()]
    payment = payment_gen()
    employer = weighted_select(cargo_employer)
    reward = weighted_select(cargo_rewards, number_of_rewards)
    destination = weighted_select(cargo_destination)
    goods = weighted_select(cargo)
    complication = weighted_select(cargo_complication, number_of_complications)
    twist = weighted_select(job_twist)
    print(f"""{difficulty.name} job {distance.name} ${payment:,}{' with '+ str(reward) if reward else ''}
    {employer} wants to transport {goods} to {destination}
    complication: {complication} twist: {twist}""")


def make_military_job(is_merc: False):
    difficulty, distance, number_of_complications, payment_gen, number_of_rewards = jobs[dice.roll_d6() + 10 * dice.roll_d6()]
    payment = payment_gen()
    if is_merc:
        employer = weighted_select(cargo_employer)
    else:
        employer = 'USMC'
    reward = weighted_select(military_reward, number_of_rewards)
    destination = weighted_select(military_location)
    mission = weighted_select(military_mission)
    complication = weighted_select(military_complication, number_of_complications)
    twist = weighted_select(job_twist)
    print(f"""{difficulty.name} job {distance.name} ${payment:,}{' with '+ str(reward) if reward else ''}
    {employer} wants {mission} mission at {destination}
    complication: {complication} twist: {twist}""")


def make_expedition_job():
    difficulty, distance, number_of_complications, payment_gen, number_of_rewards = jobs[dice.roll_d6() + 10 * dice.roll_d6()]
    payment = payment_gen()
    employer = weighted_select(expedition_sponsor)
    reward = weighted_select(expedition_reward, number_of_rewards)
    destination = weighted_select(expedition_target)
    mission = weighted_select(expedition_mission)
    complication = weighted_select(expedition_complication, number_of_complications)
    twist = weighted_select(job_twist)
    print(f"""{difficulty.name} job {distance.name} ${payment:,}{' with '+ str(reward) if reward else ''}
    {employer} wants a crew for a {mission} mission at a {destination}
    complication: {complication} twist: {twist}""")

if __name__ == '__main__':
    for i in range(5):
        make_expedition_job()
