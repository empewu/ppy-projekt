class Enemy:
    def __init__(self, name, health, damage, defence, loot_table,
                 weakness=None, resistance=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.defence = defence
        #lista tupli (item, chance)
        self.loot_table = loot_table
        # damage types this enemy takes extra / reduced damage from.
        # Either a specific type ("melee"/"ranged"/"magic"), the "physical"
        # shorthand (melee and ranged), or None.
        self.weakness = weakness
        self.resistance = resistance
