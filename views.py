from route_helper import simple_route
import weapons
import enemies

GAME_HEADER = """
<head>
  <link rel="stylesheet" href="/static/style.css">
</head>
<h1>Welcome to adventure quest!</h1>
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

@simple_route('/')
def hello(world: dict) -> str:
    """
    The welcome screen for the game.

    :param world: The current world
    :return: The HTML to show the player
    """
    return GAME_HEADER+"""Hello, and welcome to _____<br>
    
    What is your name?
    <form action="/save/name/">
        <input type="text" name="playerName"><br>
        <input type="submit" value="Submit"><br>
    </form>
"""


ENCOUNTER_MONSTER = """
<!-- Curly braces let us inject values into the string -->
You are in {}. You found a monster!<br>

<!-- Image taken from site that generates random Corgi pictures-->
<img src="http://placecorgi.com/260/180" /><br>
    
What is its name?

<!-- Form allows you to have more text entry -->    
<form action="/save/name/">
    <input type="text" name="name"><br>
    <input type="submit" value="Submit"><br>
</form>
"""
#

@simple_route('/goto/<where>/')
def open_door(world: dict, where: str) -> str:
    """
    Update the player location and encounter a monster, prompting the player
    to give them a name.

    :param world: The current world
    :param where: The new location to move to
    :return: The HTML to show the player
    """
    world['location'] = where
    return GAME_HEADER+ENCOUNTER_MONSTER.format(where)


@simple_route("/save/name/")
def save_name(world: dict, name: str) -> str:
    """
    Update the player name

    :param world: The current world
    :param name: The player/character's name
    :return:
    """
    character['name'] = name

    """
    classes:
    
        rogue:7,5,9
        brute?:7,9,5
        knight:9,7,5
    """

    return GAME_HEADER+"""Well, """+character["name"]+""", ready to pick a class?
    <br><br>
    str is <span style = 'color:red'>strength</span><br>
    hp is <span style = 'color:blue'>health</span><br>
    agi is <span style = 'color:green'>agility</span><br><br>
    
    Knight: 9 str, 7 hp, 5 agi<br>
    Brute: 7 str, 9 hp, 5 agi<br>
    Rogue: 7 str, 5 hp, 9 agi<br><br>
    
    
    <form action="/save/class/">
        <input type="submit" name="classChoice" value="Knight"><br>
        <input type="submit" name="classChoice" value="Brute"><br>
        <input type="submit" name="classChoice" value="Rogue"><br>

    </form>
    
    """


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

    return GAME_HEADER + """Congrats """ + character["name"] + """ you are a """+classChoice+"""
    <br><br>   
    Ready to <a href = '/start'>start</a>?
    """

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
    return """<head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <h1>Welcome to adventure quest!</h1>"""+"""
        <span class="hidden" id="weapons">{weapon_list}</span>
        <span class="hidden" id="items">{item_list}</span>
        <span class="hidden" id="equipped">{equip}</span>
        <br>
        <h4 id="equip"></h4>
        <br>
        <div class="dropdown">
            <button id="dropdownButton"></button>
            <div class="dropdownList">
                <form action="/inventory/" id="dropdownList">
                </form>
            </div>
        </div>
        <br>
        <a href = "" id="goBack">Back</a>
        <script type="text/javascript" src="/static/inventory.js"></script>
    """.format(weapon_list=hidden_weapons, item_list=hidden_items, equip=hidden_stats)

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
    return GAME_HEADER+"""<br>
    <h3>{where}</h3>
    
    <br>
    <span class="typing">
    You find yourself in the Hut of Pizza, a small run-down shack
    <br>
    The owner, Tom Boli, comes up to you: "Interested in an adventure?" he asks.
    </span>
    <br>
    <button type="button" id="yesButton" class = "listedButtons">Yes</button><br>
    <button type="button" id="noButton" class = "listedButtons">No</button>
    
    <p id = "yesQuote" class = "hidden">"Yes"</p>
    <p id = "noQuote" class = "hidden">"No"</p>
    
    <div class="hidden" id="respondYes">
    "Alright.  We're going to bring down Pizzaroni Toni," Boli explains, "Toni has stolen my business and destroyed all 
    other pizza business in town apart from the Hut of Pizza and his own.  I know he's hiding some demonic secret, so 
    we'll have to be careful.  <a href = '/game/mansion_front'>Let's go.</a>"
    </div>
    <div class="hidden" id="respondNo">
    "Oh," says Boli, "well, then, <a href = "/">bye</a>..."
    </div>
    <script type="text/javascript" src="/static/start.js"></script>
    """.format(where=world["location"])

@simple_route("/game/mansion_front/")
def game_mansion_front(world: dict)->str:
    world["location"] = "Pizzaroni Toni's Mansion Front"
    return GAME_HEADER+"""
    <br>
    <h3>{where}</h3>
    <br>
    You and Boli arrive at Pizzaroni Toni's Mansion, a dark manor perpetually cloaked in shade, surrounded in a spiked
    fence.  You go up to the door and knock, a murder of crows start to cry out and disperse.  The sound of footsteps 
    steadily get louder, until the door opens and Toni appears.  He is wearing the guise of a huggable man, with a broad
    smile, blue eyes, and jet-black hair.
    <br>
    "Oh, you again," Toni greets Boli, "brought another person to try and kill me?  Well, traveler, this isn't Boli's 
    first time trying to supposedly get his business back.  All the others have, well, that isn't important."
    <br>
    A window on the top floor shatters, and a shrill shriek cries forth.
    <br>
    "Oh!  I suppose I must be going now," Toni excuses himself, and heads back inside.  His frame suddenly shifts to a
    shadowy outline, and he suddenly exudes dark magic.  The door slams shut, but no lock is heard clicking.
    <br><a href = "/game/mansion_entrance/">Enter</a>
    """.format(where=world["location"])

@simple_route("/game/mansion_entrance/")
def game_mansion_entrance(world: dict)->str:
    world["location"] = "Mansion Entrance"
    return GAME_HEADER+"""
    <br>
    <h3>{where}</h3>
    <br>
    Entering the old, dark, building you find a desk with a weird engraving on it.
    <br>
    <img src="/static/symbol.png" alt="Symbol" width="100" height="100">
    <br>
    The person behind the desk reveals herself as Domino, an up-and-coming pizza artist and rapper.
    <br>
    Domino explains that she hates her dad, Pizzaroni Toni, and wants to see him defeated.
    <br>
    "While I can't help you directly, I won't stop you from progressing," she lets up.  "Start by 
    <a href="/game/spider_room">going through that door</a>."
    """.format(where=world["location"])

@simple_route("/game/spider_room/")
def game_spider_room(world: dict)->str:
    world["location"] = "Spider Room"
    world["enemy"] = enemies.spider.get_name()

    return GAME_HEADER+"""
    <br>
    {where}
    <div class="hidden" id="charAGI">{agi}</div>
    <div class="hidden" id="charHP">{hp}</div>
    <br>
    Through the door you see a sleeping {enemy}.  It is lying in the center of a huge web, and will likely wake up if 
    you try to sneak past it.
    <br>
    <button id="attack">Attack</button>
    <button id="sneak">Try and sneak around</button>
    
    <div class="hidden" id="attackDiv">
    <a href="/battle/spider/">Battle!</a>
    </div>
    
    <div class="hidden" id="sneakDiv">
    You somehow manage to sneak past the {enemy}.<br>
    <a href="/game/checkpoint1/">Next Room</a>
    </div>
    
    <div class="hidden" id="okSneakDiv">
    You don't quite sneak past the {enemy}, but you do manage to damage it before you have to 
    <a href="/battle/spiderd/">Battle!</a>
    </div>
    
    <div class="hidden" id="badSneakDiv">
    You fail to sneak past the {enemy}, so now you have to <a href="/battle/spider/">Battle!</a>
    </div>
    
    
    <script type="text/javascript" src="/static/spiderRoom.js"></script>
    """.format(where=world["location"],enemy=world["enemy"],agi=character["agi"],hp=character["hp"])

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
        return "/game/checkpoint1/?get=spideregg"
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
    return GAME_HEADER+"""
    
    <div class="hidden" id="charAGI">{agi}</div>
    <div class="hidden" id="charHP">{hp}</div>
    <div class="hidden" id="charSTR">{str}</div>
    <div class="hidden" id="charWepSTR">{wepSTR}</div>
    <div class="hidden" id="charWepACC">{wepACC}</div>
    <div class="hidden" id="enemyName">{enemyName}</div>
    <div class="hidden" id="enemyHP">{enemyHP}</div>
    <div class="hidden" id="currentEnemyHP">{currentEnemyHP}</div>
    <div class="hidden" id="enemySTR">{enemySTR}</div>
    <div class="hidden" id="enemySPD">{enemySPD}</div>
    
    <div id="enemyStatus">
    {currentEnemyHP} / {enemyHP}
    </div>
    <br><br>
    <div id="charStatus">    
    {hp} / {hp}
    </div>
    <button id="attackButton">Attack</button>
    <button id="healButton">Heal</button>
    <button id="waitButton">Wait</button>
    <br>
    <div class="hidden" id="nextRoomDiv"><a href = "{nextRoom}">Continue On</div>
    <br>
    <div id="combatLog"></div>
    <br>
    <div class="hidden" id="retry"><button onClick="window.location.reload();">Retry</button></div>
    
    
    
    <script type="text/javascript" src="/static/fight.js"></script>
    """.format(agi=character['agi'],hp=character['hp'],str=character['str'],wepSTR=character['weapon'].get_modifier(),
               wepACC=character['weapon'].get_accuracy(),enemyName=current_enemy.get_name(),
               enemyHP=current_enemy.get_max_hp(),currentEnemyHP=current_enemy.hp_current,
               enemySTR=current_enemy.get_damage(),enemySPD=current_enemy.get_spd(),nextRoom=next_room)