# tests/test_navigation.py
from PC.brain.navigation_map import NavigationMap

nav = NavigationMap()

def test_find_by_room_id():
    result = nav.find("1.47")
    assert result is not None
    assert result["name"] == "Lab 1.47"

def test_find_by_alias():
    result = nav.find("lab 1.47")
    assert result is not None

def test_unknown_room():
    result = nav.find("9.99")
    assert result is None

def test_path_returned():
    result = nav.find("1.47")
    assert isinstance(result["path"], list)
    assert len(result["path"]) > 0

# def test_rfid_lookup():
#     result = nav.locate_by_rfid("A3:FF:12:09")
#     assert result["room_id"] == "1.47"