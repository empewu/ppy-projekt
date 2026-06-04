class Enemy:
    def __init__(self, name, health, damage, defence, loot_table):
        self.name = name
        self.health = health
        self.damage = damage
        self.defence = defence
        #lista tupli (item, chance)
        self.loot_table = loot_table