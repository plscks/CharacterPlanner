import csv
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.sql import select, update, insert

from testappPI.services.database import SkillDB, SpellDB


class SkillAttrib:
    def __init__(self, skill_name, base_skill, has_child, parent_skill, CP_cost, skill_class, turned_off, desc):
        self.skill_name = skill_name
        self.base_skill = base_skill
        self.parent_skill = parent_skill
        self.has_child = has_child
        self.CP_cost = CP_cost
        self.skill_class = skill_class
        self.turned_off = turned_off
        self.desc = desc


def key_in(key, dict):
    if key in dict.keys():
        return True
    else:
        return False
    