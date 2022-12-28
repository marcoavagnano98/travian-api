from custom_session import CustomSession as Cs
from login import Login
from parser import *


class Account:
    def __init__(self, url, credentials):
        self.session = Cs()
        self.parser = ParserController(session=self.session, base_url=url)
        self.credentials = credentials
        self.base_url = url
        self.ids = {}  # id: village_name
        self.coins = {}
        self.villages = {}
        self.login = None
        # steps to access and retrieve fundamental info about villages
        self.account_login()
        self.set_village_ids()
        self.set_account_info()

    def set_account_info(self):
        self.coins = self.get_silver_gold_amount()
        # set other stuffs

    def close_session(self):
        self.session.close_session()

    def account_login(self):
        self.login = Login(url=self.base_url, credentials=self.credentials, session=self.session)
        self.login.login()

    def get_villages_info(self):
        from model import village
        # get info from all villages, with reload time set to 2 secs, it's avoid multiple requests
        coordinates = self.get_coordinates()
        population = self.get_population()
        w_amount = self.get_warehouse_amount()
        g_amount = self.get_granary_amount()
        production = self.get_production()
        troops = self.get_troops()
        for v in self.ids.values():  # foreach village
            self.villages[v] = village.Village(name=v, x=coordinates[v][0], y=coordinates[v][1],
                                               population=population[v], warehouse=w_amount[v],
                                               granary=g_amount[v], production=production[v], troops=troops[v])
        return self.villages

    def get_coordinates(self):
        if self.login.logged_in:
            return self.parser.parse('dorf1.php', Pt.COORDINATES)

    def get_silver_gold_amount(self):
        if self.login.logged_in:
            self.coins = self.parser.parse('dorf1.php', Pt.SILVER_GOLD)
            return self.coins

    def set_village_ids(self):
        if self.login.logged_in:
            self.ids = self.parser.parse('dorf1.php', Pt.IDS)

    def get_population(self):
        if self.login.logged_in:
            population = {}
            for key in self.ids.keys():
                amount = self.parser.parse('dorf1.php?newdid={key}&', Pt.POPULATION)
                population[self.ids[key]] = amount
            return population

    def get_warehouse_amount(self):
        warehouse_amounts = {}
        if self.login.logged_in:
            for key in self.ids.keys():
                amount = self.parser.parse('dorf1.php?newdid={key}&', Pt.WAREHOUSE)
                warehouse_amounts[self.ids[key]] = amount
            return warehouse_amounts

    def get_granary_amount(self):
        granary_amount = {}
        if self.login.logged_in:
            for key in self.ids.keys():
                amount = self.parser.parse('dorf1.php?newdid={key}&', Pt.GRANARY)
                granary_amount[self.ids[key]] = amount
            return granary_amount

    def get_production(self):
        if self.login.logged_in:
            production = {}
            for key in self.ids.keys():
                _production = self.parser.parse('dorf1.php?newdid={key}&', Pt.PRODUCTION)
                production[self.ids[key]] = _production
            return production

    def get_troops(self):
        if self.login.logged_in:
            troops = {}
            for key in self.ids.keys():
                _troops = self.parser.parse(f'dorf1.php?newdid={key}&', Pt.TROOPS)
                troops[self.ids[key]] = _troops
            return troops

    def get_buildings_queue(self):
        if self.login.logged_in:
            buildings = {}
            for key in self.ids.keys():
                _buildings = self.parser.parse(f'dorf1.php?newdid={key}&', Pt.BUILDING_LIST)
                buildings[self.ids[key]] = _buildings
            return buildings

    def get_all_buildings(self, villages = "all", filter="all"):
        if self.login.logged_in:
            buildings = {}
            for key in self.ids.keys():
                _buildings = self.parser.parse(f'dorf2.php?newdid={key}&', Pt.BUILDINGS)
                buildings[self.ids[key]] = _buildings
            return buildings
    def get_movements(self):
        if self.login.logged_in:
            movements ={}
            for key in self.ids.keys():
                _movements = self.parser.parse(f'dorf1.php?newdid={key}&', Pt.MOVEMENTS)
                movements[self.ids[key]] = _movements
            return movements
