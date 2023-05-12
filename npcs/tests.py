from pathlib import Path

import pytest

from .parsers import parse_manage_npc

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


@pytest.fixture
def npc_page() -> bytes:
    return FIXTURES_ROOT.joinpath("npc.html").open("rb").read()


def test_parse_location(npc_page: bytes):
    assert list(parse_manage_npc(npc_page)) == [
        {
            "id": 22438,
            "name": "Rosalie",
            "image": "img/items/a_098.png",
            "likes": [
                "Carrot",
                "Aquamarine",
                "Apple",
                "Purple Flower",
                "Iced Tea",
                "Caterpillar",
                "Apple Cider",
                "Fireworks",
            ],
            "loves": [
                "Gold Carrot",
                "Green Dye",
                "Box of Chocolate 01",
                "Valentines Card",
                "Blue Dye",
                "Red Dye",
                "Purple Dye",
            ],
            "hates": [
                "Worms",
                "Fish Bones",
                "Coal",
                "Old Boot",
                "Iron Cup",
                "Carp",
                "Grubs",
                "Horned Beetle",
                "Fire Ant",
                "Spider",
            ],
        },
        {
            "id": 22439,
            "name": "Holger",
            "image": "img/items/a_028.png",
            "likes": [
                "Largemouth Bass",
                "Peas",
                "Trout",
                "Arrowhead",
                "Bluegill",
                "Carp",
                "Horn",
                "Cheese",
                "Apple Cider",
                "Peach",
                "Mushroom Stew",
            ],
            "loves": ["Potato", "Marlin", "Gold Trout", "Mug of Beer"],
            "hates": ["Worms", "Aquamarine", "Milk", "Valentines Card"],
        },
        {
            "id": 22440,
            "name": "Beatrix",
            "image": "img/items/a_011.png",
            "likes": ["Hops", "Coal", "Bird Egg", "Carbon Sphere", "Hammer", "Oak"],
            "loves": ["Black Powder", "Explosive", "Iced Tea", "Fireworks"],
            "hates": ["Worms", "Grubs", "Horned Beetle", "Fire Ant"],
        },
        {
            "id": 22441,
            "name": "Thomas",
            "image": "img/items/a_048.png",
            "likes": [
                "Drum",
                "Largemouth Bass",
                "Carp",
                "Iced Tea",
                "Minnows",
                "Gummy Worms",
                "Mealworms",
            ],
            "loves": ["Flier", "Fishing Net", "Gold Trout", "Gold Catfish", "Goldgill"],
            "hates": ["Worms", "Eggs", "Leek", "Green Dye"],
        },
        {
            "id": 22442,
            "name": "Cecil",
            "image": "img/items/a_027.png",
            "likes": [
                "Aquamarine",
                "Grapes",
                "Ladder",
                "Snail",
                "Giant Centipede",
                "Slimestone",
            ],
            "loves": [
                "Leather",
                "Old Boot",
                "MIAB",
                "Shiny Beetle",
                "Horned Beetle",
                "Grasshopper",
                "Yarn",
            ],
            "hates": ["Worms", "Feathers", "Mushroom", "Milk"],
        },
        {
            "id": 22443,
            "name": "George",
            "image": "img/items/a_034.png",
            "likes": [
                "Hops",
                "Glass Orb",
                "Orange Juice",
                "Arrowhead",
                "Bird Egg",
                "Mushroom Stew",
            ],
            "loves": ["Hide", "Carbon Sphere", "Spider", "Apple Cider", "Mug of Beer"],
            "hates": ["Worms", "Fish Bones", "Bone", "Cheese"],
        },
        {
            "id": 22444,
            "name": "Jill",
            "image": "img/items/a_024.png",
            "likes": ["Tomato", "Milk", "Old Boot", "Grapes", "Cheese", "Scrap Metal"],
            "loves": ["Yellow Perch", "Mushroom Paste", "Leather", "MIAB", "Peach"],
            "hates": ["Worms", "Hops", "Stingray", "Grubs", "Spider", "Snowball"],
        },
        {
            "id": 22445,
            "name": "Vincent",
            "image": "img/items/a_047.png",
            "likes": [
                "Wooden Box",
                "Apple",
                "Hops",
                "Acorn",
                "Leather Diary",
                "Horn",
                "Cheese",
                "Shovel",
            ],
            "loves": [
                "Mushroom Paste",
                "Orange Juice",
                "Lemonade",
                "Axe",
                "Apple Cider",
                "5 Gold",
                "Onion Soup",
            ],
            "hates": [
                "Worms",
                "Aquamarine",
                "Purple Flower",
                "Purple Parchment",
                "Shrimp",
                "Valentines Card",
            ],
        },
        {
            "id": 22446,
            "name": "Lorn",
            "image": "img/items/a_088.png",
            "likes": [
                "Bucket",
                "Peas",
                "Purple Parchment",
                "Green Parchment",
                "Iron Cup",
                "Iced Tea",
                "3-leaf Clover",
                "Apple Cider",
            ],
            "loves": ["Small Prawn", "Glass Orb", "Milk", "Shrimp", "Gold Peas"],
            "hates": ["Worms", "Crappie", "Old Boot", "Snail", "Spider"],
        },
        {
            "id": 22447,
            "name": "Buddy",
            "image": "img/items/buddy.png",
            "likes": [
                "Bucket",
                "Mushroom",
                "Purple Flower",
                "Bone",
                "Gold Peppers",
                "Gummy Worms",
                "Snail",
                "Giant Centipede",
                "Spider",
            ],
            "loves": [
                "Purple Flower",
                "Pirate Flag",
                "Pirate Bandana",
                "Valentines Card",
            ],
            "hates": [
                "Peppers",
                "Drum",
                "Worms",
                "Crappie",
                "Lemon",
                "Lemonade",
                "Grubs",
                "Snowball",
            ],
        },
        {
            "id": 53900,
            "name": "Borgen",
            "image": "img/items/borgen.png",
            "likes": [
                "Glass Orb",
                "Milk",
                "Gold Carrot",
                "Gold Peas",
                "Gold Cucumber",
                "Slimestone",
            ],
            "loves": [
                "Wooden Box",
                "Ancient Coin",
                "Cheese",
                "Skull Coin",
                "Gold Catfish",
            ],
            "hates": [
                "Worms",
                "Purple Flower",
                "Old Boot",
                "Grubs",
                "Green Dye",
                "Valentines Card",
            ],
        },
        {
            "id": 59421,
            "name": "Ric Ryph",
            "image": "img/items/npc_figure2.png",
            "likes": [
                "Bucket",
                "Green Parchment",
                "Unpolished Shimmer Stone",
                "Coal",
                "Black Powder",
                "Arrowhead",
                "Old Boot",
                "Carbon Sphere",
            ],
            "loves": ["Mushroom Paste", "Hammer", "Shovel", "5 Gold"],
            "hates": [
                "Worms",
                "Aquamarine",
                "Milk",
                "Cheese",
                "Ladder",
                "Caterpillar",
                "Valentines Card",
            ],
        },
        {
            "id": 70604,
            "name": "Mummy",
            "image": "img/items/mummy_t_01.png",
            "likes": ["Fish Bones", "Hammer", "Treat Bag 01", "Treat Bag 02", "Yarn"],
            "loves": ["Bone", "Spider", "Treat Bag 03", "Valentines Card"],
            "hates": [
                "Drum",
                "Worms",
                "Coal",
                "Cheese",
                "Snowball",
                "Box of Chocolate 01",
            ],
        },
        {
            "id": 46158,
            "name": "Star Meerif",
            "image": "img/items/npc_figure.png",
            "likes": ["Eggs", "Feathers"],
            "loves": ["Blue Feathers", "Gold Feather"],
            "hates": [
                "Worms",
                "Lemon",
                "Lemonade",
                "Bone",
                "Iron Cup",
                "Cheese",
                "Grubs",
            ],
        },
        {
            "id": 71760,
            "name": "Charles Horsington III",
            "image": "img/items/npc_horse.png",
            "likes": ["Carrot", "Twine", "3-leaf Clover", "Grasshopper"],
            "loves": [
                "Apple",
                "Gold Carrot",
                "Apple Cider",
                "Box of Chocolate 01",
                "Valentines Card",
                "Peach",
            ],
            "hates": [
                "Worms",
                "Stone",
                "Green Chromis",
                "Blue Crab",
                "Lemon",
                "Lemonade",
                "Bone",
                "Cheese",
                "Grubs",
                "Snail",
                "Spider",
            ],
        },
        {
            "id": 71761,
            "name": "ROOMBA",
            "image": "img/items/robot_02.png",
            "likes": ["Glass Orb", "Hammer", "Scrap Wire"],
            "loves": ["Carbon Sphere", "Scrap Metal"],
            "hates": [
                "Worms",
                "Milk",
                "Acorn",
                "Arrowhead",
                "Bird Egg",
                "3-leaf Clover",
                "Snowball",
            ],
        },
        {
            "id": 71805,
            "name": "Captain Thomas",
            "image": "img/items/MustacheTom96.png",
            "likes": ["Blue Crab", "Minnows"],
            "loves": [
                "Fishing Net",
                "Gold Trout",
                "Gold Catfish",
                "Gold Drum",
                "Large Net",
            ],
            "hates": ["Worms", "Radish", "Spider"],
        },
        {
            "id": 84518,
            "name": "frank",
            "image": "img/items/npc_bunny1.png",
            "likes": [
                "Bucket",
                "Feathers",
                "Blue Feathers",
                "Caterpillar",
                "Grasshopper",
                "Blue Dye",
            ],
            "loves": ["Carrot", "Cabbage", "Gold Carrot"],
            "hates": ["Worms", "Eggs", "Peas", "Mushroom", "Trout", "Fire Ant"],
        },
        {
            "id": 89577,
            "name": "Santa",
            "image": "img/items/lornsanta.png",
            "likes": ["Milk", "Snowball"],
            "loves": [
                "Dasher",
                "Dancer",
                "Prancer",
                "Vixen",
                "Comet",
                "Cupid",
                "Donner",
                "Blitzen",
            ],
            "hates": ["Worms", "Coal", "Spider"],
        },
        {
            "id": 125512,
            "name": "Leafy McLucky",
            "image": "img/items/buddyl.png",
            "likes": ["Green Parchment", "3-leaf Clover", "Green Dye"],
            "loves": ["4-leaf Clover", "5 Gold"],
            "hates": ["Worms", "Apple"],
        },
        {
            "id": 154722,
            "name": "Ragvin",
            "image": "img/items/ragvin.png?1",
            "likes": ["Orange", "Pirate Bandana"],
            "loves": ["Marlin", "Ancient Coin"],
            "hates": ["Worms", "Mushroom"],
        },
        {
            "id": 172470,
            "name": "FR4NK",
            "image": "img/items/robot_05.png",
            "likes": [],
            "loves": [],
            "hates": ["Worms"],
        },
        {
            "id": 178572,
            "name": "Mariya",
            "image": "img/items/chef.png",
            "likes": [
                "Eggplant",
                "Eggs",
                "Cucumber",
                "Radish",
                "Milk",
                "Iced Tea",
                "Peach",
            ],
            "loves": [
                "Leather Diary",
                "Mushroom Stew",
                "Onion Soup",
                "Cat’s Meow",
                "Quandary Chowder",
                "Sea Pincher Special",
                "Shrimp-a-Plenty",
                "Over The Moon",
            ],
            "hates": ["Worms", "Black Powder", "Explosive", "Spider"],
        },
        {
            "id": 188036,
            "name": "Ghorgen",
            "image": "img/items/ghorgen.png",
            "likes": [],
            "loves": [],
            "hates": [],
        },
        {
            "id": 231545,
            "name": "Captain Logan",
            "image": "img/items/captainlogan.png",
            "likes": [],
            "loves": [],
            "hates": [],
        },
        {
            "id": 267531,
            "name": "Baba Gec",
            "image": "img/items/merchant.png",
            "likes": [],
            "loves": [],
            "hates": [],
        },
    ]
