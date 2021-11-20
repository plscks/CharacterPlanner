"""Route declaration."""
#from wsgi import app
import json
from flask import render_template, make_response, request, url_for, redirect, g, session
from flask import current_app as app
from flask import json
from flask.json import jsonify
from sqlalchemy.sql.expression import false
from .forms import ContactForm, SignupForm
from .models import character, skills, skillAttrib
from .services import skillDisplay, database
#from . import db

db = app.db

nav = [
        {'name': 'Home', 'url': '/', 'id': 'home'},
        {'name': 'SignUp!', 'url': '/signup', 'id': 'signup'},
        {'name': 'API link', 'url': '/api', 'id': 'api'},
        {'name': 'B5 test server', 'url': 'javascript:alert("ACCESS DENIED!!! :P")', 'id': 'clash'},
        {'name': 'Learn Some Flask!', 'url': 'https://hackersandslackers.com/flask-jinja-templates', 'id': 'flask'},
        {'name': 'Contacts', 'url': '/contact', 'id': 'contacts'},
        {'name': 'Logout', 'url': '/logout', 'id': 'logout'},
        {'name': 'Planner', 'url': '/planner/', 'id': 'planner'}
    ]


@app.route('/')
def home():
    """Landing page."""
    # return render_template(
    #     'home.html',
    #     nav=nav,
    #     title="Is this a test?",
    #     description="It has to be a Flask test site..."
    # )
    session.pop('dude', None)
    return redirect(url_for('planner', tier2=None, tier3=None, reset=1))


@app.route('/skills/<selected_class>/', methods=['GET'])
def mortal_skills(selected_class):
    """Displays mortal skills"""
    skill_class = selected_class.title()
    skills_list = skillDisplay.skill_grab(db, skill_class)
    return render_template(
        'skilltree.html',
        title=selected_class,
        skills_list=skills_list,
        nav=nav
    )

@app.route('/planner/reset/')
def reset():
    session.pop('dude', None)
    return redirect(url_for('planner', tier2=None, tier3=None, reset=1))


@app.route('/planner/update/')
def update():
    # Update skills database from csv
    # spells = database.SpellDB()
    # spells.updateDB()
    # skills = database.SkillDB()
    # skills.updateDB()
    session.pop('dude', None)
    return redirect(url_for('planner', tier2=None, tier3=None, reset=1))


# Main planner route
@app.route('/planner/', defaults={'tier2': None, 'tier3': None, 'reset': 1}, methods=['GET'])
@app.route('/planner/<tier2>/', defaults={'tier3': None, 'reset': None}, methods=['GET'])
@app.route('/planner/<tier2>/<tier3>/', defaults={'reset': None}, methods=['GET'])
def planner(tier2, tier3, reset):
    skills = database.SkillDB()
    spells = database.SpellDB()
    print(f'reset: {reset}')
    if reset == 3:
        reset = 1
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set and reset == None:
        dude = session['dude']
    else:
        dude = character.Character('dude')
        session['dude'] = dude
    mortalskills = skills.getSkills('Mortal')
    if not tier2 and not tier3:
        print('not tier 2')
        t2skills = skills.getSkills(dude.class_2_choice)
        t3skills = skills.getSkills(dude.class_3_choice)
    elif tier2 and not tier3:
        print(f'tier2: {tier2} and not tier3: {tier3}')
        t2choice = tier2.title()
        dude.chooseclass(2, tier2)
        dude.chooseclass(3, dude.exit_classes(t2choice)[0])
        t2skills = skills.getSkills(t2choice)
        t3skills = skills.getSkills(dude.exit_classes(t2choice)[0])
    else:
        print('else')
        t2choice = tier2.title()
        t3choice = tier3.title()
        dude.chooseclass(2, tier2)
        dude.chooseclass(3, tier3)
        t2skills = skills.getSkills(t2choice)
        t3skills = skills.getSkills(t3choice)
        session['dude'] = dude
    allskills = mortalskills + t2skills + t3skills
    # allspells is a dictionary {spell_damage_type: [spell list of skill objects], ...}
    allspells = spells.getSpells(dude)
    skilldescriptions = {skill.skill_name: skill.desc for skill in allskills}
    spelldescriptions = {spell.skill_name: spell.desc for type in allspells for spell in allspells[type]}
    descriptions = {**skilldescriptions, **spelldescriptions}
    return render_template(
        'planner.html',
        dude=dude,
        nav=nav,
        mortalskills = mortalskills,
        t2skills = t2skills,
        t3skills = t3skills,
        spells_list = allspells,
        descriptions = descriptions
    )


@app.route('/levelup', methods=['GET'])
def levelup():
    ##dude = session.get('dude')
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set:
        dude = session['dude']
    else:
        uh_oh = 'Something went wrong!'
        print(uh_oh)
        dude = character.Character('dude')
    if dude.level != 30:
        print(f'Leveling up {dude.name} from level {dude.level} to {dude.level + 1}...')
        dude.levelup()
    session['dude'] = dude
    result = dude.to_dict2()
    return json.dumps(result)


@app.route('/buyskill', methods=['GET'])
def busykill():
    skill = request.args.get('skill', '', type=str)
    cost = request.args.get('cost', 0, type=int)
    parent = request.args.get('parent', '', type=str)
    skillclass = request.args.get('skillclass', '', type=str)
    print(f'buying a skill maybe? skill: {skill}  cost: {cost}  parent: {parent}  skillclass: {skillclass}')
    ##dude = session.get('dude')
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set:
        dude = session['dude']
    else:
        uh_oh = 'Something went wrong!'
        print(uh_oh)
        dude = character.Character('dude')
    dude_classes = [dude.class_1, dude.class_2, dude.class_3]
    if dude.cp >= cost and skillclass in dude_classes:
        if parent != '':
            dude_skills = dude.listskills()
            result = False
            for skillcheck in dude_skills:
                if skillcheck == parent:
                    dude.skillbuy(skill, cost, parent, skillclass)
                    session['dude'] = dude
                    result = dude.to_dict2()
            if not result:
                failure = f'You do not know the parent skill required to purchase this skill!'
                print(failure)
                result = ['Failure', failure]
        else:
            dude.skillbuy(skill, cost, parent, skillclass)
            session['dude'] = dude
            result = dude.to_dict2()
    else:
        print(f'skillclass: {skillclass}')
        if not skillclass:
            print(f'skillclass is false')
            failure = 'Characters of your alignment cannot learn this spell!\n(note Angels cannot learn Acid spells and Demons cannot learn Electric spells)'
        else:
            print('skillclass is not false?')
            failure = 'You do not have the CP or class required to purchase this skill!'
        print(failure)
        result = ['Failure', failure]
    return json.dumps(result)


@app.route('/updatePane', methods=['GET'])
def updatePane():
    pane = request.args.get('pane', '', type=str)
    spell = request.args.get('spell', '', type=str)
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set:
        dude = session['dude']
        print(f'Updating panes: pane: {pane} | spell: {spell}')
        dude.setPane(pane, spell)
        result = 'success'
    else:
        failure = 'Something went wrong setting the pane state!'
        print(failure)
        result = ['Failure', failure]
    return result
        

@app.route('/grabdata', methods=['GET'])
def grabdata():
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set:
        dude = session['dude']
        result = dude.to_dict2()
    else:
        failure = 'Something went wrong!'
        result = ['Failure', failure];
    return json.dumps(result);


@app.route('/sellskill', methods=['GET'])
def sellskill():
    skill = request.args.get('skill', '', type=str)
    print(f'Selling a skill maybe? skill: {skill}')
    ##dude = session.get('dude')
    dude_set = skillDisplay.key_in('dude', session)
    if dude_set:
        dude = session['dude']
    else:
        uh_oh = 'Something went wrong!'
        print(uh_oh)
        dude = character.Character('dude')
    skillsold = dude.sellskill(skill)
    if skillsold == True:
        session['dude'] = dude
        result = dude.to_dict2()
        return json.dumps(result)
    else:
        result = ['Failure', skillsold];
        return json.dumps(result);


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Standard `contact` form."""
    # form = ContactForm()
    # if form.validate_on_submit():
    #     return redirect(url_for("success"))
    # return render_template(
    #     "contact.jinja2",
    #     nav=nav,
    #     form=form,
    #     title="Contact Us:",
    #     template="form-template"
    # )
    session.pop('dude', None)
    return redirect(url_for('planner', tier2=None, tier3=None, reset=1))


@app.errorhandler(404)
def not_found(thing):
    """Page not found."""
    return make_response(render_template(
        "error.html",
        thing=thing,
        nav=nav
        ), 404)


@app.errorhandler(500)
def broke_stuff(thing):
    """Page broken."""
    return make_response(render_template(
        "error.html",
        thing=thing,
        nav=nav
        ), 500)


@app.route("/api")
def api():
    """
    May someday connect into the Nexus Clash Character API

    Returns:
        [type]: [description]
    """
    if request.method != 'GET':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
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
    return make_response(jsonify(classskills), 200, headers)
