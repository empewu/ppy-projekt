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
        self.equipment = {
            "Head": 0,
            "Torso": 0,
            "Arms": 0,
            "Legs": 0,
            "MainHand": 0,
            "OffHand": 0,
            "Ring1": 0,
            "Ring2": 0,
        }

    #zamiana na słownik
    def to_dict(self):
        return {
            "name": self.name,
            "gold": self.gold,
            "inventory": self.inventory,
            "statistics": self.statistics,
            "healthMax": self.healthMax,
            "healthCurrent": self.healthCurrent,
            "equipment": self.equipment,
        }
    
    #ładowanie gracza z save-a
    @classmethod
    def from_save(cls, data):
        stats = data["statistics"]
        player = cls(
            name=data["name"],
            Strength=stats["Strength"],
            Agility=stats["Agility"],
            Intelligence=stats["Intelligence"],
            Endurance=stats["Endurance"],
        )
        player.gold = data["gold"]
        player.inventory = data["inventory"]
        player.healthMax = data["healthMax"]
        player.healthCurrent = data["healthCurrent"]
        player.equipment = data["equipment"]
        return player

    def is_alive(self):
        return self.healthCurrent > 0


