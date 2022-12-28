class Village:
    def __init__(self, name, x, y, population, warehouse, granary, production, troops):
        self.x = x
        self.y = y
        self.name = name
        self.population = population
        self.warehouse = warehouse
        self.granary = granary
        self.troops = troops
        self.production = production
        self.fields = {}


class Building:
    def __init__(self, name, level, gid, id):
        self.name = name
        self.level = level
        # params to send post request
        self.gid = gid
        self.id = id
