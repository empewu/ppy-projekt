class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return self.name

#mikstury i inne przedmioty jednorazowe
class Consumable(Item):
    def __init__(self, name, description, value, effect, amount):
        super().__init__(name, description, value)
        # effect: "heal" (anywhere) or "damage_buff"/"defence_buff" (combat only).
        self.effect = effect
        self.amount = amount
    
class Equipment(Item):
    def __init__(self, name, description, value, slot, attribute_required = None, attribute_amount = 0):
        super().__init__(name, description, value)
        self.slot = slot
        self.attribute_required = attribute_required
        self.attribute_amount = attribute_amount

#zbroje
class Armour(Equipment):
    def __init__(self, name, description, value, defence, slot, **kwargs):
        super().__init__(name, description, value, slot, **kwargs)
        self.defence = defence

class HeadArmour(Armour):
    def __init__(self, name, description, value, defence, **kwargs):
        super().__init__(name, description, value, defence, slot="Head", **kwargs)

class TorsoArmour(Armour):
    def __init__(self, name, description, value, defence, **kwargs):
        super().__init__(name, description, value, defence, slot="Torso", **kwargs)

class ArmsArmour(Armour):
    def __init__(self, name, description, value, defence, **kwargs):
        super().__init__(name, description, value, defence, slot="Arms", **kwargs)

class LegsArmour(Armour):
    def __init__(self, name, description, value, defence, **kwargs):
        super().__init__(name, description, value, defence, slot="Legs", **kwargs)


#bronie, mainhand i offhand
class Weapon(Equipment):
    def __init__(self, name, description, value, damage, defence, slot,
                 damage_type=None, governing_stat=None, **kwargs):
        super().__init__(name, description, value, slot, **kwargs)
        self.damage = damage
        self.defence = defence
        # damage_type: "melee" / "ranged" / "magic" (None for non-damaging gear).
        # governing_stat: the attribute that scales this weapon's damage
        # (None = flat damage that does not scale, e.g. a talisman).
        self.damage_type = damage_type
        self.governing_stat = governing_stat
    
class MainHand(Weapon):
    def __init__(self, name, description, value, damage, defence, **kwargs):
        super().__init__(name, description, value, damage, defence, slot="MainHand", **kwargs)

class OffHand(Weapon):
    def __init__(self, name, description, value, damage, defence, **kwargs):
        super().__init__(name, description, value, damage, defence, slot="OffHand", **kwargs)


#pierscienie
class Ring(Equipment):
    def __init__(self, name, description, value, attribute_gained, attribute_value, **kwargs):
        super().__init__(name, description, value, slot="Ring", **kwargs)
        self.attribute_gained = attribute_gained
        self.attribute_value = attribute_value
