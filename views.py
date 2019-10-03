from route_helper import simple_route
import math

import weapons
import enemies

GAME_HEADER = """
<head>
  <link rel="stylesheet" href="/static/style.css">
</head>
<h1>Pizzaroni Toni’s Cheesy Crypt</h1>
<p><a href = '/inventory/?equip='>Inventory</a></p>
<!--<p>At any time you can <a href='/reset/'>reset</a> your game.</p>-->
"""

character = {
    "name": "",
    "str": 0,
    "hp": 0,
    "hpCurrent": 0,
    "agi": 0,
    "class": None,
    "inventory": [],
    "weapon": None
}
checkpoints = {
    "c1":False,
    "c2":False,
    "c3":False
}

def get_file_text(name:str)->str:
    file = open(name,"r")
    toReturn = file.read()
    file.close()
    return toReturn

@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    html = get_file_text("launch.html")
    return GAME_HEADER+html

@simple_route("/save/name/")
def save_name(world: dict, name: str) -> str:
    """
    Update the player name

    :param world: The current world
    :param name: The player/character's name
    :return:
    """
    character['name'] = name

    html = get_file_text("pickClass.html")

    return GAME_HEADER+html.format(name=character["name"])


@simple_route("/save/class/")
def save_class(world: dict, classChoice: str) -> str:
    """
    Update the player name

    :param world: The current world
    :param monsters_name:
    :return:
    """
    character['class'] = classChoice

    if(classChoice == "Knight"):
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
    character["hpCurrent"]=character["hp"]

    html = get_file_text("classChoice.html")

    return GAME_HEADER + html.format(name=character["name"],c=character["class"])

@simple_route("/inventory/")
def inventory(world:dict, equip:str)->str:
    if(equip!=""):
        for w in weapons.ALL_WEAPONS:
            if(w.get_name()==equip and w in character["inventory"]):
                character["inventory"].append(character["weapon"])
                character["inventory"].remove(w)
                character["weapon"] = w
                break

    hidden_weapons = ""
    hidden_stats = ""
    hidden_items = ""

    if(character["weapon"]!=None):
        weapons_list = [character['weapon']]

        for item in character["inventory"]:
            if (type(item) == type(weapons.sword)):
                weapons_list.append(item)
            else:
                hidden_items+=item.get_name().replace(" ","_")+" "
        for weapon in weapons_list:
            hidden_weapons+=(weapon.get_name()).replace(" ","_")+" "

    if(character["class"]!=None):
        current_weapon = character["weapon"]
        hidden_stats = character["name"].replace(" ","replace_with_space")+" "+character["class"]+" "+\
                       str(character["str"])+" "+str(character["hp"])+" "+str(character["agi"])
        if(current_weapon!=None):
            hidden_stats+=" "+current_weapon.get_name().replace(" ","_")+" "+str(current_weapon.get_modifier())+" "+\
                          str(current_weapon.get_accuracy())

    html = get_file_text("inventory.html")
    return html.format(weapon_list=hidden_weapons, item_list=hidden_items, equip=hidden_stats)

'''
<form method=post action="/cgibin/example.cgi">  
<center> Select an option:<select> 
<option>option 1</option> 
<option selected>option 2</option> 
<option>option 3</option>  
</form>  
'''

@simple_route('/start/')
def startGame(world:dict)->str:
    world['location'] = "The Hut of Pizza"

    html = get_file_text("start.html")
    return GAME_HEADER+html.format(where=world["location"])

def get_loc_name_file(where:str)->[str]:
    if(where=="mansion_front"):
        return ["Pizzaroni Toni's Mansion Front","mansionFront.html"]
    elif(where=="mansion_entrance"):
        return ["Mansion Entrance","mansionEntrance.html"]
    elif(where=="spider_room"):
        return ["Spider Room","spiderRoom.html"]
    else:
        return ["start","start.html"]

@simple_route("/game/<where>/")
def game_where(world: dict,where:str)->str:

    loc = get_loc_name_file(where)

    world["location"] = loc[0]

    html = get_file_text(loc[1])
    return GAME_HEADER+html.format(where=world["location"],agi=character["agi"],hp=character["hp"],str=character['str'])

def get_enemy(enemy:str):
    if(enemy=="spider"):
        return enemies.spider
    elif(enemy=="skeleton"):
        return enemies.skeleton
    elif(enemy=="golem"):
        return enemies.golem
    else:
        return enemies.toni
def get_next_room(enemy:str)->str:
    if(enemy=="spider"):
        return "/checkpoint1/?get=spideregg"
    elif(enemy=="skeleton"):
        return enemies.skeleton
    elif(enemy=="golem"):
        return enemies.golem
    else:
        return enemies.toni

@simple_route("/battle/<enemy>/")
def battle_enemy(world: dict, enemy:str)->str:
    damage = "y" if(enemy[-1]=="d") else 0
    enemy = "spider" if("spider" in enemy) else enemy
    current_enemy = get_enemy(enemy)
    next_room = get_next_room(enemy)
    if(damage!=0):
        current_enemy.hp_current = current_enemy.get_max_hp()-character["str"]*character["weapon"].get_modifier()*\
                                   character["weapon"].get_accuracy()*0.25
    html = get_file_text("battle.html")

    return GAME_HEADER+html.format(agi=character['agi'],hp=character['hp'],str=character['str'],wepSTR=character['weapon'].get_modifier(),
               wepACC=character['weapon'].get_accuracy(),enemyName=current_enemy.get_name(),
               enemyHP=current_enemy.get_max_hp(),currentEnemyHP=current_enemy.hp_current,
               enemySTR=current_enemy.get_damage(),enemySPD=current_enemy.get_spd(),nextRoom=next_room)

def round_stat(num:float)->int:
    if(num-math.floor(num)>=0.5):
        return math.ceil(num)
    else:
        return math.floor(num)

def get_item_name(item:str)->str:
    switch = {
        "spideregg":"Spider Egg"
    }
    return switch.get(item,"DNE")

@simple_route("/checkpoint<num>/")
def checkpoint(world:dict,num, get=""):
    html = ""
    item_name = get_item_name(get)
    if(item_name!="DNE" and not item_name in character['inventory']):
        character['inventory'].append(item_name)
        html+="<br>You found {}!".format(item_name)
    if(not checkpoints['c1']):
        checkpoints['c1'] = True
        character['agi'] = round_stat(character['agi']*1.25)
        character['str'] = round_stat(character['str'] * 1.25)
        character['hp'] = round_stat(character['hp'] * 1.5)
        html+="<br>You leveled up!"
    character['hp_current']=character['hp']

    html+=get_file_text("checkpoint"+str(num)+".html")

    return GAME_HEADER+html






