import re
from . import *


class Dorf1:
    def __init__(self):
        self.html_parser = None

    def parse(self, html_parser, _type):
        self.html_parser = html_parser
        if _type is Pt.SILVER_GOLD:
            return self.get_silver_gold_amount()
        if _type is Pt.WAREHOUSE:
            return self.get_warehouse_amount()
        if _type is Pt.GRANARY:
            return self.get_granary_amount()
        if _type is Pt.IDS:
            return self.get_village_ids_name()
        if _type is Pt.PRODUCTION:
            return self.get_production()
        if _type is Pt.TROOPS:
            return self.get_troops()
        if _type is Pt.POPULATION:
            return self.get_population()
        if _type is Pt.COORDINATES:
            return self.get_coordinates()

    def get_silver_gold_amount(self):
        gold_text = self.clean(self.html_parser.find('div', {'class': 'ajaxReplaceableGoldAmount'}).text, True)
        silver_text = self.clean(self.html_parser.find('div', {'class': 'ajaxReplaceableSilverAmount'}).text, True)

        return {'gold': int(gold_text), 'silver': int(silver_text)}

    def get_warehouse_amount(self):
        amount = self.html_parser.find('div', {'class': 'warehouse'}) \
            .find('div', {'class', 'capacity'}) \
            .find('div', {'class', 'value'}).text
        return int(self.clean(amount, True))

    def get_population(self):
        amount = self.clean(self.html_parser.find('div', {'class': 'population'}).find('span').text, True)
        return int(amount)

    def get_granary_amount(self):
        amount = self.html_parser.find('div', {'class': 'granary'}) \
            .find('div', {'class', 'capacity'}) \
            .find('div', {'class', 'value'}).text
        return int(self.clean(amount, True))

    def get_production(self):
        production = {}
        lines = self.html_parser.find('table', {'id': 'production'}).find('tbody').find_all('tr')
        for line in lines:
            res = line.find("td", {"class", "res"}).text.strip().replace(':', '')
            num = self.clean(line.find("td", {"class", "num"}).text)
            production[res] = int(num)
        return production

    def get_troops(self):
        troops = {}
        lines = self.html_parser.find('table', {'id': 'troops'}).find('tbody').find_all('tr')
        for line in lines:
            unit = line.find("td", {"class", "un"}).text
            num = self.clean(line.find("td", {"class", "num"}).text)
            troops[unit] = int(num)
        return troops

    def get_villages_tags(self):
        lists = self.html_parser.find('div', {'class': 'villageList'})
        return lists.find_all('div', {'class': 'listEntry'})

    def get_village_ids_name(self):
        ids = {}
        for tag in self.get_villages_tags():
            html_text = tag.text
            info = self.clean(re.sub(re.compile(r'\s+'), ' ', html_text)).split(' ')[0]
            ids[tag.attrs['data-did']] = info
        return ids

    def get_coordinates(self):
        villages = {}
        for tag in self.get_villages_tags():
            html_text = tag.text
            info = self.clean(re.sub(re.compile(r'\s+'), ' ', html_text)).split(' ')
            x, y = re.sub('[()]', '', info[1]).split('|')
            villages[info[0]] = (x, y)
        return villages

    def clean(self, str, int_type=False):
        parsed = str.replace('\u202c', '').replace('\u202d', '').strip()
        if int_type:
            parsed = parsed.replace('.', '')
        return parsed


class Dorf2:
    def __init__(self):
        self.html_parser = None

    def parse(self, html_parser, _type):
       return NotImplemented
