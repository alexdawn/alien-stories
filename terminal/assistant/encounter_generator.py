import dice

encounter_freq = {
    'habitable world': '1 per day',
    'outer system': '1 per week',
    'unexplored systems': '1 per month'
}

def ship_encounter(location):
    ship_type = {
        11: 'research vessel',
        12: 'asteroid mining ship',
        13: 'small survey ship',
        14: 'small colony supply vessel',
        15: 'military recon craft',
        16: 'private executive transport',
        21: 'hypersleep transport',
        22: 'light shuttle',
        23: 'bulk freighter',
        24: 'liquefied gas transport',
        25: 'tugship towing a platform',
        26: 'bulk freighter',
        31: 'container ship',
        32: 'colony supply vessel',
        33: 'petroleum carrier',
        34: 'salvage ship',
        35: 'military patrol craft',
        36: 'emergency response vessel',
        41: 'military missile cruiser',
        42: 'tugship not towing',
        43: 'heavy shuttle',
        44: 'fast courier vessel',
        45: 'modular cargo transport',
        46: 'large space-station',
        51: 'light tugship',
        52: 'in-system shuttle',
        53: 'container ship',
        54: 'communication relay station',
        55: 'military dropship in orbit',
        56: 'in-system shuttle',
        61: 'customs cutter',
        62: 'military assault ship',
        63: 'in-system shuttle',
        64: 'corporate space station',
        65: 'private security cutter',
        66: 'mobile construction rig'
    }
    reaction = {
        2: 'unusual',
        3: 'dismissive',
        4: 'dismissive',
        5: 'radio-silence, polite',
        6: 'radio-silence, polite',
        7: 'radio-silence, polite',
        8: 'radio-silence, polite',
        9: 'friendly',
        10: 'friendly',
        11: 'assistance',
        12: 'familiar'
    }
    result10, result1 = dice.roll_d6(), dice.roll_d6()
    if location in ('outer-rim', 'frontier'):
        result10 -= 3
    elif location == 'uncharted':
        result10 -= 5
    ship = ship_type.get(result10 * 10 + result1, None)
    react = reaction[dice.roll_2d6()] if ship else None
    print(ship, react)


def planet_encounter(is_colonised):
    # daily encounter
    encouter = {
        3: 'temperature swing',
        4: 'temperature swing',
        5: 'temperature swing',
        6: 'unstable ground',
        7: 'unstable ground',
        8: 'diversion',
        9: 'cross ravine/river',
        10: 'rough terrain',
        11 : 'nothing',
        12: 'wildcatters',
        13: 'mining operation',
        14: 'lone colonist',
        15: 'scientists',
        16: 'abandoned kit',
        17: 'explorers',
        18: 'explorers'
    }
    result = dice.roll_3d6() 
    result = result if is_colonised else min(11, result)
    return encounter[result]

def colony_encounter(is_established):
    pass

if __name__ == '__main__':
    for i in range(10):
        ship_encounter('frontier')
