from pathlib import Path

FIXTURES_ROOT = Path(__file__).joinpath("../fixtures").resolve()


# @pytest.fixture
# def npclevels() -> bytes:
#     return FIXTURES_ROOT.joinpath("npclevels.html").open("rb").read()


# def test_parse_location(npc_page: bytes):
#     data = list(parse_manage_npc(npc_page))
#     assert len(data) == 29
#     assert data[0] == {
#         "id": 22438,
#         "name": "Rosalie",
#         "image": "img/items/a_098.png",
#         "can_send": [],
#         "likes": [
#             "Carrot",
#             "Aquamarine",
#             "Apple",
#             "Purple Flower",
#             "Iced Tea",
#             "Caterpillar",
#             "Apple Cider",
#             "Fireworks",
#         ],
#         "loves": [
#             "Gold Carrot",
#             "Green Dye",
#             "Box of Chocolate 01",
#             "Valentines Card",
#             "Blue Dye",
#             "Red Dye",
#             "Purple Dye",
#         ],
#         "hates": [
#             "Worms",
#             "Fish Bones",
#             "Coal",
#             "Old Boot",
#             "Iron Cup",
#             "Carp",
#             "Grubs",
#             "Horned Beetle",
#             "Fire Ant",
#             "Spider",
#         ],
#     }
#     assert data[1] == {
#         "id": 22439,
#         "name": "Holger",
#         "image": "img/items/a_028.png",
#         "can_send": [],
#         "likes": [
#             "Largemouth Bass",
#             "Peas",
#             "Trout",
#             "Arrowhead",
#             "Bluegill",
#             "Carp",
#             "Horn",
#             "Cheese",
#             "Apple Cider",
#             "Peach",
#             "Mushroom Stew",
#         ],
#         "loves": ["Potato", "Marlin", "Gold Trout", "Mug of Beer", "Wooden Table"],
#         "hates": ["Worms", "Aquamarine", "Milk", "Valentines Card"],
#     }
#     assert data[6] == {
#         "id": 22444,
#         "name": "Jill",
#         "image": "img/items/a_024.png",
#         "can_send": ["Corn", "Corn Husk Doll"],
#         "likes": ["Tomato", "Milk", "Old Boot", "Grapes", "Cheese", "Scrap Metal"],
#         "loves": [
#             "Yellow Perch",
#             "Corn",
#             "Mushroom Paste",
#             "Leather",
#             "MIAB",
#             "Peach",
#             "Corn Husk Doll",
#         ],
#         "hates": ["Worms", "Hops", "Stingray", "Grubs", "Spider", "Snowball"],
#     }
