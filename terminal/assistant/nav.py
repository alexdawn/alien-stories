from typing import Iterable, List
from collections import namedtuple, defaultdict
import csv
import math
import random
import sys
import re
from io import TextIOWrapper
from zipfile import ZipFile

import star_system_generator

# work out binaries

PC_TO_LIGHT_YEAR = 0.3066014

AlienSystem = namedtuple('AlienSystem', 
    ['hab_hyg_idx', 'star_name', 'locations', 'affiliation', 'match_mode'
    ])

System = namedtuple('System', 
    ['hab_hyg_idx', 'hip_idx', 'is_hab', 'display_name', 'Hyg_idx', 
     'bf_name', 'gliese_idx', 'bd_idx', 'hd_idx', 'hr_idx', 'proper_name', 
     'spectral_class', 'distance', 'x', 'y', 'z', 'abs_mag'])


# todo generate nearest neighbour paths
# generate seeded systems

def load_starmap():
    systems = {}
    with ZipFile('HabHYG.zip') as zf:
        with zf.open('HabHYG.csv', 'r') as file:
            reader = csv.reader(TextIOWrapper(file, 'iso-8859-1'))
            for i, row in enumerate(reader):
                if i != 0:
                    assert row[0] not in systems.keys()
                    systems[row[0]] = System(*row)
    return systems

def match_with_alien_data():
    systems = defaultdict(list)
    with open('matched.csv', 'rb') as file:
        reader = csv.reader(TextIOWrapper(file, 'utf-8'), )
        for i, row in enumerate(filter(lambda p: len(p) > 0 and '#' not in p[0], reader)):
            if i != 0:
                try:
                    systems[row[0]].append(AlienSystem(*row[:5]))
                except:
                    print(f"Failed on row {i}, with data {row}")
    return systems

def dist_sqr(pos1: Iterable[float], pos2: Iterable[float]) -> float:
    return sum(math.pow(p2 - p1, 2.0) for p1, p2 in zip(pos1, pos2))


def get_distance(pos1: Iterable[float], pos2: Iterable[float]) -> float:
    return math.sqrt(dist_sqr(pos1, pos2))


def make_3d_point(sys: System):
    return (float(sys.x), float(sys.y), float(sys.z))

def dist_between_systems(sys1: System, sys2: System):
    return get_distance(make_3d_point(sys1), make_3d_point(sys2))

def dist_sqr_between_systems(sys1: System, sys2: System):
    return dist_sqr(make_3d_point(sys1), make_3d_point(sys2))

# alien types:
#  'giant',
#  'subgiant'
#         'main sequence'
#         'white dwarf':
#         'red dwarf'
#         'white main sequence'
roman_lookup = {
        '0': 'giant',#'super giant',
        'Ia+': 'giant',#'super giant',
        'Ia': 'giant',#'super giant',
        'Ia': 'giant',#'super giant',
        'Iab': 'giant',#'super giant',
        'Ib': 'giant',#'super giant',
        'II': 'giant',#'bright giant',
        'III': 'giant',#'normal giant',
        'IV': 'subgiant',
        'V': 'main sequence',
        'VI': 'red dwarf', #'sub dwarf',
        'VII': 'white dwarf'
}

def spectra(sys):
    p = re.compile(
        '''(sd|D|d)?([OoBbAaFfGgKkMmWwCcLlTtYy])?[^Iab+V]*(0|Ia\+|Ia|Iab|Ib|II|III|IV|V|VI|VII)?[^Iab+V]*''')
    if sys.spectral_class.strip():
        prefix, colour, lum = p.match(sys.spectral_class).groups()
        if prefix and prefix.lower() == 'sd':
            lum = 'VI'
        if prefix and prefix.lower() == 'd':
            lum = 'VII'
        if not lum:  # maybe default to something dimmer?
            lum = 'VI'
        return roman_lookup.get(lum, lum)
    else:
        return "red dwarf"  # unknown but guess

def get_systems_within(
        current_system_idx: str, systems: List[System], max_distance: float)\
        -> List:
    """get systems in x distance of a given system id"""
    current_system = systems[current_system_idx]
    threshold = math.pow(max_distance, 2)
    data = match_with_alien_data()

    i = 0
    for k, system in sorted(systems.items(), key=lambda x: dist_sqr_between_systems(current_system, x[1])):
        if dist_sqr_between_systems(current_system, system) <= threshold:
            print(k, round(dist_between_systems(current_system, system), 2), *display_system(system, data[k]))
            #print(f"{system.proper_name:>25}{system.display_name:>25}{system.spectral_class:>10}\t{round(float(system.abs_mag), 2):>5}")
            i += 1
    print(f"{i} systems")

def display_system(system: System, extra_data: AlienSystem):
    coords = f'({system.x}, {system.y}, {system.z})'
    return ([s.star_name for s in extra_data] or system.display_name, 
        coords,
        ';'.join(s.locations for s in extra_data),
        ' '.join(set(s.affiliation for s in extra_data)))

if __name__ == '__main__':
    systems = load_starmap()
    data = match_with_alien_data()
    for k, s in systems.items():
        print(k, s.display_name, s.spectral_class, spectra(s), sep='\t')
        if k in data.keys():
            print(display_system(s, data[k]))
        else:
            s = star_system_generator.StarSystem(
                s.display_name, spectra(s), random.choice(['UA', '3WE', 'ICSC', 'UPP']), seed=s.hab_hyg_idx
            )
            s.print_data()
        print()
    # for user_input in sys.stdin:
    #     id, dist = user_input.split(' ')
    #     get_systems_within(id, systems, float(dist))
