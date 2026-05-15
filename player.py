# player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.health > 0

    def show_stats(self):
        print(f"\n--- {self.name} ---")
        print(f"HP: {self.health}")
        print(f"Gold: {self.gold}")
    
    def create(self):
        choice = input("> ").strip()
    
