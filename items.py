class Item:
    name:str = ""
    hp_mod:int = 0
    str_mod:int = 0
    agi_mod:int = 0

    def __init__(self, name:str,hp_mod:int,str_mod:int,agi_mod:int):
        self.name = name
        self.hp_mod = hp_mod
        self.str_mod = str_mod
        self.agi_mod = agi_mod
    def get_name(self)->str:
        return self.name
    def get_hp_mod(self)->int:
        return self.hp_mod
    def get_str_mod(self)->int:
        return self.str_mod
    def get_agi_mod(self)->int:
        return self.agi_mod


frog_and_rat = Item("Frog & Rat",0,1,1)
spider_egg = Item("Spider Egg",1,0,0)
cheese_pebble = Item("Cheese Pebble",0,1,0)

NAI = Item("NAI",-1,-1,-1)

ALL_ITEMS = [frog_and_rat,spider_egg,cheese_pebble]