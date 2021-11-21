import csv
from flask import current_app as app
from sqlalchemy import or_

from testappPI.models.skillAttrib import SkillAttrib

db = app.db

class SkillDB(db.Model):
    """The skills database table"""
    __table__ = db.Model.metadata.tables['skills']

    def __repr__(self):
        class_name = self.__getattribute__('class_name')
        return f'{self.skill_name} for {class_name}'


    def csv_to_dict(self):
        """Returns a dictionary where the keys are the id primary key column"""
        filepath = 'testappPI/services/' + self.__table__.name + '_templates.csv'
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            # columns
            # [0]skill_name, [1] parent_skill, [2]CP_cost, [3]class_name, [4]skill_id(primary key), [5]description, [6]turned_off, [7]grant_items, [8]initial_skill_grant, [9]boost_AP, [10]boost_HP, [11]boost_MP
            skills = {int(row[4]): [row[0], row[1], int(row[2]), row[3], int(row[4]), row[5], int(row[6]), row[7], row[8], int(row[9]), int(row[10]), int(row[11])] for row in reader}            
        return skills


    def updateDB(self):
        """Updates the skills database from a skill_templates.csv file in the services folder"""
        update = self.csv_to_dict()
        attributes = ['skill_name', 'parent_skill', 'CP_cost', 'class_name', 'skill_id', 'description', 'turned_off', 'grant_items', 'initial_skill_grant', 'boost_AP', 'boost_HP', 'boost_MP']
        for skill_id in update:
            old_skill = self.query.filter_by(skill_id = skill_id).first()
            # Check for existing skill
            if old_skill:
                needs_update = 0
                count = 0
                # If we have an existing skill, check its attributes against the new data
                for column in attributes:
                    if update[skill_id][count] != getattr(old_skill, column):
                        # If there is a change then change the database row
                        setattr(old_skill, column, update[skill_id][count])
                        needs_update = 1
                    count += 1
                if needs_update == 1:
                    # If we had any changes in the row, commit the changes
                    db.session.commit()
                else:
                    print(f'The {old_skill.skill_name} skill does not require an update at this time.')
            else:
                # if we don't have a skill with this ID, let's insert it
                new_skill = SkillDB()
                count = 0
                for column in attributes:
                    setattr(new_skill, column, update[skill_id][count])
                    count += 1
                db.session.add(new_skill)
                db.session.commit()


    def getSkills(self, class_name):
        """Get skills for a given class note filter_by() cannot utilize != one must use filter()"""
        from .skillDisplay import SkillAttrib
        masterlist = []
        skills1 = self.query.filter_by(class_name = class_name, turned_off = 0).all()
        for skill in skills1:
            has_child = self.count(self.query.filter_by(class_name = class_name, parent_skill = skill.skill_name, turned_off = 0).all())
            if skill.parent_skill == '':
                base_skill = 1
            else:
                base_skill = 0
            if has_child > 0:
                has_child = 1
            else:
                has_child = 0
            masterlist.append(SkillAttrib(skill.skill_name, base_skill, has_child, skill.parent_skill, int(skill.CP_cost), skill.class_name, int(skill.skill_id), skill.description))
        return masterlist


    def count(self, result_set=''):
        if result_set == '':
            length = len(self.query.all())
        else:
            length = len(result_set)
        return length
        
        
class SpellDB(db.Model):
    """The spells database table"""
    __table__ = db.Model.metadata.tables['spells']

    def __repr__(self):
        return self.spell_name


    def csv_to_dict(self):
        """Returns a dictionary where the keys are the id primary key column"""
        filepath = 'testappPI/services/' + self.__table__.name + '_templates.csv'
        with open(filepath, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            # columns
            # [0]id(primary key), [1]spell_name, [2]spell_weight, [3]spell_base, [4]attack_tree, [5]spell_MP_cost, [6]spell_CP_cost, [7]spell_damage, [8]spell_damage_type, [9]spell_type, [10]restriction, [11]description
            spells = {int(row[0]): [int(row[0]), row[1], int(row[2]), row[3], row[4], int(row[5]), int(row[6]), int(row[7]), row[8], row[9], row[10]] for row in reader}
        return spells


    def updateDB(self):
        """Updates the spells database from a .csv file named spell_templates.csv in the services folder"""
        update = self.csv_to_dict()
        attributes = ['id', 'spell_name', 'spell_weight', 'spell_base', 'attack_tree', 'spell_MP_cost', 'spell_CP_cost', 'spell_damage', 'spell_damage_type', 'spell_type', 'restriction', 'description']
        for spell_id in update:
            old_spell = self.query.filter_by(id = spell_id).first()
            # Check for existing skill
            if old_spell:
                needs_update = 0
                count = 0
                # If we have an existing skill, check its attributes against the new data
                for column in attributes:
                    if count == 11:
                        description = self.create_desc(update[spell_id])
                        if description != getattr(old_spell, column):
                            setattr(old_spell, column, description)
                            needs_update = 1
                    else:
                        if update[spell_id][count] != getattr(old_spell, column):
                            # If there is a change then change the database row
                            setattr(old_spell, column, update[spell_id][count])
                            needs_update = 1
                    count += 1
                if needs_update == 1:
                    # If we had any changes in the row, commit the changes
                    print(f'Updating existing spell: {old_spell.spell_name}')
                    db.session.commit()
                else:
                    print(f'The {old_spell.spell_name} spell does not require updating at this time')
            else:
                # if we don't have a skill with this ID, let's insert it
                new_spell = SpellDB()
                count = 0
                for column in attributes:
                    if count == 11:
                        description = self.create_desc(update[spell_id])
                        setattr(new_spell, column, description)
                    else:
                        setattr(new_spell, column, update[spell_id][count])
                    count += 1
                print(f'Inserting new spell: {new_spell.spell_name}')
                db.session.add(new_spell)
                db.session.commit()


    def create_desc(self, skill_row):
        """Function that creates a description for a spell"""
        restricted = skill_row[10]
        attack_tree = skill_row[4]
        spell_damage_type = skill_row[8]
        spell_damage = skill_row[7]
        if restricted != '':
            restricted_text = f'a {restricted} '
        else:
            if skill_row[9] == 'offensive':
                restricted_text = f'an '
            else:
                restricted_text = f'a '
        if attack_tree != '':
            attack_tree_text = f' that functions off of the {attack_tree} attack tree'
        else:
            attack_tree_text = ''
        if spell_damage_type != '':
            damage_text = f'{spell_damage_type} '
        else:
            damage_text = ''
        if spell_damage != 0:
            spell_damage_text = f', does {spell_damage} damage,'
        else:
            spell_damage_text = ''
        description = f'{skill_row[1]} is {restricted_text}{skill_row[9]} type {damage_text}spell{attack_tree_text}. It costs {skill_row[5]} mp to cast{spell_damage_text} and costs {skill_row[6]} CP to learn.'
        return description


    def getSpells(self, dude):
        """Get sspells for a given class note filter_by() cannot utilize != one must use filter()"""
        from .skillDisplay import SkillAttrib
        masterlist = {
            'Acid': [],
            'Cold': [],
            'Death': [],
            'Electric': [],
            'Fire': [],
            'Impact': [],
            'Piercing': [],
            'Slashing': [],
            'Glyph': [],
            'Utility': []
            }
        for type in masterlist:
            spells = []
            if type == 'Glyph':
                spells = self.query.filter(SpellDB.spell_name == SpellDB.spell_base, SpellDB.spell_damage_type == 'area').order_by(SpellDB.spell_MP_cost, SpellDB.attack_tree.desc()).all()
            elif type == 'Utility':
                spells = self.query.filter(SpellDB.spell_name == SpellDB.spell_base, or_(SpellDB.spell_damage_type == 'buff1', SpellDB.spell_damage_type == 'buff2')).order_by(SpellDB.spell_MP_cost, SpellDB.attack_tree.desc()).all()
            else:
                spells = self.query.filter(SpellDB.spell_name == SpellDB.spell_base, SpellDB.spell_damage_type == type.lower()).order_by(SpellDB.spell_MP_cost, SpellDB.attack_tree.desc()).all()
            masterlist[type] = [SkillAttrib(spell.spell_name, 1, 0, self.getReqClass(dude, spell)[0], int(spell.spell_CP_cost), self.getReqClass(dude, spell)[1], spell.spell_damage_type, spell.description) for spell in spells]        
        return masterlist


    def getReqClass(self, dude, spellrow):
        """Return a dude specific list where 0 is skill required for spells and position 1 is the class requirement"""
        spellskill = {
            'Sorcerer': 'Spellcraft',
            'Defiler': 'Spellcraft',
            'Shepherd': 'Spellcraft',
            'Ex-Defiler': 'Spellcraft',
            'Ex-Shepherd': 'Spellcraft',
            'Holy Champion': 'Spellcraft',
            'Nexus Champion': 'Tattoo of Sorcery',
            'Doom Howler': 'Spellcraft'
        }
        restricted = {
            'Non-Angel': ['Sorcerer', 'Defiler', 'Ex-Shepherd', 'Nexus Champion', 'Doom Howler'],
            'Non-Demon': ['Sorcerer', 'Shepherd', 'Ex-Difiler', 'Holy Champion', 'Nexus Champion']
        }
        returnlist = []
        if dude.class_2_choice not in spellskill.keys() and dude.class_3_choice not in spellskill.keys():
            return [False, False]
        else:
            if dude.class_2_choice in spellskill.keys():
                spelltier = 2
            elif dude.class_3_choice in spellskill.keys():
                spelltier = 3
            else:
                return [False, False]
        if spellrow.restriction == 'Tier 3':
            if spelltier == 2:
                returnlist = [spellskill[dude.class_2_choice], dude.class_3_choice]
            else:
                returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        elif spellrow.restriction == 'Non-Angel':
            if spelltier == 2:
                if dude.class_2_choice not in restricted['Non-Angel']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_2_choice], dude.class_2_choice]
            else:
                if dude.class_3_choice not in restricted['Non-Angel']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        elif spellrow.restriction == 'Non-Demon':
            if spelltier == 2:
                if dude.class_2_choice not in restricted['Non-Demon']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_2_choice], dude.class_2_choice]
            else:
                if dude.class_3_choice not in restricted['Non-Demon']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        elif spellrow.restriction == 'Non-Angel Tier 3':
            if spelltier == 2:
                if dude.class_2_choice not in restricted['Non-Angel']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_2_choice], dude.class_3_choice]
            else:
                if dude.class_3_choice not in restricted['Non-Angel']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        elif spellrow.restriction == 'Non-Demon Tier 3':
            if spelltier == 2:
                if dude.class_2_choice not in restricted['Non-Demon']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_2_choice], dude.class_3_choice]
            else:
                if dude.class_3_choice not in restricted['Non-Demon']:
                    returnlist = [False, False]
                else:
                    returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        else:
            if spelltier == 2:
                returnlist = [spellskill[dude.class_2_choice], dude.class_2_choice]
            else:
                returnlist = [spellskill[dude.class_3_choice], dude.class_3_choice]
        return returnlist


    def count(self):
        return len(self.query.all())
