import random
import itertools
from operator import attrgetter
import dice

with open("names.txt") as file:
    names = [line.strip() for line in file if line[0] != '#' and line.strip() != '']

class StarSystem:
    def __init__(self, name: str, star_type: str, location: str, seed=0, star_colour: str = None):
        self.name = name
        random.seed(seed)
        self.star = Star(star_type, star_colour)
        self.location = location
        self.gas_giants = self.generate_gas_giants()
        self.asteroid_belts = self.generate_asteroid_belts()
        self.planets = self.generate_planets()
        self.ice_planets = self.generate_ice_planets()
        self.pick_colony_location(location)

    def print_data(self, only_colonies=True):
        self.star.print_data()
        if only_colonies:
            print(f"{len(self.planets)} planets")
            for p in self.planets:
                if len(p.colonies) > 0:
                    p.print_data()
            print(f"{len(self.gas_giants)} gas giants")
            for p in self.gas_giants:
                for m in p[1]:
                    if len(m.colonies) > 0:
                        m.print_data(True)
        else:
            print("Inner planets:")
            for p in self.planets:
                p.print_data()
            for p in self.asteroid_belts:
                print("Asteroid belt: ", p)
            for p in self.gas_giants:
                print("Gas giant: ", p[0])
                for m in p[1]:
                    m.print_data(True)
            # print("Ice planets:")  ## not very interesting
            # for p in self.ice_planets:
            #     p.print_data()

    def pick_colony_location(self, location):
        """Uses the hab score to pick the best location for the colony"""
        planetoids = [m for p in self.gas_giants for m in p[1]] + self.planets + self.ice_planets
        best = max(planetoids, key=attrgetter('habitability_rating'))
        best.generate_colony(location)


    def generate_gas_giants(self):
        giants = (
            'storms',
            'single super storm',
            'rings',
            'high winds',
            'intense radiation fields',
            'small for a gas giant'
        )
        count = dice.roll_d6() - 1 - (self.star.type == 'subgiant') - (4 * self.star.type == 'white dwarf')
        common_temp = dice.roll_2d6()
        return [
            (
                random.choice(giants),
                # rolls for a common base temperature for all moons
                [Planetoid(False, True, self.location, common_roll=common_temp) for x in range(dice.roll_d6() + 1)]
            )
            for x in range(max(count, 0))
        ]

    def generate_asteroid_belts(self):
        asteroids = (
            'bright and highly visible',
            'high orbital inclination',
            'dust belt',
            'contains several large dwarf planets',
            'very wide - covers several orbits',
            'intensely mineral rich asteroids'
        )
        count = dice.roll_d6() - 3 - (2 * self.star.type in ('white dwarf', 'subgiant'))
        return [random.choice(asteroids) for x in range(max(count, 0))]

    def generate_planets(self):
        count = dice.roll_d6() - (3 * self.star.type in ('white dwarf', 'red dwarf', 'giant', 'subgiant'))  # giants not in CRB
        return [Planetoid(False, False, self.location) for x in range(dice.roll_d6())]

    def generate_ice_planets(self):
        count = dice.roll_d6() + 1 - (self.star.type in ('white main sequence', 'giant', 'subgiant'))
        return [Planetoid(True, False, self.location) for x in range(count)]

class Star:
    types = {
        'giant': ('huge bright and cool star in late life', 'Type III'),
        'subgiant': ('a large bright star exhausting it\'s fuel', 'Type IV'),
        'main sequence': ('a small but common star', 'Type V'),
        'white dwarf': ('a dead burnt out star, small and super dense', 'Type DA'),
        'red dwarf': ('a red main sequence star, small and cool, very common', 'Type MV'),
        'white main sequence': ('white main sequence stars that burn hot and bright', 'Type AOV')
    }
    spectral_classes = {
        'O': 'Blue',
        'B': 'Blue',
        'A': 'White',
        'F': 'Yellow-White',
        'G': 'Yellow',
        'K': 'Orange',
        'M': 'Red'
    }
    # % probability for M stars
    spectral_ratio = {
        'O': 0.00003,
        'B': 0.13,
        'A': 0.6,
        'F': 3,
        'G': 7.6,
        'K': 12.1,
        'M': 76.45,
    }
    roman_lookup = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IV': 4,
        'V': 5,
        'VI': 6,
        'VII': 7

    }

    def extract_from_string(self, text):
        regex = '.*([OBAFGKM][0-9])([IV]{1,3}).*'

    def __init__(self, star_type, spectral_class=None):
        assert star_type in Star.types.keys()
        self.type = star_type
        # self.brightness = brightness
        if spectral_class:
            self.spectral_class = spectral_class
        else:  # elif star_type == 'main sequence':
            self.spectral_class = random.choices(list(Star.spectral_ratio.keys()), weights=list(Star.spectral_ratio.values()))[0]

    def print_data(self):
        print("type:", self.type)
        print("colour:", self.spectral_class)

class Planetoid:
    def __init__(self, is_ice: bool, is_moon: bool, location: str, common_roll=None):
        self.is_ice = is_ice
        self.is_moon = is_moon
        self.generate_name(False)
        self.generate_size()
        self.generate_atmosphere()
        self.generate_temperature(common_roll)
        self.generate_geosphere()
        self.generate_terrain()
        self.estimate_habitability()
        self.colonies = []
        self.moons = 0 if self.is_moon else dice.roll_d3() - 1
        self.colony_mission = None

    def estimate_habitability(self):
        """Heuristic for placing the colony on the best world"""
        gravs = {
            '~0G': 0,
            '0.1G': 0.1,
            '0.2G': 0.2,
            '0.5G': 0.5,
            '0.7G': 0.7,
            '1.0G': 1.0,
            '1.3G': 0.7,
            '2G': 0.2
        }
        airs = {
            'none': 0.1,
            'thin': 0.5,
            'breathable': 1.0,
            'toxic': 0.2,
            'dense': 0.5,
            'corrosive': 0.1,
            'infiltrating': 0.1,
            'special': 0.8
        }
        temps = {
            'frozen': 0.5,
            'cold': 0.8,
            'temperate': 1.0,
            'hot': 0.8,
            'burning': 0.1
        }
        water = {
            'desert': 0.1,
            'arid': 0.5,
            'temperate dry': 0.8,
            'temperate wet': 1.0,
            'wet': 0.8,
            'water': 0.3
        }
        self.habitability_rating = gravs[self.size[1]] * airs[self.atmosphere] * temps[self.temperature[0]] * water[self.geosphere[0]]


    def generate_colony(self, location):
        self.has_colony = True
        self.generate_name(True)
        self.colonies.append(Colony(self, location))
        if dice.roll_2d6() == 10:
            self.colonies.append(Colony(self, location))
        
    def generate_name(self, inhabited: bool):
        prefixes = ['LV', 'MT', 'RF']
        if inhabited:
            if self.name:
                self.former_name = self.name
            self.name = random.choice(names)
        else:
            self.name = f'{random.choice(prefixes)}-{random.randint(1, 1000):3>0}'

    def generate_size(self):
        sizes = (
            # size_km surface_gravity example
            (1000, '~0G', 'Asteroid'),
            (2000, '0.1G', 'Iapetus'),
            (2000, '0.1G', 'Iapetus'),
            (4000, '0.2G', 'Luna, Europa'),
            (4000, '0.2G', 'Luna, Europa'),
            (7000, '0.5G', 'Mars'),
            (10000, '0.7G', ''),
            (12500, '1.0G', 'Earth, Venus'),
            (12500, '1.0G', 'Earth, Venus'),
            (15000, '1.3G', ''),
            (20000, '2G', 'Super Earths'),
        )
        die_result = dice.roll_2d6() - (2 * self.is_ice) - (4 * self.is_moon) - 2
        if die_result > 0:
            self.size = sizes[die_result]
        else:
            self.size = sizes[0]

    def generate_atmosphere(self):
        airs = [
            'thin',
            'thin',
            'breathable',
            'breathable',
            'breathable',
            'toxic',
            'toxic',
            'toxic',
            'dense',
            'corrosive',
            'infiltrating',
            'special'
        ]
        assert len(airs) == 12
        die_result = dice.roll_2d6() - 2
        if self.size[0] <= 4000:
            die_result -= 8  # tweaked
        elif self.size[0] <= 7000:
            die_result -= 4  # tweaked
        elif self.size[0] >= 15000:
            die_result += 4  # tweaked
        if die_result > 0:
            self.atmosphere = airs[min(die_result, 11)]
        else:
            self.atmosphere = 'none'  # tweaked

    def generate_temperature(self, common_roll=None):
        temps = (
            ('frozen', '< -50C', 'Titan, Pluto, Enceladus'),
            ('frozen', '< -50C', 'Titan, Pluto, Enceladus'),
            ('cold', '-50-0C', 'Antarctica'),
            ('cold', '-50-0C', 'Alaska'),
            ('temperate', '0-30C', 'Boston'),
            ('temperate', '0-30C', 'Paris'),
            ('hot', '31-80C', 'Mojave'),
            ('hot', '31-80C', 'Sahara'),
            ('hot', '31-80C', 'Sahara'),
            ('burning', '80C+', 'Mercury'),
            ('burning', '80C+', 'Venus')
        )
        if not common_roll:
            die_result = dice.roll_2d6()
        else:
            die_result = common_roll
        if self.atmosphere == 'thin':
            die_result -= 4
        elif self.atmosphere == 'dense':
            die_result += 1
        elif self.atmosphere in ('corrosive', 'dense'):
            die_result += 6
        if self.is_ice:
            self.temperature = temps[0]
        else:
            self.temperature = temps[max(min(die_result, 12), 2) - 2]

    def generate_geosphere(self):
        water_content = (
            ('desert', 'no water'),
            ('desert', 'no water'),
            ('desert', 'no water'),
            ('arid', 'desert and dry steppes with some lakes'),
            ('arid', 'desert and dry steppes with some lakes and small seas'),
            ('temperate dry', 'Ocean cover 30%'),
            ('temperate dry', 'Ocean cover 40%'),
            ('temperate wet', 'Ocean cover 60%'),
            ('temperate wet', 'Ocean cover 70%'),
            ('wet', 'global ocean with some islands and archipelagos'),
            ('water', 'No dry land'),
        )
        die_result = dice.roll_2d6()
        if self.atmosphere in ('thin', 'corrosive', 'infiltrating'):  # CRB has 'dense'
            die_result -= 4
        elif self.atmosphere == 'dense':
            die_result += 2  # tweaked
        elif self.temperature[0] == 'hot':
            die_result -= 2
        elif self.temperature[0] == 'burning':
            die_result -= 2
        elif self.temperature[0] == 'frozen':
            die_result -= 2
        if self.atmosphere == 'none':
            self.geosphere = water_content[0]
        else:
            self.geosphere = water_content[max(min(die_result, 12), 2) - 2]

    def generate_terrain(self):
        if self.is_ice:
            terrains = [
                'huge impact craters',
                'geysers spew water into low orbit from long fissures',
                'deep fissures leading to a subsurface ocean',
                'dramatically coloured blue-green ice fissures',
                'huge and active cyro-volcano',
                'vast range of ice mountains',
                'world-spanning super canyon',
                'disturbing, wind-cut ice formations',
                'black, dust-covered ice plains',
                'impressive ice escarpment of great length',
                'extensive dune-fields of methane sand grains'
            ]
            selection = dice.roll_2d6()
            self.terrain = terrains[selection - 2]
        else:
            # todo sense check weather, water and flora makes sense
            terrains = [
                'huge impact craters',  #requires little air/water
                'plains of silicon glass',  #requires land
                'disturbing wind-cut rock formations',  # requires air/land
                'permanent global dust-storm',  # requires air/land
                'eerily coloured dust plains',  # requires land
                'active volcanic lava fields',  # requires large enough planet or tidal forces
                'extensive salt flats',  # requires land
                'dust-laden, permanent sunset sky',  # requires air, tidal lock
                'ancient, blackend lava plains',  # requires large enough planet or tidal forces
                'thermal springs and steam vents',  # requires large enough planet or tidal forces
                'tall, gravel-strewn mountains',  # large enough for some tectonics
                'howling winds that never stop',  # requires air
                'daily fog banks roll in',  # requires air and water
                'deep and wide rift valley',  # requires tectonics
                'bizarrley eroded, wind-cut badlands',  # requires air
                'steep-sided river gorges cut into soft rocks',  # requires water
                'huge moon dominates day/night sky',  # requires/adds moon
                'world-spanning super canyon',  # requires land
                'impressive river of great length',  # requires water and land
                'oddly coloured forests of (alien) vegetation',  # requires water and land
                'mountains cut by sky blue lakes',  # requires tectonics/water
                'sweeping plains of elephant grass',  #requires water and land
                'highly toxic, but beautiful plant life', #requires water and land
                'small, bright, incredibly fast/close moons in orbit', # requires/adds moon
                'vast and complex river delta', #requires water and land
                'immense series of waterfalls', #requires water and land
                'endless mudflats with twisting water-ways', #requires water and land
                'impressive coastline of fjords and cliffs', #requires water and land
                'volcanoes, active & widespread',  # requires tectonics
                'impenetrable jungle', #requires water and land
                'dangerous tides-fast & loud', #requires water and land
                'vast, permanent super storm', #requires air
                'toxic sea creatures floating with the currents', #requires water
                'volcanic island chains',  #requires water, tectonics
                'permanently overcast with unrelenting rainfall', #requires water, heat
                'mildly acidic oceans and rainfall' #requires water, air
            ]
            selection = random.randint(0, len(terrains))
            if self.geosphere[0] == 'desert':
                selection -= 3 * 6
            elif self.geosphere[0] == 'arid':
                selection -= 2 * 6
            elif self.geosphere[0] == 'wet':
                selection += 2 * 6
            elif self.geosphere[0] == 'water':
                selection += 3 * 6
            if self.temperature[0] == 'frozen':
                selection -= 2 * 6
            self.terrain = terrains[max(min(selection, len(terrains) - 1), 0)]

    def print_data(self, indent=False):
        print('\t' if indent else '', f'{"moon" if self.is_moon else "planet"} {self.name}')
        print('\t\t' if indent else '\t', self.size[1], self.atmosphere, self.temperature[0], self.geosphere[0], sep='\t')
        print('\t\t' if indent else '\t', self.terrain, sep='\t')
        for colony in self.colonies:
            colony.print_data(indent)
            print()


class Colony():
    def __init__(self, planet, location):
        # todo add name for colony
        self.planet = planet
        self.generate_colony_size()
        self.generate_colony_mission()
        self.generate_orbital_objects()  # need to append to list if two colonies?
        self.generate_colony_factions()
        self.generate_allegiance(location)
        self.generate_event()

    def print_data(self, indent):
        print('\t\t' if indent else '\t', self.allegiance, self.colony, self.colony_mission, self.factions, sep='\t')
        print('\t\t' if indent else '\t', self.event, sep='\t')
        print('\t\t' if indent else '\t', self.planet.orbital_objects, sep='\t')

    def generate_colony_size(self):
        small = ('start up', lambda : dice.roll_3d6() * 10, lambda : min(dice.roll_d3() - 1, 1))
        medium = ('young', lambda : dice.roll_3d6() * 100, lambda : dice.roll_d3() - 1)
        large = ('established', lambda : dice.roll_2d6() * 1000, lambda : dice.roll_d3())
        size = (
            small,
            small,
            small,
            small,
            small,
            small,
            medium,
            medium,
            medium,
            large,
            large
        )
        die_result = dice.roll_2d6()
        if self.planet.atmosphere == 'breathable':
            die_result += 1
        elif self.planet.atmosphere in ('corrosive', 'infiltrating'):
            die_result -= 2
        if self.planet.size[0] <= 4000:
            die_result -= 3
        result = size[max(min(die_result, 12), 2) - 2]
        self.colony = (result[0], result[1](), result[2]())

    def generate_colony_mission(self):
        # todo sense check misison
        mission = (
            'terraforming',  # can't be too habitable
            'research',
            'survey and prospecting',
            'prison / secluded or exile',
            'mining and refining',
            'mineral drilling',
            'communications relay',
            'military',
            'cattle ranching / logging',  #requires water and land
            'corporate HQ',
            'government HQ'
        )
        die_result = dice.roll_2d6()
        if self.planet.atmosphere == 'breathable':
            die_result += 1
        elif self.planet.atmosphere in ('toxic', 'corrosive', 'infiltrating'):
            die_result -= 6
        if self.colony[0] == 'start up':
            die_result -= 1
        elif self.colony[0] == 'established':
            die_result += 4
        self.colony_mission = mission[max(min(die_result, 12), 2) - 2]

    def generate_orbital_objects(self):
        self.planet.orbital_objects = self._generate_orbital_objects(True)

    def _generate_orbital_objects(self, allow_twelve):
        # max value 8 for uninhabited planets
        # todo moon results to modify score, also only for planets
        objects = (
            'little (wreckage or nothing)',
            'little (wreckage or nothing)',
            'little (wreckage or nothing)',
            'ring',  # not for moons
            'abandoned or repurposed satellite or space station',
            f'{dice.roll_d3()} Moons',  # not for moons
            f'{dice.roll_d3()} Moons',  # not for moons
            'survey station',
            'survey station and communication satellites',
            'transfer station',
            [self._generate_orbital_objects(False) for x in range(dice.roll_d6())] if allow_twelve else ''
        )
        die_result = dice.roll_2d6()
        if self.colony[0] == 'young':
            die_result += 1
        elif self.colony[0] == 'established':
            die_result += 2
        return objects[max(min(die_result, 12), 2) - 2]

    def generate_colony_factions(self):
        factions = [
            'newcomers',
            'corporate',  # corporate representatives
            'scientists',
            'workers',
            random.choice(['security', 'military']),
            'administration'  # colonial leadership
        ]
        make_faction = lambda x: random.choices(factions, k=x)
        r = dice.roll_d6()
        balance = [
            ('one dominant {} faction'.format(*make_faction(1))),
            ('two balanced {} and {} factions'.format(*make_faction(2))),
            ('two competing {} and {} factions'.format(*make_faction(2))),
            ('one dominant {} faction, one weak {} faction'.format(*make_faction(2))),
            ('three competing {}, {} and {} factions'.format(*make_faction(3))),
            ('total mess {} with strengths {}'.format(make_faction(r), [dice.roll_d6() for x in range(r)])),
        ]
        self.factions = balance[dice.roll_d6() - 1]

    def generate_allegiance(self, location):
        # todo multi colonies with rival powers
        if location == 'ICSC':
            orgs = [
                'Kelland Mining',
                'Kelland Mining',
                'GeoFund investor',
                'Seegson',
                'Independent',
                'Jingti Long Corporation',
                'Jingti Long Corporation',
                'Jingti Long Corporation',
                'Chigusa Corporation',
                'Lasalle Bionational',
                'Seegson',
                'Lorenz SysTech',
                'Gemini Exoplanet',
                'Farside Mining',
                'Farside Mining'
            ]
        elif location in ('3WE', 'UA'):
            orgs = [
                'Kelland Mining',
                'Kelland Mining',
                'Gustafsson Enterprise',
                'Lasalle Bionational',
                'Weyland-Yutani',
                'Goverment Rep',
                'Goverment Rep',
                'Goverment Rep',
                'Weyland-Yutani',
                'Seegson',
                'Jingti Long Corporation',
                'Chigusa Corporation',
                'Gemini Exoplanet',
                'Farside Mining',
                'Farside Mining'
            ]
        if location == 'UPP':
            self.allegiance ='UPP'
        else:
            self.allegiance = orgs[dice.roll_3d6() - 3]

    def generate_event(self):
        events = [
            'Pilfering and thefts force security to search rooms and lockers.',
            'Incidents of Sabotage are increasing; security suspects organised crime.',
            'Colonial administration is investigating the colony for ilegal practices',
            'Colonists returning to base report seeing a monster on the surface.',
            'Petty crime, theft and sabotage are rife.',
            'Equipment failure has resulting in rationing at the colony, tempers are frayed.',
            'Ship recently arrived with some kind of parasite that will soon spread through the colony',
            'Stolen goods are on offer-cheap!',
            'Unknown to you and old friend/flame is at the colony.',
            'Unknown to you an old enemy/rival is at the colony.',
            'A minor dignitary/notable is visting in company of several aides or guards.',
            'Part of the colony is off-limits temporarily- no reason given.',
            'Sudden restriction on free movement, unless you can find a way to avoid it.',
            'An emergency means repairs and vital supplies are being shipped in from a nearby colony.',
            'Local crisis about to hit (storm, earthquake, riot, fire etc.)',
            'Period of solar flare-will cut communications for one shift (D6 days if star type MV).',
            'Spies from a neighbouring colony have been discovered and arrested.',
            'Operations manager and his/her deputy are in conflict; everyone is choosing sides.',
            'PCs are invited to a formal dinner, meeting or party',
            'The local colonists are not what they seem.',
            'A military ship is in orbit and the landing party is searching for someone/something.',
            'A rival colony or coporation is about to carry out an act of sabotage.',
            'The spaceport is currently quarantined.',
            'Security situation at the colony.',
            'A bunch of asteroid miners causing trouble while on leave.',
            'Mystery ship arrives at the spaceport.',
            'Civil unrest is about to break out.',
            'Colonists are trapped and need rescuing far from the settlement itself.',
            'Authorities have just locked down the colony after a riot.',
            'A religious leader is whipping up discontent.',
            'PCs will be harassed by angry locals. Why the anger? And why directed at off-worlders?',
            'An expedition is being assembled for a trek overland- the PCs are invited.',
            'An important colonial official is murdered, only an hour after you arrive.',
            'Several colonists have gone missing- a search is underway.',
            'A lifeboat has crashed on planet and contains an interesting individual.',
            'The corporation or government paying for the colony keeps ordering teams out to search remote areas- but won\'t way what they are searching for.'
        ]
        self.event = random.choice(events)


if __name__ == '__main__':
    s = StarSystem('main sequence', 'ICSC')
    s.print_data()
        
