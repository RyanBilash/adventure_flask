class Weapon:
    name:str = "Weapon"
    modifier:float = 1.
    accuracy:float = 1.

    def __init__(self, name:str, modifier:float, accuracy:float):
        self.name = name
        self.modifier = modifier
        self.accuracy = accuracy

sword = Weapon("Sword",1.2,0.9)
axe = Weapon("Axe",1.3,0.75)
dagger = Weapon("Dagger",1.1,.95)
none = Weapon("None",0.85,0.85)

