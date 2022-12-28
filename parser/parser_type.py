from enum import Enum


class ParseType(Enum):
    # DORF1
    SILVER_GOLD = 1
    WAREHOUSE = 2
    GRANARY = 3
    TROOPS = 4
    POPULATION = 5
    COORDINATES = 6
    IDS = 7
    PRODUCTION = 8
    BUILDING_LIST = 9
    MOVEMENTS = 10
    # DORF2
    BUILDINGS = 11
