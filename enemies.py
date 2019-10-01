class Enemy:
    name:str = ""
    hp_max:int = 0
    hp_current:float = 0.
    damage:float = 0

    def __init__(self, name:str,hp_max:int,damage:float):
        self.name = name
        self.hp_max = hp_max
        self.hp_current = hp_max
        self.damage = damage

spider = Enemy("Giant Spider",13,1.2)
skeleton = Enemy("Sans",7,1.5)
golem = Enemy("Pizza Golem",20,2)
toni = Enemy("Pizzaroni Toni",50,.5)