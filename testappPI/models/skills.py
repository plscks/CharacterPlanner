class Skills:
    def __init__(self, level, name, cost, parent, skill_class):
        self.level = level
        self.name = name
        self.cost = cost
        self.parent = parent
        self.skill_class = skill_class
        self.hp_max = 0
        self.mp_max = 0
        self.ap_max = 0
        self.weigh_max = 0
        self.melee_acc = 0
        self.sword_acc = 0
        self.hth_acc = 0
        self.bow_acc = 0
        self.firearm_acc = 0
        self.thrown_acc = 0
        self.spell_acc = 0
        self.ehw_acc = 0
        self.death_type = 0
        self.melee_dam = 0
        self.sword_dam = 0
        self.hth_dam = 0
        self.bow_dam = 0
        self.firearm_dam = 0
        self.thrown_dam = 0
        self.gen_spell_dam = 0
        self.gem_spell_dam = 0
        self.dodge = 0
        self.evade = 0
        self.impact_soak = 0
        self.slash_soak = 0
        self.pierce_soak = 0
        self.acid_soak = 0
        self.cold_soak = 0
        self.fire_soak = 0
        self.elec_soak = 0
        self.death_soak = 0
        self.holy_soak = 0
        self.unholy_soak = 0
        self.arcane_soak = 0
        self.hide = 0
        self.search = 0
        # TODO Character.add_skill() needs to accommodate the resistances??
        self.impact_res = ''
        self.piercing_res = ''
        self.slashing_res = ''
        self.fire_res = ''
        self.cold_res = ''
        self.electric_res = ''
        self.acid_res = ''
        self.holy_res = ''
        self.unholy_res = ''
        self.arcane_res = ''
        self.death_res = ''

        if self.name == 'Hand-to-Hand Combat':
            self.hth_acc = 20
        elif self.name == 'Melee Combat':
            self.melee_acc = 20
        elif self.name == 'Ranged Combat':
            self.bow_acc = 20
            self.thrown_acc = 20
            self.firearm_acc = 20
        elif self.name == 'Martial Arts':
            self.hth_acc = 10
        elif self.name == 'Boxing':
            self.hth_dam = 1
        elif self.name == 'Advanced Martial Arts':
            self.hth_acc = 10
        elif self.name == 'Firearms':
            self.firearm_acc = 10
        elif self.name == 'Archery':
            self.bow_acc = 10
        elif self.name == 'Thrown Weapons':
            self.thrown_acc = 10
        elif self.name == 'Advanced Thrown Weapons':
            self.thrown_acc = 10
        elif self.name == 'Advanced Archery':
            self.bow_acc = 10
        elif self.name == 'Advanced Firearms':
            self.firearm_acc = 10
        elif self.name == 'Advanced Melee Combat':
            self.melee_acc = 10
        elif self.name == 'Expert Melee Combat':
            self.melee_acc = 10
        elif self.name == 'Dodge':
            self.dodge = 5
        elif self.name == 'Evasion':
            self.evade = 5
        elif self.name == 'Advanced Dodge':
            self.dodge = 5
            self.evade = 5
        elif self.name == 'Hide':
            self.hide = 20
        elif self.name == 'Advanced Hide':
            self.hide = 10
        elif self.name == 'Strength':
            self.weigh_max = 10
            self.ehw_acc = 5
        elif self.name == 'Stamina':
            self.hp_max = 10
        elif self.name == 'Combat Mastery':
            self.melee_acc = 5
            self.hth_acc = 5
            self.bow_acc = 5
            self.firearm_acc = 5
            self.thrown_acc = 5
            self.sword_acc = 5
        elif self.name == 'Super Reflexes':
            self.dodge = 5
            self.evade = 5
        elif self.name == 'Spellcraft':
            self.spell_acc = 20
        elif self.name == 'Spell Combat':
            self.spell_acc = 15
        elif self.name == 'Battle Magic':
            self.spell_acc = 10
        elif self.name == 'Natural Predator':
            self.hth_acc = 10
            self.hth_dam = 1
        elif self.name == 'Shadow of the Dust':
            self.hp_max = -10
            self.piercing_res = '25%'
            self.impact_res = '25%'
            self.slashing_res = '25%'
        elif self.name == 'Tattoo of Blood':
            self.hp_max = 5
        elif self.name == 'Tattoo of Soul':
            self.mp_max = 5
        elif self.name == 'Tattoo of Inner Strength':
            self.hp_max = 10
            self.mp_max = 5
        elif self.name == 'Tattoo of Resistance':
            self.impact_soak = 3
            self.slash_soak = 3
            self.pierce_soak = 3
            self.elec_soak = 6
            self.cold_soak = 6
            self.fire_soak = 6
            self.acid_soak = 5
            self.death_soak = 5
            self.arcane_soak = 4
            self.holy_soak = 4
            self.unholy_soak = 4
        elif self.name == 'Tattoo of Sorcery':
            self.spell_acc = 20
        elif self.name == 'Master of the Lashing Kick':
            self.hth_acc = 5
        elif self.name == 'Way of Earth':
            self.impact_res = '25%'
            self.piercing_res = '25%'
            self.slashing_res = '25%'
            self.fire_res = '20%'
            self.cold_res = '20%'
            self.electric_res = '15%'
            self.acid_res = '15%'
            self.holy_res = '20%'
            self.unholy_res = '20%'
            self.arcane_res = '20%'
            self.death_res = '15%'
        elif self.name == 'Way of Vim':
            self.hp_max = 10
        elif self.name == 'Magical Reserves':
            self.mp_max = 5
        elif self.name == 'Divine Armor':
            self.impact_soak = 3
            self.pierce_soak = 3
            self.slash_soak = 3
            self.holy_soak = 4
            self.arcane_soak = 2
            self.fire_soak = 2
            self.cold_soak = 2
            self.elec_soak = 2
            self.death_soak = 2
            self.acid_soak = 2
        elif self.name == 'Hulking Brute':
            self.hp_max = 25
        elif self.name == 'Fiendish Bulk':
            self.hp_max = 35

    def to_dict(self):
        json = {
            'level': self.level,
            'name': self.name,
            'cost': self.cost,
            'parent': self.parent,
            'skill_class': self.skill_class,
            'hp_max': self.hp_max,
            'mp_max': self.mp_max,
            'ap_max': self.ap_max,
            'weigh_max': self.weigh_max,
            'melee_acc': self.melee_acc,
            'sword_acc': self.sword_acc,
            'hth_acc': self.hth_acc,
            'bow_acc': self.bow_acc,
            'firearm_acc': self.firearm_acc,
            'thrown_acc': self.thrown_acc,
            'spell_acc': self.spell_acc,
            'ehw_acc': self.ehw_acc,
            'death_type': self.death_type,
            'melee_dam': self.melee_dam,
            'sword_dam': self.sword_dam,
            'hth_dam': self.hth_dam,
            'bow_dam': self.bow_dam,
            'firearm_dam': self.firearm_dam,
            'thrown_dam': self.thrown_dam,
            'gen_spell_dam': self.gen_spell_dam,
            'gem_spell_dam': self.gem_spell_dam,
            'dodge': self.dodge,
            'evade': self.evade,
            'impact_soak': self.impact_soak,
            'slash_soak': self.slash_soak,
            'pierce_soak': self.pierce_soak,
            'acid_soak': self.acid_soak,
            'cold_soak': self.cold_soak,
            'fire_soak': self.fire_soak,
            'elec_soak': self.elec_soak,
            'death_soak': self.death_soak,
            'holy_soak': self.holy_soak,
            'unholy_soak': self.unholy_soak,
            'arcane_soak': self.arcane_soak,
            'hide': self.hide,
            'search': self.search,
            'impact_res': self.impact_res,
            'piercing_res': self.piercing_res,
            'slashing_res': self.slashing_res,
            'fire_res': self.fire_res,
            'cold_res': self.cold_res,
            'electric_res': self.electric_res,
            'acid_res': self.acid_res,
            'holy_res': self.holy_res,
            'unholy_res': self.unholy_res,
            'arcane_res': self.arcane_res,
            'death_res': self.death_res
        }

        return json

    def to_dict2(self):
        skill_dict = {}
        for attr in vars(self):
            attr_value = getattr(self, attr)
            skill_dict[attr] = attr_value
        return skill_dict