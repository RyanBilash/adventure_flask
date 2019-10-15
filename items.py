class Item:
    name: str = ""
    hp_mod: int = 0
    str_mod: int = 0
    agi_mod: int = 0

    def __init__(self, name: str, hp_mod: int, str_mod: int, agi_mod: int):
        self.name = name
        self.hp_mod = hp_mod
        self.str_mod = str_mod
        self.agi_mod = agi_mod

    def get_name(self) -> str:
        return self.name

    def get_hp_mod(self) -> int:
        return self.hp_mod

    def get_str_mod(self) -> int:
        return self.str_mod

    def get_agi_mod(self) -> int:
        return self.agi_mod

    def get_hidden_details(self) -> str:
        return self.name.replace(" ", "_") + "," + str(self.hp_mod) + "," + str(self.str_mod) + "," + str(self.agi_mod)


frog_and_rat = Item("Frog & Rat", 0, 1, 1)
spider_egg = Item("Spider Egg", 1, 0, 0)
cheese_pebble = Item("Cheese Pebble", 0, 1, 0)

pepper = Item("Pepper", 0, 1, 0)
tomato_sauce = Item("Tomato Sauce", 0, 0, 1)
magic_dough = Item("Magic Dough", 1, 1, 0)
shredded_cheese = Item("Shredded Cheese", 0, 0, 1)
garlic_flakes = Item("Garlic Flakes", 0, 0, 1)

NAI = Item("NAI", -1, -1, -1)

ALL_ITEMS = [frog_and_rat, spider_egg, cheese_pebble, pepper, tomato_sauce, magic_dough, shredded_cheese, garlic_flakes]
END_ITEMS = [pepper, tomato_sauce, magic_dough, shredded_cheese, garlic_flakes]
