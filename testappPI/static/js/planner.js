(() => {
    'use strict';
    const popin = {
        'Desc': {
            'class': '.description',
            'width': '-410px'
        },
        'Spells': {
            'class': '.spells',
            'width': '-470px'
        }
    }

    window.onload = function(e){
        $.getJSON('/grabdata',
                function(data) {
                    const click = false;
                    console.log(data)
                    const spellsOpen = ($('.spells').css('right')) == '0px' ? true : false;
                    const descOpen = ($('.description').css('right')) == '0px' ? true : false;
                    console.log(`spellsOpen: ${spellsOpen} | descOpen: ${descOpen} | data.spellPane: ${data.spellPane} | data.descPane: ${data.descPane}`);
                    if (data.spellPane !== spellsOpen) {
                        toggleMenu('Spells', click);
                        toggleMenu(data.spellPaneSelect, click);
                    }
                    if (data.descPane !== descOpen) {
                        toggleMenu('Desc', click);
                    }
                    if (spellsOpen) {
                        toggleMenu(data.spellPaneSelect, click);
                    }
                    updateSkills(data);
            });
            return false;
    }
    
    document.querySelectorAll('.skilldesc').forEach(skill => {
        skill.addEventListener('mouseover', e => {
            const skillName = skill.firstElementChild.id;
            const skillArea = document.querySelector('.description');
            skillArea.innerHTML = `
            <h2>${skillName}</h2>
            <p>
            ${descs[skillName]}
            </p>
            `;
        });
    });

    /* Menu enable/disable */
    $('.dropdown-toggle').click( (e) => {
        const click = true;
        const target = e.target.id.split('menuTrigger')[1];
        toggleMenu(target, click);
    });

    function toggleMenu(target, click) {
        const spellsOpen = ($('.spells').css('right')) == '0px' ? true : false;
        const descOpen = ($('.description').css('right')) == '0px' ? true : false;
        const curState = {
            'Spells': spellsOpen,
            'Desc': descOpen
        }
        if (target == 'Desc' || target == 'Spells') {
            console.log(`click: ${click} | target: ${target} | curState[target]: ${curState[target]} | class: ${popin[target]['class']} | width: ${popin[target]['width']}`);
            if (curState[target]) {
                    //Menu is visible, so HIDE menu
                $(popin[target]['class']).animate({
                    right: popin[target]['width']
                },800);
            } else {
                    //Menu is hidden, so SHOW menu
                $(popin[target]['class']).animate({
                    right: 0
                },800);
            }
            if (click) {
                updatePane(target, '');
            }
        } else {
            const spelltypes = ['Acid', 'Cold', 'Death', 'Electric', 'Fire', 'Glyph', 'Impact', 'Piercing', 'Slashing', 'Utility'];
            spelltypes.forEach((type) => {
                (type == target)? $(`.spells${type}`).css('display','block') : $(`.spells${type}`).css('display','none');
            });
            if (click) {
                updatePane('', target);
            }
        }
    }

    $(function() {
        $('#levelup').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/levelup',
                function(data) {
                    console.log(data)
                    const items = Array('level', 'cp', 'spent_cp', 'melee_acc', 'sword_acc', 'hth_acc', 'ehw_acc', 'bow_acc', 'firearm_acc', 'thrown_acc', 'spell_acc', 'melee_dam', 'sword_dam', 'hth_dam', 'death_type', 'bow_dam', 'firearm_dam', 'thrown_dam', 'gen_spell_dam', 'gem_spell_dam', 'hp_max');
                    items.forEach((item) => {
                        console.log(`item: ${item}`);
                        if (item.endsWith('_acc')) {
                            document.getElementById(item).innerText = `${data[item]}%`;
                        } else if (item.endsWith('_dam') || item.endsWith('_type')) {
                            document.getElementById(item).innerText = `+${data[item]}`;
                        } else {
                            document.getElementById(item).innerText = data[item];
                        }
                    });
                    if (data['level'] > 19) {
                        const cpGain = 30;
                        addRow(data['level'], cpGain, '---Level Up---', 'gain');
                    } else if (data['level'] > 9 && data['level'] < 20) {
                        const cpGain = 20;
                        addRow(data['level'], cpGain, '---Level Up---', 'gain');
                    } else {
                        const cpGain = 10;
                        addRow(data['level'], cpGain, '---Level Up---', 'gain');
                    }
                    refreshSkillDraw(data);
                    updateSkills(data);
            });
            return false;
        });
    });
    
    $(function() {
        $('.skillbuy').on('click', function(e) {
            e.preventDefault()
            console.log(e.target.id);
            let skillinq = document.getElementById(e.target.id);
            let page_action = null;
            console.log(skillinq);
            const skill_owned = skillinq.checked;
            const buy_args = e.target.value.split(', ');
            if (buy_args[2] === "''") {
                buy_args[2] = '';
            }
            console.log(`skill_owned: ${skill_owned}`);
            if (!skill_owned) {
                page_action = '/sellskill';
            } else {
                page_action = '/buyskill';
            }
            console.log(buy_args);
            console.log(page_action);
            $.getJSON(page_action, {
                skill: buy_args[0],
                cost: parseInt(buy_args[1]),
                parent: buy_args[2],
                skillclass: buy_args[3]
            }, 
                function(data) {
                    console.log(data)
                    if (data[0] === 'Failure') {
                        alert(data[1]);
                    } else {
                        // Need to get skills and make sure they are checked to accomodate for behind the scences actions where a skill may be bought
                        skillinq.checked = !skillinq.checked;
                        const items = Array('level', 'cp', 'spent_cp', 'melee_acc', 'sword_acc', 'hth_acc', 'ehw_acc', 'bow_acc', 'firearm_acc', 'thrown_acc', 'spell_acc', 'melee_dam', 'sword_dam', 'hth_dam', 'death_type', 'bow_dam', 'firearm_dam', 'thrown_dam', 'gen_spell_dam', 'gem_spell_dam', 'hp_max');
                        items.forEach((item) => {
                            console.log(`item: ${item}`);
                            if (item.endsWith('_acc')) {
                                document.getElementById(item).innerText = `${data[item]}%`;
                            } else if (item.endsWith('_dam') || item.endsWith('_type')) {
                                document.getElementById(item).innerText = `+${data[item]}`;
                            } else {
                                document.getElementById(item).innerText = data[item];
                            }
                        });
                        updateSkills(data);
                        if (page_action === '/buyskill') {
                            const change = 'spend';
                            addRow(data['level'], buy_args[1], buy_args[0], change);
                        } else {
                            const change = 'gain';
                            const id = rowID(data['level'], buy_args[0], change);
                            document.getElementById(id).remove();
                        }
                    }
                    refreshSkillDraw(data)
            });
            return false;
        });
    });

    function updateSkills(data) {
        console.dir(data);
        if (data) {
            const tier2 = data.class_2;
            const tier3 = data.class_3;
            const skills = data.skills;
            skills.forEach((skill) => {
                const name = skill.name;
                const skill_class = skill.skill_class;
                const checkBox = document.getElementById(name);
                if (checkBox) {
                    const checkClass = checkBox.value.split(', ')[3];
                    if (checkBox.checked != true && checkClass == skill_class) {
                        checkBox.checked = true;
                    } else {
                        if (checkClass != 'Mortal' && checkClass != skill_class) {
                            checkBox.checked = false;
                        }
                    }
                }
            });
        } else {
            console.log(`Did not recieve data!`);
        }
    }
    
    function refreshSkillDraw(data) {
        const actualT2 = data.class_2;
        const displayedT2 = document.getElementsByClassName('t2skills')[0].childNodes[1].innerText
        if (actualT2 === 'Ex-Paladin' || actualT2 === 'Ex-Shepherd' || actualT2 === 'Ex-Pariah' || actualT2 === 'Ex-Defiler') {
            if (actualT2 != displayedT2) {
                window.location.href = `/planner/${actualT2}/${data.class_3}`;
            }
        }
    }

    function updatePane(pane, selection) {
        $.ajax({
            url: "/updatePane",
            data: {"pane": pane,"spell": selection},
            success: function(response) {
                console.log(`Successfully changed state of ${pane} pane | selection: ${selection}`);
            },
            error: function(xhr) {
                console.log(`A failure has happened setting pane state of ${pane} pane | selection: ${selection}`);
            }
        });
    }

    function addRow(lvl, cp, skill, change) {
        const cpString = (change == 'gain') ? `+${cp}` : `-${cp}`;
        const id = rowID(lvl, skill, change);
        const buildplan = document.querySelector('.buildplan');
        const newrow = document.createElement('tr');
        newrow.insertCell(0).innerText = lvl;
        newrow.insertCell(1).innerText = cpString;
        newrow.insertCell(2).innerText = skill;
        newrow.id = id;
        buildplan.append(newrow);
    }

    function rowID(lvl, skill, change) {
        return (skill == '---Level Up---') ? skill.replace(/\s+/g, '-').toLowerCase() + lvl: skill.replace(/\s+/g, '-').toLowerCase();
    }

})();

