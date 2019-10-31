from route_helper import simple_route
from flask import request, render_template
import math
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

"""
The set_last_loc function sets the last place the player has been, except for the inventory, so that they can leave
the inventory page
"""
def set_last_loc():
    character['last_loc'] = request.base_url

"""
The hello route is the welcome screen for the game

@return
    the rendered template
"""
@simple_route('/')
def hello(world: dict) -> str:
    world['location'] = "Launch"

    set_last_loc()
    return render_template('launch.html', where=world['location'])

"""
The save_name route saves the name of the player and prompts them to choose a class

@args
    name (str) - The chosen name of the player
@return
    the rendered template
"""
@simple_route("/save/name/")
def save_name(world: dict, name: str) -> str:
    character['name'] = name
    world['location'] = "Save Name"

    set_last_loc()
    return render_template("pickClass.html", name=character["name"], where=world['location'])

"""
The save_class route saves the class that the player has chosen

@args
    classChoice (str) - The name of the class the player chose
@return
    the rendered template
"""
@simple_route("/save/class/")
def save_class(world: dict, class_choice: str) -> str:
    character['class'] = class_choice
    world['location'] = "Save Class"
    if (class_choice != ""):
        if (class_choice == "Knight"):
            character["str"] = 9
            character["hp"] = 7
            character["agi"] = 5
            character["weapon"] = weapons.sword
        elif (class_choice == "Brute"):
            character["str"] = 7
            character["hp"] = 9
            character["agi"] = 5
            character["weapon"] = weapons.axe
        elif (class_choice == "Rogue"):
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
    return render_template("classChoice.html", name=character["name"], c=class_choice)

"""
The inventory route shows the player's inventory

@args
    equip (str) - The name of the weapon to attempt to equip
@return   
    the rendered template
"""
@simple_route("/inventory/")
def inventory(world: dict, equip: str) -> str:
    equip_weapon(equip)

    hidden_weapons = get_weapon_info()
    hidden_stats = get_stats()
    hidden_items = get_items_info()

    world['location'] = "Inventory"

    return render_template("inventory.html", weapon_list=hidden_weapons, item_list=hidden_items, equip=hidden_stats,
                           refer=character['last_loc'])


"""
The equip_weapon attempts to equip a weapon to the player

@args
    equip (str) - the name of the weapon to attempt to equip
"""
def equip_weapon(equip:str):
    if (equip != ""):
        for w in weapons.ALL_WEAPONS:
            if (w.get_name() == equip and w in character["inventory"]):
                character["inventory"].append(character["weapon"])
                character["inventory"].remove(w)
                character["weapon"] = w
                break


"""
The get_weapon_info function gets the player's weapon info

@return
    a string of combined hidden weapon details
"""
def get_weapon_info():
    hidden_weapons = ""
    if (character["weapon"] != None):
        weapons_list = [character['weapon']]

        for item in character["inventory"]:
            if (type(item) == type(weapons.sword)):
                weapons_list.append(item)
        for weapon in weapons_list:
            hidden_weapons += (weapon.get_name()).replace(" ", "_") + " "
    return hidden_weapons


"""
The get_stats function gets the player's stats

@return
    a string of combined hidden stat + weapon stat details
"""
def get_stats():
    hidden_stats = ""
    if (character["class"] is not None):
        current_weapon = character["weapon"]
        hidden_stats = character["name"].replace(" ", "replace_with_space") + " " + character["class"] + " " + \
                       str(character["str"]) + " " + str(character["hp"]) + " " + str(character["agi"])
        if (current_weapon is not None):
            hidden_stats += " " + current_weapon.get_name().replace(" ", "_") + " " + str(
                current_weapon.get_modifier()) + " " + \
                            str(current_weapon.get_accuracy())
    return hidden_stats


"""
The get_items_info function gets the hidden info of the player's items

@return
    a string of combined hidden item details
"""
def get_items_info():
    hidden_items = ""
    if (character["weapon"] != None):
        for item in character["inventory"]:
            if (type(item) != type(weapons.sword)):
                hidden_items += item.get_hidden_details() + " "

    return hidden_items


"""
The start_game route starts the game, introducting the player to the story

@return
    the rendered template
"""
@simple_route('/start/')
def startGame(world: dict) -> str:
    world['location'] = "The Hut of Pizza"

    set_last_loc()
    return render_template("start.html", where=world["location"])


"""
The get_loc_name_file function returns the location and html template of the page

@args
    where (str) - The name of the location; the url location
@return
    a new list of a name and html template file
"""
def get_loc_name_file(where: str) -> [str]:
    if (where == "mansion_front"):
        return ["Pizzaroni Toni's Mansion Front", "mansionFront.html"]
    elif (where == "mansion_entrance"):
        return ["Mansion Entrance", "mansionEntrance.html"]
    elif (where == "spider_room"):
        return ["Spider Room", "spiderRoom.html"]
    elif (where == "picture_room"):
        return ["Picture Room", "pictureRoom.html"]
    elif ("skeleton" in where):
        return ["Skeleton Room", "skeletonRoom.html"]
    elif (where == "pizza_throne"):
        return ["Throne Room", "throneRoom1.html"]
    elif (where == "end_room"):
        get_win_items()
        return ["Throne Room", "endRoom.html"]
    else:
        return ["start", "start.html"]


"""
The game_where route is the base location route that sends the player to some page

@args
    *args - unused, only needed for the keys
@return
    the rendered template
"""
@simple_route("/game/<where>/")
def game_where(world: dict, *args, where="") -> str:
    loc = get_loc_name_file(where)

    world["location"] = loc[0]

    temp_html = ""

    lost = request.values.get('lost', "NONE")

    if (lost != "NONE"):
        for item in character['inventory']:
            if (item.get_name().replace(" ", "_") == lost):
                character['inventory'].remove(item)
                temp_html = "You got a Frog and Rat, but lost your " + item.get_name() + "<br>"

    set_last_loc()
    return render_template(loc[1], where=world["location"], agi=character["agi"], hp=character["hp"],
                           str=character['str'], prev=temp_html)


"""
The get_enemy function returns the enemy object based on the given enemy name

@args
    enemy (str) - the name or variation of the name of the enemy
@return
    the enemy object of the given name
"""
def get_enemy(enemy: str):
    if ("spider" in enemy):
        return enemies.spider
    elif ("skeleton" in enemy):
        if ("y" in enemy and items.cheese_pebble not in character['inventory']):
            character['inventory'].append(items.cheese_pebble)
        return enemies.skeleton
    elif ("golem" in enemy):
        return enemies.golem
    elif ("toni" in enemy):
        return enemies.toni
    else:
        return enemies.get_random_enemy()


"""
The get_next_room function returns the url of the page to go to after defeating the enemy

@args
    enemy (str) - the name or the variation of the name of the enemy
@return
    the url of the next page
"""
def get_next_room(enemy: str) -> str:
    if ("spider" in enemy):
        return "/checkpoint/1y/"
    elif ("skeleton" in enemy):
        return "/checkpoint/2/"
    elif ("golem" in enemy):
        return "/checkpoint/3/"
    elif ("toni" in enemy):
        return "/game/end_room/"
    else:
        return "/battle/random/"


"""
The get_item_stats function totals all of the stats from the player's items

@return
    a list of the stat modifiers   
"""
def get_item_stats() -> [int]:
    stats = [0, 0, 0]
    for item in character['inventory']:
        if (type(item) == type(items.spider_egg)):
            stats[0] += item.get_hp_mod()
            stats[1] += item.get_str_mod()
            stats[2] += item.get_agi_mod()

    return stats


"""
The battle_enemy route has the player fight an enemy

@args
    enemy (str) - The name of the enemy with a possible modifier
@return
    the rendered template
"""
@simple_route("/battle/<enemy>/")
def battle_enemy(world: dict, enemy: str) -> str:
    damage = "y" if (enemy[-1] == "d") else 0

    world['location'] = "Battle " + enemy

    temp_html = ""

    if (enemy != "random"):
        current_enemy = get_enemy(enemy)
        next_room = get_next_room(enemy)
    else:
        current_enemy = enemies.get_random_enemy()
        enemy = current_enemy.get_name()
        next_room = get_next_room(enemy)
        temp_html += "<p><a href='/credits/'>Credits</a></p>"

    if (damage != 0):
        current_enemy.hp_current = current_enemy.get_max_hp() - character["str"] * character["weapon"]. \
            get_modifier() * character["weapon"].get_accuracy() * 0.25

    item_stats = get_item_stats()

    set_last_loc()

    return render_template("battle.html", agi=character['agi'], hp=character['hp'],
                           str=character['str'],
                           wepSTR=character['weapon'].get_modifier(),
                           wepACC=character['weapon'].get_accuracy(),
                           enemyName=current_enemy.get_name(),
                           enemyHP=current_enemy.get_max_hp(),
                           currentEnemyHP=current_enemy.hp_current,
                           enemySTR=current_enemy.get_damage(), enemySPD=current_enemy.get_spd(),
                           nextRoom=next_room, itemHP=item_stats[0], itemSTR=item_stats[1],
                           itemAGI=item_stats[2])


"""
The round stat function rounds a float to an int

@args
    num (float) - the float to round
@return
    the float rounded either up or down to the nearest int
"""
def round_stat(num: float) -> int:
    if (num - math.floor(num) >= 0.5):
        return math.ceil(num)
    else:
        return math.floor(num)


"""
The get_item function attempts to return an item based on a possible checkpoint string

@args
    item (str) - the name of the checkpoint to return
@return
    either the item based on the name, or the lack thereof
"""
def get_item(item: str) -> items.Item:
    switch = {
        "1y": items.spider_egg,
        "3": weapons.pizza_cutter
    }
    return switch.get(item, items.NAI)


"""
The get_win_items tries to add the list of end-game items to the player's inventory
"""
def get_win_items():
    if (not checkpoints['won']):
        checkpoints['won'] = True
        for item in items.END_ITEMS:
            character['inventory'].append(item)


"""
The checkpoint route heals the player, typically after a fight, before continuing with the story

@args
    num (str) - the checkpoint number, typically an actual number
@return
    the rendered template
"""
@simple_route("/checkpoint/<num>/")
def checkpoint(world: dict, num):
    temp_html = ""
    item = get_item(num)
    if (item != items.NAI and item not in character['inventory']):
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
            item_list += i.get_name().replace(" ", "_") + " "

    set_last_loc()

    return render_template(file_name, checkpoint=temp_html, where=world['location'], items=item_list)


"""
The credits page shows the credits for the game

@return
    the rendered template
"""
@simple_route("/credits/")
def final_credits(world: dict) -> str:
    set_last_loc()
    world['location'] = "Credits"
    return render_template("credits.html")
