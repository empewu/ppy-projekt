from items.base import Item

coinPouch = Item(
    "Coin Pouch",
    "A pouch with coins.",
    value = 20
    )

goldBar = Item(
    "Gold Bar",
    "A bar of gold.",
    value = 100
    )

valuableGem = Item(
    "Gemstone",
    "A valuable gem, maybe.",
    value = 50
    )

monsterParts = Item(
    "Monster Parts",
    "Bones, organs, viscera and the like. Valuable for alchemy and not much else.",
    value = 30
    )

monsterPartsRare = Item(
    "Rare Monster Parts",
    "Venom sacs, silk glands and similar rare organs. Not as common and therefore more valuable.",
    value = 30
    )

monsterPartsMagical = Item(
    "Magical Monster Parts",
    "Slime brains, golem hearts and similar magical 'organs'. Especially valuable.",
    value = 80
    )
