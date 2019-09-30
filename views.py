from route_helper import simple_route
import weapons

GAME_HEADER = """
<head>
  <link rel="stylesheet" href="/static/style.css">
</head>
<h1>Welcome to adventure quest!</h1>
<p><a href = '/inventory/'>Inventory</a></p>
<!--<p>At any time you can <a href='/reset/'>reset</a> your game.</p>-->
"""

#keep for inventory page
"""
<script>
  document.write('<a href="' + document.referrer + '">Go Back</a>');
</script>
"""

character = {
    "name": "",
    "str": 0,
    "hp": 0,
    "hpCurrent": 0,
    "agi": 0,
    "class": None,
    "inventory":[],
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
    :param monsters_name:
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
    
    """.format(where=world['location'], monster_name=world['name'])


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
    """.format(where=world['location'], monster_name=world['name'])
@simple_route('/start/')
def startGame(world:dict)->str:
    world['location'] = "The Hut of Pizza"
    return GAME_HEADER+"""<br>
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
    we'll have to be careful."
    </div>
    <div class="hidden" id="respondNo">
    "Oh," says Boli, "well, then, <a href = "/">bye</a>..."
    </div>
    <script>
        var yesButton = document.getElementById("yesButton");
        var noButton = document.getElementById("noButton");
        
        yesButton.onclick= function(){
            document.getElementById("respondYes").classList.remove("hidden");
            document.getElementById("yesQuote").classList.remove("hidden");
            hideButtons();
        }
        noButton.onclick= function(){
            document.getElementById("respondNo").classList.remove("hidden");
            document.getElementById("noQuote").classList.remove("hidden");
            hideButtons();
        }
        function hideButtons(){
            yesButton.classList.add("hidden");
            noButton.classList.add("hidden");
        }
    </script>
    
    """