from .models import Dorf1, Dorf2
from .parser_type import ParseType as Pt


class ParserController:
    def __init__(self, session, base_url):
        self.d1 = Dorf1(session=session, base_url=base_url)
        self.d2 = Dorf2(session=session, base_url=base_url)

    def parse(self, params, _type):
        if "dorf1" in params:
            # before doing whatever thing in models it must set the parser to get right html page
            self.d1.set(params)
            if _type is Pt.MOVEMENTS:
                link = self.d1.get_movements_link()
                if link:
                    self.d1.set(link)
            return self.d1.parse(_type)
        if "dorf2" in params:
            self.d2.set(params)
            return self.d2.parse(_type)
