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
            "Head": None,
            "Torso": None,
            "Arms": None,
            "Legs": None,
            "MainHand": None,
            "OffHand": None,
            "Ring1": None,
            "Ring2": None,
        }

    #zamiana na słownik
    def to_dict(self):
        return {
            "name": self.name,
            "gold": self.gold,
            "inventory": [item.name for item in self.inventory],
            "statistics": self.statistics,
            "healthMax": self.healthMax,
            "healthCurrent": self.healthCurrent,
            "equipment": {slot: (item.name if item else None) for slot, item in self.equipment.items()},
        }
    

    #ładowanie gracza z save-a
    @classmethod
    def from_save(cls, data):
        from items import ITEM_REGISTRY
        stats = data["statistics"]
        player = cls(
            name=data["name"],
            Strength=stats["Strength"],
            Agility=stats["Agility"],
            Intelligence=stats["Intelligence"],
            Endurance=stats["Endurance"],
        )
        player.gold = data["gold"]
        player.healthMax = data["healthMax"]
        player.healthCurrent = data["healthCurrent"]
        player.inventory = [ITEM_REGISTRY[name] for name in data["inventory"]]
        player.equipment = {
            slot: (ITEM_REGISTRY[name] if name else None)
            for slot, name in data["equipment"].items()
        }
        return player

    def is_alive(self):
        return self.healthCurrent > 0

    def heal(self, amount=None):
        if amount is None:
            self.healthCurrent = self.healthMax
        else:
            self.healthCurrent = min(self.healthMax, self.healthCurrent + amount)
