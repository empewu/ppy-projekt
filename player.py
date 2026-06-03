class Player:
    def __init__(self, name, Strength, Agility, Intelligence, Endurance):
        self.name = name
        self.gold = 0
        self.inventory = []
        self.statistics = {
            "Strength": Strength,
            "Agility": Agility,
            "Intelligence": Intelligence,
            "Endurance": Endurance,
        }
        self.healthMax = Endurance * 5
        self.healthCurrent = self.healthMax

    def is_alive(self):
        return self.health > 0


