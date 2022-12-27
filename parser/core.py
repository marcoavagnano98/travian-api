import bs4
import time
from . import *
from . import models
import re


class Parser:

    def __init__(self, session):
        self.current_url = None
        self.session = session
        self.html_parser = None
        self.last_reload = 0
        self.treshold_reload = 2  # reload each 2 secs
        self.d1 = models.Dorf1()

    def set(self, url):
        time_elapsed = time.time() - self.last_reload
        if time_elapsed > self.treshold_reload or url != self.current_url:
            self.current_url = url
            html_page = self.session.get_request(url=url).text
            self.html_parser = bs4.BeautifulSoup(html_page, 'html5lib')
            self.last_reload = time.time()

    def parse(self, url, _type):
        self.set(url)
        if "dorf1" in url:
            return self.d1.parse(self.html_parser, _type)
        if "dorf2" in url:
            return None
