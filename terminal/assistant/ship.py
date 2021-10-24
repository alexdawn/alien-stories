from collection import namedtuple


ShipAttributes = namedtuple('ShipAttributes', [
    'crew',
    'passengers',
    'length',
    'ftl_rating',
    'signature',
    'thrusters',
    'hull',
    'armour'
])


class Ship:
    def __init__(name, model, pos):
        self.name = name
        self.model = model
        self.manufacturer = ''

        self.ai = ''  # will have own class
        self.attributes = ()
        self.ship_log = ShipLog()
        self.damage_points = 0
        self.modules = []
        self.lease_cost = None
        self.component_damage = []  # store both minor and major
        self.upgrades = []
        self.armaments = []
        self.pos = pos


class ShipLog:
    def __init__():
        self.records = []

    def add_entry(date, text):
        self.records.append((date, text))
