class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return self.name
    
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
    def __init__(self, name, description, value, damage, defence, slot):
        super().__init__(name, description, value, slot)
        self.damage = damage
        self.defence = defence
    
class MainHand(Weapon):
    def __init__(self, name, description, value, damage, defence):
        super().__init__(name, description, value, damage, defence, slot="MainHand")

class OffHand(Weapon):
    def __init__(self, name, description, value, damage, defence):
        super().__init__(name, description, value, damage, defence, slot="OffHand")


#pierscienie
class Ring(Equipment):
    def __init__(self, name, description, value, attribute_gained, attribute_value):
        super().__init__(name, description, value, slot="Ring1")
        self.attribute_gained = attribute_gained
        self.attribute_value = attribute_value
