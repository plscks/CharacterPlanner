class Character:
    """
    The Character class is a Nexus Clash character object, it should hold all of the data that a character would.
    Skills along with a skill history, basic stats, level up function, as much as I can get to work really.
    """
    def __init__(self, name, level=1, hp=50, mp=20, ap=50, cp=10, spent_cp=0, skills=[], class_2=None, class_3=None, class_2_choice='Paladin', class_3_choice='Seraph'):
        self.name = name
        self.level = level
        self.hp_max = hp
        self.mp_max = mp
        self.ap_max = ap
        self.cp = cp
        self.spent_cp = spent_cp
        self.skills = skills
        self.class_1 = 'Mortal'
        self.class_2 = class_2
        self.class_3 = class_3
        self.class_2_choice = class_2_choice
        self.class_3_choice = class_3_choice
        self.weigh_max = 50
        self.melee_acc = 25
        self.sword_acc = 25
        self.hth_acc = 25
        self.bow_acc = 25
        self.firearm_acc = 25
        self.thrown_acc = 25
        self.spell_acc = 25
        self.ehw_acc = -20
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
        self.descPane = True
        self.spellPane = False
        self.spellPaneSelect = None
        self.mortal_exits = [
            ['Mortal', 'Paladin'],
            ['Mortal', 'Shepherd'],
            ['Mortal', 'Myrmidon'],
            ['Mortal', 'Sorcerer'],
            ['Mortal', 'Pariah'],
            ['Mortal', 'Defiler']
        ]       
        self.t2_exits = [
            ['Paladin', 'Exalted Harbinger'],
            ['Paladin', 'Seraph'],
            ['Paladin', 'Holy Champion'],
            ['Paladin', 'Fallen'],
            ['Shepherd', 'Advocate'],
            ['Shepherd', 'Archon'],
            ['Shepherd', 'Lightspeaker'],
            ['Shepherd', 'Fallen'],
            ['Myrmidon', 'Eternal Soldier'],
            ['Myrmidon', 'Nexus Champion'],
            ['Myrmidon', 'Revenant'],
            ['Sorcerer', 'Conduit'],
            ['Sorcerer', 'Wizard'],
            ['Sorcerer', 'Lich'],
            ['Sorcerer', 'Elementalist'],
            ['Pariah', 'Infernal Behemoth'],
            ['Pariah', 'Void Walker'],
            ['Pariah', 'Doom Howler'],
            ['Pariah', 'Redeemed'],
            ['Defiler', 'Dark Oppressor'],
            ['Defiler', 'Wyrm Master'],
            ['Defiler', 'Corruptor'],
            ['Defiler', 'Redeemed']
        ]

    def skillbuy(self, skill, cost, parent, reclass):
        from .skills import Skills
        classlist = [self.class_1, self.class_2, self.class_3]
        if self.cp - cost < 0:
            print(f'You do not have enough CP to purchase {skill}! It costs {cost} CP, you have only {self.cp}!')
            return
        elif reclass not in classlist:
            print(f'You must be a {reclass} in order to buy {skill}!')
            return
        else:
            if parent == '':
                self.cp = self.cp - cost
                self.spent_cp = self.spent_cp + cost
                self.skills.append(Skills(self.level, skill, cost, parent, reclass))
                self.addskill()
                print(f'You have purchased {skill} for {cost}cp! You now have {self.cp}cp')
            else:
                ownsparent = 0
                for row in self.skills:
                    if row.name != parent:
                        pass
                    else:
                        ownsparent = 1

                if ownsparent == 1:
                    self.cp = self.cp - cost
                    self.spent_cp = self.spent_cp + cost
                    self.skills.append(Skills(self.level, skill, cost, parent, reclass))
                    self.addskill()
                    print(f'You have purchased {skill} for {cost}cp! You now have {self.cp}cp')
                else:
                    print(f'You do not have the prerequisite skill of {parent} required to purchase {skill}')
                    return
            if self.class_2 == None and self.spent_cp >= 70 and self.level >= 10:
                self.chooseclass(2, self.class_2_choice)
            elif self.class_3 == None and self.class_2 != None and self.spent_cp >= 250 and self.level >= 20:
                self.chooseclass(3, self.class_3_choice)

    def levelup(self):
        if self.level == 30:
            print(f'You have reached maxx level and cannot grow stronger!')
            return

        self.level = self.level + 1
        self.mp_max = self.mp_max + 1
        self.cp = self.cp + 10

        if self.level >= 10:
            self.ap_max = self.ap_max + 1
            self.hp_max = self.hp_max + 1
            self.cp = self.cp + 10
            if self.level == 10 and self.class_2_choice:
                self.chooseclass(2, self.class_2_choice)

        if self.level >= 20:
            self.cp = self.cp + 10
            if any(x.name == 'Magical Reserves' for x in self.skills):
                self.mp_max = self.mp_max + 1
            if self.level == 20 and self.class_3_choice:
                self.chooseclass(3, self.class_3_choice)

        return f'You are now level {self.level} you have {self.cp}cp and have spent {self.spent_cp}'

    def delevel(self):
        print(f'Deleveling:')
        if not self.skills:
            if self.level == 1:
                print(f'You cannot level down any farther than level {self.level}!')
                return
            if 10 <= self.level <= 19:
                level_cp = 20
                self.ap_max = self.ap_max - 1
                self.hp_max = self.hp_max - 1
            elif self.level >= 20:
                level_cp = 30
                self.ap_max = self.ap_max - 1
                self.hp_max = self.hp_max - 1
            else:
                level_cp = 10
            self.mp_max = self.mp_max - 1
            self.cp = self.cp - level_cp
            self.level = self.level - 1
            print(f'New level is {self.level} new cp total is {self.cp}, new spent cp total is {self.spent_cp}')
            self.listskills()
        else:
            if self.skills[len(self.skills)-1].level == self.level:
                self.remove_last_skill()
            else:
                if 10 <= self.level <= 19:
                    level_cp = 20
                    self.ap_max = self.ap_max - 1
                    self.hp_max = self.hp_max - 1
                elif self.level >= 20:
                    level_cp = 30
                    self.ap_max = self.ap_max - 1
                    self.hp_max = self.hp_max - 1
                else:
                    level_cp = 10
                self.mp_max = self.mp_max - 1
                self.cp = self.cp - level_cp
                self.level = self.level - 1
                print(f'New level is {self.level} new cp total is {self.cp}, new spent cp total is {self.spent_cp}')
                self.listskills()

    def stats(self, size=0):
        if size == 'sum':
            if self.class_3 != '' and self.level >= 20:
                upperclass = self.class_3
            elif self.class_2 != '' and self.class_3 == '' and self.level >= 10:
                upperclass = self.class_2
            else:
                upperclass = self.class_1

            stat1 = f'{self.name} a level {self.level} {upperclass}'
            stat2 = f' HP: {self.hp_max}  AP: {self.ap_max}  MP: {self.mp_max}'
            stat3 = f' Banked CP: {self.cp}  Spent CP {self.spent_cp}'
            print(stat1, stat2, stat3)
        else:
            for thing in dir(self):
                if isinstance(getattr(self, thing), str) or isinstance(getattr(self, thing), int):
                    print(f'{thing}: {getattr(self, thing)}')

    def addskill(self):
        for skill in dir(self.skills[-1]):
            if getattr(self.skills[-1], skill) != 0 and skill != 'level' and isinstance(getattr(self.skills[-1], skill),
                                                                                        int) and skill != 'cost':
                setattr(self, skill, getattr(self.skills[-1], skill) + getattr(self, skill))

    def remove_last_skill(self):
        last_skill = self.skills[len(self.skills)-1]
        for stat in dir(last_skill):
            if getattr(last_skill, stat) != 0 and stat != 'level' and isinstance(
                    getattr(last_skill, stat),
                    int) and stat != 'cost':
                setattr(self, stat, getattr(self, stat) - getattr(last_skill, stat))
        self.cp = self.cp + last_skill.cost
        self.spent_cp = self.spent_cp - last_skill.cost
        print(f'Removing {last_skill.name}, refunding skill cost of {last_skill.cost}cp.')
        print(f'New cp total is {self.cp} new spent cp total is {self.spent_cp}')
        self.skills.remove(last_skill)

    def sellskill(self, skill):
        for skillcheck in self.skills:
            if skillcheck.parent == skill:
                print(f'You cannot remove {skill} without first removing {skillcheck.name}!')
                return f'You cannot remove {skill} without first removing {skillcheck.name}!'
            else:
                return self.removeskill(skill)

    def removeskill(self, removedskill):
        killskill = []
        for skill in self.skills:
            if skill.name == removedskill:
                for stat in dir(skill):
                    if getattr(skill, stat) != 0 and stat != 'level' and isinstance(
                            getattr(skill, stat),
                            int) and stat != 'cost':
                        setattr(self, stat, getattr(self, stat) - getattr(skill, stat))
                self.cp = self.cp + skill.cost
                self.spent_cp = self.spent_cp - skill.cost
                print(f'Removing {skill.name}, refunding skill cost of {skill.cost}cp.')
                print(f'New cp total is {self.cp} new spent cp total is {self.spent_cp}')
                killskill.append(skill)
        if not killskill:
            failure = f'You don\'t seem to  know the skill {removedskill}!'
            print(failure)
            return failure
        else:
            for remove in killskill:
                for skill_in_list in self.skills:
                    if skill_in_list == remove:
                        self.skills.remove(skill_in_list)
            return True

    def listskills(self):
        print(f'Known skills:')
        knownskills = []
        for skill in self.skills:
            knownskills.append(skill.name)
            print(f'{skill.name} - {skill.cost}cp - purchased at level {skill.level} object: {skill}')
        return knownskills

    def chooseclass(self, tier, chosen_class):
        ## TODO fix spells in turncoat area
        classskills = {
            'Exalted Harbinger': 'Demon Tracker',
            'Seraph': 'Corpus Machina',
            'Holy Champion': 'Holy Radiance',
            'Advocate': 'Holy Intercessor',
            'Archon': 'Divine Vengeance',
            'Lightspeaker': 'Faunabond',
            'Fallen': 'Fractured Vessel',
            'Eternal Soldier': 'Way of Vim',
            'Nexus Champion': 'Tattoo of Balance',
            'Revenant': 'Strength of Darkness',
            'Conduit': 'Code of Efficiency',
            'Wizard': 'Magical Reserves',
            'Lich': 'Paragon of Death',
            'Elementalist': 'Child of the Elements',
            'Infernal Behemoth': 'Hulking Brute',
            'Void Walker': 'Stepping of the Corner',
            'Doom Howler': 'Unsettling Aura',
            'Dark Oppressor': 'Lord over Domain',
            'Wyrm Master': 'Acid Blood',
            'Corruptor': 'Manabiter',
            'Redeemed': 'Mask of the Penitent',
            'Myrmidon': 'Combination Attack',
            'Sorcerer': 'Spellcraft',
            'Paladin': 'Divine Investiture',
            'Shepherd': 'Prayer',
            'Pariah': 'Stygian Fury',
            'Defiler': 'Desecration'
        }
        turncoatswap = {
            'Paladin': {
                'Divine Investiture': 'Heal Self',
                'Heal Self': 'Divine Investiture',
                'Bolster Attack': 'Enervate',
                'Enervate': 'Bolster Attack',
                'Crusader Piety': 'Agitating Ardor',
                'Agitating Ardor': 'Crusader Piety',
                'Crusader Zeal': 'Agitating Fervor',
                'Agitating Fervor': 'Crusader Zeal',
                'Divine Armor': 'Exploit Weakness',
                'Exploit Weakness': 'Divine Armor',
                'Helmet of Justice': 'Unabated Malice',
                'Unabated Malice': 'Helmet of Justice',
                'Hand of Zealotry': 'Unholy Avoidance',
                'Unholy Avoidance': 'Hand of Zealotry',
                'Holier Than Thou': 'Callous Celerity',
                'Callous Celerity': 'Holier Than Thou',
                'Holy Avenger': 'Shadow Dirk',
                'Shadow Dirk': 'Holy Avenger',
                'Lay On Hands': 'Feast on Suffering',
                'Feast on Suffering': 'Lay On Hands',
                'Smite': 'Hellfire',
                'Hellfire': 'Smite',
                'Shield of Faith': 'Mutual Suffering',
                'Mutual Suffering': 'Shield of Faith'
            },
            'Shepherd': {
                'Prayer': 'Desecration',
                'Desecration': 'Prayer',
                'Absolve Suffering': 'Poison',
                'Poison': 'Absolve Suffering',
                'Sacred Alchemy': 'Foul Alchemy',
                'Foul Alchemy': 'Sacred Alchemy',
                'Devout Supplication': 'Thorough Desecration',
                'Thorough Desecration': 'Devout Supplication',
                'Energize': 'Hellfire',
                'Hellfire': 'Energize',
                'Heal Others': 'Heal Self',
                'Heal Self': 'Heal Others',
                'Sanctify Spell': 'Taint Spell',
                'Taint Spell': 'Sanctify Spell',
                'Glyph of Pain vs Evil': 'Glyph of Pain vs Good',
                'Glyph of Sapping vs Evil': 'Glyph of Sapping vs Good',
                'Glyph of Protection vs Evil': 'Glyph of Protection vs Good',
                'Glyph of Slowing vs Evil': 'Glyph of Slowing vs Good',
                'Fist of the Eel': 'Corrosive Grasp',
                'Cloudburst': 'Noxious Globule',
                'Shocking Dart': 'Acid Dart',
                'Spark Spray': 'Bilious Purge',
                'Thunder Bolt': 'Caustic Bolt',
                'Static Charge': 'Acrid Vapors'
            },
            'Defiler': {
                'Desecration': 'Last Rites',
                'Last Rites': 'Desecration',
                'Dark Heart': 'Energize',
                'Energize': 'Dark Heart',
                'Foul Alchemy': 'Sacred Alchemy',
                'Sacred Alchemy': 'Foul Alchemy',
                'Soul Vampire': 'Hands of the Healer',
                'Hands of the Healer': 'Soul Vampire',
                'Demoralize': 'Encourage',
                'Encourage': 'Demoralize',
                'Life Vampire': 'Heal Others',
                'Heal Others': 'Life Vampire',
                'Poison': 'Absolve Suffering',
                'Absolve Suffering': 'Poison',
                'Taint Spell': 'Sanctify Spell',
                'Sanctify Spell': 'Taint Spell',
                'Glyph of Pain vs Good': 'Glyph of Pain vs Evil',
                'Glyph of Sapping vs Good': 'Glyph of Sapping vs Evil',
                'Glyph of Protection vs Good': 'Glyph of Protection vs Evil',
                'Glyph of Slowing vs Good': 'Glyph of Slowing vs Evil',
                'Corrosive Grasp': 'Fist of the Eel',
                'Noxious Globule': 'Cloudburst',
                'Acid Dart': 'Shocking Dart',
                'Bilious Purge': 'Spark Spray',
                'Caustic Bolt': 'Thunder Bolt',
                'Acrid Vapors': 'Static Charge'
            },
            'Pariah': {
                'Blood Claws': 'Scarred Nails',
                'Scarred Nails': 'Blood Claws',
                'Blood Taste': 'Supernal Volley',
                'Supernal Volley': 'Blood Taste',
                'Enervate': 'Shield of Mercy',
                'Shield of Mercy': 'Enervate',
                'Rend Flesh': 'Enfolding Mercy',
                'Enfolding Mercy': 'Rend Flesh',
                'Feast on Suffering': 'Hands of the Healer',
                'Hands of the Healer': 'Feast on Suffering',
                'Hellfire': 'Dead to Sin',
                'Dead to Sin': 'Hellfire',
                'Strike of Cain': 'Acceptable Sacrifice',
                'Acceptable Sacrifice': 'Strike of Cain',
                'Stygian Fury': 'Stygian Atonement',
                'Stygian Atonement': 'Stygian Fury',
                'Blooded Fury': 'Glory in Suffering',
                'Glory in Suffering': 'Blooded Fury',
                'Explosive Murder': 'Sublime Sacrifice',
                'Sublime Sacrifice': 'Explosive Murder'
            }
        }
        char_classes = [self.class_1, self.class_2, self.class_3]
        if chosen_class not in char_classes:
            old_t2_class = self.class_2
            old_t3_class = self.class_3
            # Add to choice but nothing more if not able to change class now.
            if tier == 3 and (self.level < 20 or self.spent_cp < 250):
                print(f'Setting tier 3 class choice to {chosen_class}')
                self.class_3_choice = chosen_class
                return
            elif tier == 2 and (self.level < 10 or self.spent_cp < 70):
                print(f'Setting tier 2 class choice to {chosen_class}')
                self.class_2_choice = chosen_class
                return
            # If there is a tier 3 class selected then remove it and all of its skills
            if self.class_3 != None:
                # Nuke T3 skills and delevel down to at least the free skill
                while self.class_3 == old_t3_class:
                    last_skill = self.skills[len(self.skills) - 1]
                    if last_skill.cost != 0:
                        # Delevel until get to free skill
                        self.delevel()
                    else:
                        self.class_3 = None
            if tier == 2:
                last_skill = self.skills[len(self.skills) - 1]
                if self.class_2 == None and self.level >= 10 and self.spent_cp >= 70:
                    # Can buy tier 2 now, do it
                    print(f'Buying new class: {chosen_class}')
                    self.class_2 = chosen_class
                    self.class_2_choice = chosen_class
                    self.skillbuy(classskills[chosen_class], 0, '', chosen_class)
                    return
                else:
                    if last_skill.cost == 0 and last_skill.skill_class == old_t3_class:
                        # nuke the free T3 skill
                        self.delevel()
                    while self.class_2 == old_t2_class:
                        last_skill = self.skills[len(self.skills)-1]
                        if last_skill.cost != 0 and last_skill.skill_class != old_t3_class:
                            self.delevel()
                        else:
                            # At free skill change class and stuff
                            # Remove free skill
                            self.remove_last_skill()
                            # Set new tier 2
                            self.class_2_choice = chosen_class
                            # Buy new tier 2 if able and get free skill
                            if self.level >= 10 and self.spent_cp >= 70:
                                print(f'Buying new class: {chosen_class}')
                                self.class_2 = chosen_class
                                self.skillbuy(classskills[chosen_class], 0, '', chosen_class)
            else:
                last_skill = self.skills[len(self.skills) - 1]
                if self.class_3 == None and last_skill.cost !=0:
                    print(f'Buying new class: {chosen_class}')
                    # Can buy tier 3 now, do it
                    self.class_3 = chosen_class
                    self.class_3_choice = chosen_class
                    self.skillbuy(classskills[chosen_class], 0, '', chosen_class)
                    if chosen_class == 'Fallen' or chosen_class == 'Redeemed':
                        # Have chosen a turncoat class for T3, need to swap T2 skills
                        self.class_2 = f'Ex-{old_t2_class}'
                        self.class_2_choice = f'Ex-{old_t2_class}'
                        skillswap = turncoatswap[old_t2_class]
                        for i, skill in enumerate(self.skills):
                            if skill.skill_class == old_t2_class:
                                if skill.name in skillswap:
                                    print(f'Removing {skill.name} and buying {skillswap[skill.name]}')
                                    self.addturncoatskill(skill.name, skillswap)
                                else:
                                    print(f'Nothing to change for {skill.name}, removing and rebuying under new T2 class.')
                                    self.skills[i].skill_class = self.class_2
                        return
                    else:
                        return
                else:
                    #if self.skills[len(self.skills)-1]
                    self.remove_last_skill()
                    # Set new tier 3
                    print(f'Buying new class: {chosen_class}')
                    self.class_3_choice = chosen_class
                    # Buy new tier 3 if able and get free skill
                    if self.level >= 19 and self.spent_cp >= 250:
                        self.class_3 = chosen_class
                        self.skillbuy(classskills[chosen_class], 0, '', chosen_class)
        else:
            return

    def addturncoatskill(self, oldskill, skillswap):
        # function to exchange turncoat skills
        # First remove old skill attributes
        from .skills import Skills
        for skill in self.skills:
            if skill.name == oldskill:
                cost = 0
                reclass = self.class_2
                newskill = skillswap[skill.name]
                if skill.parent and skill.parent in skillswap:
                    parent = skillswap[skill.parent]
                else:
                    parent = ''
                for stat in dir(skill):
                    if getattr(skill, stat) != 0 and stat != 'level' and isinstance(
                            getattr(skill, stat),
                            int) and stat != 'cost':
                        setattr(self, stat, getattr(self, stat) - getattr(skill, stat))
                print(f'Removing {skill.name} attributes and refunding skill cost of {cost}cp.')
                print(f'New cp total is {self.cp} new spent cp total is {self.spent_cp}')
                # buy new skill
                self.skills.append(Skills(self.level, newskill, cost, parent, reclass))
                self.addskill()
                print(f'You have purchased {newskill} for {cost}cp! You now have {self.cp}cp')
        return

    def to_dict(self):
        json = {
            'name': self.name,
            'level': self.level,
            'hp_max': self.hp_max,
            'mp_max': self.mp_max,
            'ap_max': self.ap_max,
            'cp': self.cp,
            'spent_cp': self.spent_cp,
            'skills': [s.to_dict() for s in self.skills],
            'class_1': self.class_1,
            'class_2': self.class_2,
            'class_3': self.class_3,
            'class_2_choice': self.class_2_choice,
            'class_3_choice': self.class_3_choice,
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
            'death_res': self.death_res,
            'descPane': self.descPane,
            'spellPane': self.spellPane,
            'spellPaneSelect': self.spellPaneSelect
        }

        return json


    def setPane(self, pane, type):
        print(f'setPane(pane: {pane}, type: {type})')
        if pane == 'Desc':
            self.descPane = not self.descPane
        elif pane == 'Spells':
            self.spellPane = not self.spellPane
        else:
            # Pane is '' so set spell
            self.spellPaneSelect = type


    def to_dict2(self):
        char_dict = {}
        skill_list = []
        for attr in vars(self):
            attr_value = getattr(self, attr)
            if attr == 'skills':
                char_dict[attr] = skill_list
                for skill in attr_value:
                    skill_dict = skill.to_dict2()
                    char_dict[attr].append(skill_dict)
            else:
                char_dict[attr] = attr_value
        return char_dict


    def exit_classes(self, t2_choice):
        exits = []
        for thing in self.t2_exits:
            if thing[0] == t2_choice:
                exits.append(thing[1])
        return exits