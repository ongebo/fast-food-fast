from fastfoodfast.models import FoodItem, food_items


def test_food_item_creation():
    assert len(food_items) == 0
    item = FoodItem()
    created_item = item.create_food_item('Hamburger', 'set', 5000)
    assert created_item == {'id': 0, 'item': 'Hamburger', 'unit': 'set', 'rate': 5000}
