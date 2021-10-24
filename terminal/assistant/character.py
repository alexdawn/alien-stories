from collection import namedtuple

from dice import roll_d6

Name = namedtuple('Name', [
    'title',
    'first_name',
    'surname'
])

CharacterAttributes = namedtuple('CharacterAttributes', [
    'strength',
    'wits',
    'empathy',
    'agility'
])

CharacterSkills = namedtuple('CharacterSkills', [
    'heavy_machinery',
    'close_combat',
    'stamina',
    'observation',
    'survial',
    'comtech',
    'medical_aid',
    'manipulation',
    'command',
    'piloting',
    'mobility',
    'ranged_combat'
])

# abstract subclass humans an androids
class Character:
    def __init__(**kwargs):
        self.career = kwargs.get('career')
        self.name = kwargs.get('name', self.generate_name())
        self.appearance = kwargs.get('appearance', self.generate_appearance())
        self.personal_agenda = kwargs.get('personal_agenda', self.generate_agenda())

        self.buddy = kwargs.get('buddy', None)
        self.rival = kwargs.get('rival', None)

        self.attributes = CharacterAttributes(3, 3, 3, 3) # total 14, between 2-4 (5 for key attr)
        self.skills = CharacterSkills(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)  # total 10 up to 3 for career talents (1 otherwise)
        self.talents = kwargs.get('talents', self.generate_talent())
        self.exp = 0
        self.story_points = 0  # max 3

        self.items = kwargs.get('items', self.generate_items())  # gear, weapons and tiny items 
        self.signature_item = kwargs.get('signature_item', self.generate_signature())
        self.stress = 0
        self.radiation = 0
        self.critical_injuries = []
        self.conditions = []  # starving, dehydration, exhaustion, freezing
        self.consumables = {
            'air': 0,
            'food': 0,
            'water': 0
        }
        self.encumbrance = 0
        self.armour = 0

    def generate_name(self) -> None:
        self.name = Name('', 'Foo', 'Bar')

    def generate_cash(self) -> None:
        self.cash = 600

    def advance_time(self, amount: int, type: str):
        if type == 'turn':
            if self.is_safe:
                self.stress -= 1
        elif type == 'shift':
            if self.is_safe:
                self.stress -= 6
        elif type == 'day':
            if self.is_safe:
                self.stress -= 24

    def death_test(self):
        if self.skill_test('stamina'):
            pass
        else:
            pass # dead

    def _roll(self, standard: int, stress: int) -> Tuple[List[str], List[str]]:
        return (
            random.choices(['fail', 'pass'], weights = [5, 1], k = standard), 
            random.choices(['panic','fail', 'pass'], weights = [1, 4, 1], k = stress)
        )

    def attribute_test(self, attribute: str) -> int:
        return any(r == 'pass' for r, _ in _roll(getattr(self.attribute, attribute), 0))

    def skill_test(self, skill: str, gm_mod: int=0) -> int:
        result = _roll(getattr(self.skill, skill) + gm_mod, self.stress)
        if any(r == 'panic' for r in result[1]):
            panic_result = self.panic()
        if not panic_result:
            return sum(r == 'pass' for r in result[0]) + sum(r == 'pass' for r in result[1])
        else:
            return 0

    def take_damage(self, amount: int) -> None:
        armour_saves = sum(random.choices([0, 1], [5, 1], k=self.armour))
        print(f"armour saves {armour_saves} points of damage")
        mitigated_amount = amount - armour_saves
        if mitigated_amount > 0:
            print(f"{self.name} takes {mitigated_amount} points of damage")
            self.stress += 1
            self.health = max(self.health - amount, 0)
            if self.health == 0:
                self.broken = True

    def recover(self):
        self.health = 1

    def panic(self) -> None:
        def twitch():
            self.stress += 1
        def tremble():
            self.attributes = self.attributes._replace('agility', self.attributes.agility - 2)
        def drop_item():
            pass
        def run_away():
            pass
        def freeze():
            pass
        def berzerk():
            pass
        def catatonic():
            pass
        outcomes = {
            7: 'twitch',
            8: 'tremble',
            9: 'drop item',
            10: 'something',
            11: 'run away',
            12: 'freeze',
            13: 'berzerk',
            14: 'catatonic'
        }
        result = self.stress + dice.roll_d6()
        res = outcome.get(result, outcome[14]) if result >= 7 else 'fine'
        return result < 10

    def consume_air(self) -> None:
        if consumables['air'] >= 1: 
            consumables['air'] -= 1
        else:
            self.status.append('affix')

    def consume_water(self) -> None:
        if consumables['water'] >= 1:
            consumables['water'] -= 1
        else:
            self.status.append('thirst')

    def consume_food(self) -> None:
        if consumables['food'] >= 1:
            consumables['food'] -= 1
        else:
            self.status.append('starving')

    def equip(self, item: Item) -> None:
        item.equip(self)
        self.encumbrance += item.weight
        self.items.append(item)

    def drop(self, item: Item) -> None:
        item.drop(self)
        self.encumbrance -= item.weight
        self.items.remove(item)

class Android(Character):
    def __init__(self):
        pass

class Item:
    def __init__(self, weight):
        self.weight = weight
        self.power = 0

    def consume_power(self):
        pass

class TinyItem(Item):
    def __init__(self):
        self.weight = 0

class Weapon(Item):
    def __init__(self):
        pass
