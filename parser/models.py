import re
import bs4
import time
from .parser_type import ParseType as Pt


class Parser:
    def __init__(self, session, base_url):
        self.current_url = None
        self.base_url = base_url
        self.session = session
        self.html_parser = None
        self.last_reload = 0
        self.treshold_reload = 2  # reload each 2 secs

    def set(self, params):
        url = self.base_url + params
        time_elapsed = time.time() - self.last_reload
        if time_elapsed > self.treshold_reload or url != self.current_url:
            self.current_url = url
            html_page = self.session.get_request(url=url).text
            self.html_parser = bs4.BeautifulSoup(html_page, 'html5lib')
            self.last_reload = time.time()

    def clean(self, _str, int_type=False):
        parsed = _str.replace('\u202c', '').replace('\u202d', '').strip()
        if int_type:
            parsed = parsed.replace('.', '')
        return parsed


class Dorf1(Parser):
    def __init__(self, session, base_url):
        super().__init__(session, base_url)

    def parse(self, _type):

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
        if _type is Pt.BUILDING_LIST:
            return self.queue_buildings()
        # if _type is Pt.MOVEMENTS:
        #     return self.get_movements()

    def get_silver_gold_amount(self):
        gold_text = self.clean(self.html_parser.find('div', {'class': 'ajaxReplaceableGoldAmount'}).text, True)
        silver_text = self.clean(self.html_parser.find('div', {'class': 'ajaxReplaceableSilverAmount'}).text, True)

        return {'gold': int(gold_text), 'silver': int(silver_text)}

    def get_warehouse_amount(self):
        amount = self.html_parser.select_one('div.warehouse > div.capacity > div.value').text
        return int(self.clean(amount, True))

    def get_population(self):
        amount = self.clean(self.html_parser.select_one('div.population > span').text, True)
        return int(amount)

    def get_granary_amount(self):
        amount = self.html_parser.select_one('div.granary > div.capacity > div.value').text
        return int(self.clean(amount, True))

    def get_production(self):
        production = {}
        lines = self.html_parser.select('table#production > tbody > tr')
        for line in lines:
            res, num = line.select('td.num,td.res')
            production[self.clean(res.text).replace(':', '')] = int(self.clean(num.text))
        return production

    def get_troops(self):
        troops = {}
        if not self.html_parser.select_one('td.noTroops'):
            for line in self.html_parser.select('table#troops > tbody > tr'):
                num, unit = line.select('td.un,td.num')
                troops[unit.text] = int(self.clean(num.text))
        return troops

    def get_villages_tags(self):
        return self.html_parser.select('div.villageList > div.dropContainer > div.listEntry')

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

    def queue_buildings(self):
        queue = []  # 0: name, 1: level 2: time left, 3: end time
        if self.html_parser.select('div.buildingList'):
            for line in self.html_parser.select('div.buildingList > ul > li'):
                name_and_level, build_duration = line.select('div.buildDuration,div.name')
                s_build_text = self.clean(build_duration.text).split(' ')
                queue.append([self.clean(name_and_level.text).split('\t')[0],
                              self.clean(name_and_level.find('span', {'class', 'lvl'}).text),
                              s_build_text[0],
                              s_build_text[-1]])
        return queue

    def get_movements_link(self):
        lines = self.html_parser.find('table', {'id': 'movements'})
        if lines:
            lines = lines.find_all('tr')  # check all table rows
            for line in lines:
                if line.select('td'):
                    attr = line.select_one('td > a[href]').attrs['href']
                    if attr:
                        return attr[1:] if attr[0] == '/' else attr

    # def get_movements(self):
    #     queue = []  # 0: name, 1: time to finish
    #     tables = self.html_parser.select('table.troop_details')
    #     if tables:
    #         village_name = self.clean(self.html_parser.select_one('td.role > a').text)
    #         for table in tables:
    #             # let's find if troops are in village or not
    #             if table.attrs["class"].split(' ') > 1:
    #                 # troops coming or in raid/attack/
    #                 pass
    #             else:
    #                 # troops standing in village
    #                 pass


class Dorf2(Parser):
    def __init__(self, session, base_url):
        super().__init__(session, base_url)

    def parse(self, _type):
        if _type is Pt.BUILDINGS:
            return self.get_buildings()

    def get_buildings(self):
        buildings = {}
        for line in self.html_parser.select('div#villageContent > div.buildingSlot'):
            attr = line.attrs['data-name']
            gid = line.attrs['data-gid']
            id = line.attrs['data-aid']
            if attr:
                buildings[attr] = {"level": self.clean(line.find('a').attrs['data-level']), "id": id, "gid": gid}
        return buildings
