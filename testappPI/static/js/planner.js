(() => {
    'use strict';
    const popin = {
        'Desc': {
            'class': '.description',
            'width': '-410px'
        },
        'Spells': {
            'class': '.spells',
            'width': '-410px'
        }
    }

    window.onload = function(e){
        $.getJSON('/grabdata',
                function(data) {
                    const click = false;
                    const spellsOpen = ($('.spells').css('right')) == '0px' ? true : false;
                    const descOpen = ($('.description').css('right')) == '0px' ? true : false;
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
                    if (data.buildplan !== 0) {
                        buildFromList(data.buildplan);
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
                    const items = Array('level', 'cp', 'spent_cp', 'melee_acc', 'sword_acc', 'hth_acc', 'ehw_acc', 'bow_acc', 'firearm_acc', 'thrown_acc', 'spell_acc', 'melee_dam', 'sword_dam', 'hth_dam', 'death_type', 'bow_dam', 'firearm_dam', 'thrown_dam', 'gen_spell_dam', 'gem_spell_dam', 'hp_max');
                    items.forEach((item) => {
                        if (item.endsWith('_acc')) {
                            document.getElementById(item).innerText = `${data[item]}%`;
                        } else if (item.endsWith('_dam') || item.endsWith('_type')) {
                            document.getElementById(item).innerText = `+${data[item]}`;
                        } else {
                            document.getElementById(item).innerText = data[item];
                        }
                    });
                    let cpGain = 0;
                    if (data['level'] > 19) {
                        cpGain = 30;
                    } else if (data['level'] > 9 && data['level'] < 20) {
                        cpGain = 20;
                    } else {
                        cpGain = 10;
                    }
                    const skill_name = '---Level Up---';
                    const level = data['level'];
                    const cp_change = 'gain';
                    const cp_string = cpString(cp_change, cpGain)
                    const row_id = rowID(level, skill_name, cp_string)
                    addRow(row_id);
                    refreshSkillDraw(data);
                    updateSkills(data);
            });
            return false;
        });
    });
    
    $(function() {
        $('.skillbuy').on('click', function(e) {
            e.preventDefault()
            let skillinq = document.getElementById(e.target.id);
            let page_action = null;
            const skill_owned = skillinq.checked;
            const buy_args = e.target.value.split(', ');
            if (buy_args[2] === "''") {
                buy_args[2] = '';
            }
            let curr_level = parseInt(document.querySelector('#level').innerText);
            const skill_name = buy_args[0];
            const skill_cost = parseInt(buy_args[1]);
            const costString = cpString('spend', skill_cost);
            if (!skill_owned) {
                page_action = '/sellskill';
                const element_name = `${costString}|${skill_name}|`;
                curr_level = parseInt(document.querySelector(`[id^="${element_name}"]`).children[0].innerText);
            } else {
                page_action = '/buyskill';
            }
            const id = rowID(curr_level, skill_name, costString);
            $.getJSON(page_action, {
                skill: skill_name,
                cost: skill_cost,
                parent: buy_args[2],
                skillclass: buy_args[3],
                buildID: id
            }, 
                function(data) {
                    if (data[0] === 'Failure') {
                        alert(data[1]);
                    } else {
                        // Need to get skills and make sure they are checked to accomodate for behind the scences actions where a skill may be bought
                        skillinq.checked = !skillinq.checked;
                        const items = Array('level', 'cp', 'spent_cp', 'melee_acc', 'sword_acc', 'hth_acc', 'ehw_acc', 'bow_acc', 'firearm_acc', 'thrown_acc', 'spell_acc', 'melee_dam', 'sword_dam', 'hth_dam', 'death_type', 'bow_dam', 'firearm_dam', 'thrown_dam', 'gen_spell_dam', 'gem_spell_dam', 'hp_max');
                        items.forEach((item) => {
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
                            addRow(id);
                        } else {
                            document.getElementById(id).remove();
                        }
                    }
                    refreshSkillDraw(data)
            });
            return false;
        });
    });

    function updateSkills(data) {
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
        }
    }

    function buildFromList(buildplan) {
        buildplan.forEach((id) => {
            addRow(id);
        });
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
                return;
            },
            error: function(xhr) {
                return;
            }
        });
    }

    function addRow(id) {
        const vars = idtovars(id);
        const buildplan = document.querySelector('.buildplan');
        const newrow = document.createElement('tr');
        newrow.insertCell(0).innerText = vars[2];
        newrow.insertCell(1).innerText = vars[0];
        newrow.insertCell(2).innerText = vars[1];
        newrow.id = id;
        buildplan.append(newrow);
    }

    function rowID(lvl, skill, cp_string) {
        return `${cp_string}|${skill}|${lvl}`;
    }

    function cpString(change, cp) {
        return (change == 'gain') ? `+${cp}` : `-${cp}`;
    }

    function idtovars(id) {
        return [parseInt(id.split('|')[0]), id.split('|')[1], parseInt(id.split('|')[2])];
    }

})();

