class Enemy:
    name:str = ""
    hp_max:int = 0
    hp_current:float = 0.
    damage:float = 0
    spd:int = 0

    def __init__(self, name:str,hp_max:int,damage:float,spd:int):
        self.name = name
        self.hp_max = hp_max
        self.hp_current = hp_max
        self.damage = damage
        self.spd = spd
    def get_name(self)->str:
        return self.name
    def get_max_hp(self)->int:
        return self.hp_max
    def get_hp(self)->float:
        return self.hp_current
    def get_damage(self)->float:
        return self.damage
    def get_spd(self)->int:
        return self.spd

spider = Enemy("Giant Spider",13,1.2,10)
skeleton = Enemy("Sans & Hans",7,1.5,10)
golem = Enemy("Pizza Golem",20,2,10)
toni = Enemy("Pizzaroni Toni",50,.5,10)