from route_helper import simple_route
from flask import request, render_template
import math
import os
import codecs
import weapons
import enemies
import items

character = {
    "name": "",
    "str": 0,
    "hp": 0,
    "hpCurrent": 0,
    "agi": 0,
    "class": None,
    "inventory": [],
    "last_loc": "",
    "weapon": weapons.none
}

checkpoints = {
    "c1": False,
    "c2": False,
    "c3": False,
    "won": False
}


def set_last_loc():
    character['last_loc'] = request.base_url


script_dir = os.path.dirname(__file__)
html_path = "static/html/"


def get_file_text(name: str) -> str:
    path = os.path.join(script_dir, html_path + name)
    file = codecs.open(path, "r", "utf-8")
    to_return = file.read()
    file.close()
    return to_return


@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    world['location'] = "Launch"

    set_last_loc()
    return render_template('launch.html', where=world['location'])


@simple_route("/save/name/")
def save_name(world: dict, name: str) -> str:
    """
    Update the player name

    :param world: The current world
    :param name: The player/character's name
    :return:
    """
    character['name'] = name
    world['location'] = "Save Name"

    set_last_loc()
    return render_template("pickClass.html", name=character["name"], where=world['location'])


@simple_route("/save/class/")
def save_class(world: dict, classChoice: str) -> str:
    """
    Update the player class

    :param world: The current world
    :return:
    """
    character['class'] = classChoice
    world['location'] = "Save Class"
    if(classChoice != ""):
        if (classChoice == "Knight"):
            character["str"] = 9
            character["hp"] = 7
            character["agi"] = 5
            character["weapon"] = weapons.sword
        elif (classChoice == "Brute"):
            character["str"] = 7
            character["hp"] = 9
            character["agi"] = 5
            character["weapon"] = weapons.axe
        elif (classChoice == "Rogue"):
            character["str"] = 7
            character["hp"] = 5
            character["agi"] = 9
            character["weapon"] = weapons.dagger
        else:
            character["str"] = 7
            character["hp"] = 7
            character["agi"] = 7
            character["weapon"] = weapons.none
    character["hpCurrent"] = character["hp"]

    set_last_loc()
    return render_template("classChoice.html", name=character["name"], c=classChoice)


@simple_route("/inventory/")
def inventory(world: dict, equip: str) -> str:
    if (equip != ""):
        for w in weapons.ALL_WEAPONS:
            if (w.get_name() == equip and w in character["inventory"]):
                character["inventory"].append(character["weapon"])
                character["inventory"].remove(w)
                character["weapon"] = w
                break

    hidden_weapons = ""
    hidden_stats = ""
    hidden_items = ""

    world['location'] = "Inventory"

    if (character["weapon"] != None):
        weapons_list = [character['weapon']]

        for item in character["inventory"]:
            if (type(item) == type(weapons.sword)):
                weapons_list.append(item)
            else:
                hidden_items += item.get_hidden_details() + " "
        for weapon in weapons_list:
            hidden_weapons += (weapon.get_name()).replace(" ", "_") + " "

    if (character["class"] is not None):
        current_weapon = character["weapon"]
        hidden_stats = character["name"].replace(" ", "replace_with_space") + " " + character["class"] + " " + \
                       str(character["str"]) + " " + str(character["hp"]) + " " + str(character["agi"])
        if (current_weapon is not None):
            hidden_stats += " " + current_weapon.get_name().replace(" ", "_") + " " + str(
                current_weapon.get_modifier()) + " " + \
                            str(current_weapon.get_accuracy())

    return render_template("inventory.html", weapon_list=hidden_weapons, item_list=hidden_items, equip=hidden_stats,
                       refer=character['last_loc'])


@simple_route('/start/')
def startGame(world: dict) -> str:
    world['location'] = "The Hut of Pizza"

    set_last_loc()
    return render_template("start.html", where=world["location"])


def get_loc_name_file(where: str) -> [str]:
    if (where == "mansion_front"):
        return ["Pizzaroni Toni's Mansion Front", "mansionFront.html"]
    elif (where == "mansion_entrance"):
        return ["Mansion Entrance", "mansionEntrance.html"]
    elif (where == "spider_room"):
        return ["Spider Room", "spiderRoom.html"]
    elif ("skeleton" in where):
        return ["Skeleton Room", "skeletonRoom.html"]
    elif (where == "pizzaThrone"):
        return ["Throne Room", "throneRoom1.html"]
    elif (where == "endRoom"):
        get_win_items()
        return ["Throne Room", "endRoom.html"]
    else:
        return ["start", "start.html"]


@simple_route("/game/<where>/")
def game_where(world: dict, where: str) -> str:
    loc = get_loc_name_file(where)

    world["location"] = loc[0]

    #html = get_file_text(loc[1])
    set_last_loc()
    return render_template(loc[1], where=world["location"], agi=character["agi"], hp=character["hp"],
                                     str=character['str'])


def get_enemy(enemy: str):
    if ("spider" in enemy):
        return enemies.spider
    elif ("skeleton" in enemy):
        if ("y" in enemy and not items.cheese_pebble in character['inventory']):
            character['inventory'].append(items.cheese_pebble)
        return enemies.skeleton
    elif ("golem" in enemy):
        return enemies.golem
    elif ("toni" in enemy):
        return enemies.toni
    else:
        return enemies.get_random_enemy()


def get_next_room(enemy: str) -> str:
    if ("spider" in enemy):
        return "/checkpoint/1y/"
    elif ("skeleton" in enemy):
        return "/checkpoint/2/"
    elif ("golem" in enemy):
        return "/checkpoint/3/"
    elif ("toni" in enemy):
        return "/game/endRoom/"
    else:
        return "/battle/random/"


def get_item_stats() -> [int]:
    stats = [0, 0, 0]
    for item in character['inventory']:
        if (type(item) == type(items.spider_egg)):
            stats[0] += item.get_hp_mod()
            stats[1] += item.get_str_mod()
            stats[2] += item.get_agi_mod()

    return stats


@simple_route("/battle/<enemy>/")
def battle_enemy(world: dict, enemy: str) -> str:
    damage = "y" if (enemy[-1] == "d") else 0
    # enemy = "spider" if ("spider" in enemy) else enemy

    world['location'] = "Battle " + enemy

    tempHTML = ""

    if (enemy != "random"):
        current_enemy = get_enemy(enemy)
        next_room = get_next_room(enemy)
    else:
        current_enemy = enemies.get_random_enemy()
        enemy = current_enemy.get_name()
        next_room = get_next_room(enemy)
        tempHTML += "<p><a href='/credits/'>Credits</a></p>"

    if (damage != 0):
        current_enemy.hp_current = current_enemy.get_max_hp() - character["str"] * character["weapon"]. \
            get_modifier() * character["weapon"].get_accuracy() * 0.25

    item_stats = get_item_stats()

    set_last_loc()

    return render_template("battle.html", credits=tempHTML,agi=character['agi'], hp=character['hp'], str=character['str'],
                                                wepSTR=character['weapon'].get_modifier(),
                                                wepACC=character['weapon'].get_accuracy(),
                                                enemyName=current_enemy.get_name(),
                                                enemyHP=current_enemy.get_max_hp(),
                                                currentEnemyHP=current_enemy.hp_current,
                                                enemySTR=current_enemy.get_damage(), enemySPD=current_enemy.get_spd(),
                                                nextRoom=next_room, itemHP=item_stats[0], itemSTR=item_stats[1],
                                                itemAGI=item_stats[2])


def round_stat(num: float) -> int:
    if (num - math.floor(num) >= 0.5):
        return math.ceil(num)
    else:
        return math.floor(num)


def get_item(item: str) -> items.Item:
    switch = {
        "1y": items.spider_egg,
        "3": weapons.pizza_cutter
    }
    return switch.get(item, items.NAI)


def get_win_items():
    if (not checkpoints['won']):
        checkpoints['won'] = True
        for item in items.END_ITEMS:
            character['inventory'].append(item)


@simple_route("/checkpoint/<num>/")
def checkpoint(world: dict, num):
    temp_html = ""
    item = get_item(num)
    if (item != items.NAI and not item in character['inventory']):
        character['inventory'].append(item)
        temp_html += "\nYou found {}!".format(item.get_name())

    if ("1" in num):
        num = 1
    elif ("2" in num):
        num = 2
    else:
        num = 3

    world['location'] = "Checkpoint " + str(num)

    if (not checkpoints['c' + str(num)]):
        checkpoints['c' + str(num)] = True
        character['agi'] = round_stat(character['agi'] * 1.25)
        character['str'] = round_stat(character['str'] * 1.25)
        character['hp'] = round_stat(character['hp'] * 1.5)
        temp_html += "\nYou leveled up!"

    character['hp_current'] = character['hp']

    file_name = "checkpoint" + str(num) + ".html"

    item_list = ""
    for i in character['inventory']:
        if (type(i) == type(items.NAI)):
            item_list += i.get_hidden_details() + " "

    set_last_loc()

    return render_template(file_name,checkpoint=temp_html, where=world['location'], items=item_list)


@simple_route("/pictureRoom/")
def pictureRoom(world: dict, lost="NONE") -> str:
    world['location'] = "Picture Room"
    tempHTML = ""

    if (lost != "NONE"):
        for item in character['inventory']:
            if (item.get_name().replace(" ", "_") == lost):
                character['inventory'].remove(item)
                tempHTML = "You got a Frog and Rat, but lost your " + item.get_name() + "<br>"

    html = get_file_text("pictureRoom.html")
    set_last_loc()
    return render_template("pictureRoom.html", where=world['location'], prev=tempHTML, stat=character['str'])


@simple_route("/credits/")
def credits(world: dict) -> str:
    set_last_loc()
    return render_template("credits.html")
