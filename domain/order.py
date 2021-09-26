
import datetime
from domain.food_item import FoodItem, FoodItemState
from typing import List
import enum

class Order:
    def __init__(self, order_id, table_id, waiter_id, items, priority, pick_up_time, max_wait) -> None:
        self.order_id = order_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items = items
        self.items_processed = [False] * len(items)
        self.priority = priority
        self.max_wait = max_wait
        self.pick_up_time = pick_up_time
        self.received_time = datetime.datetime.utcnow().timestamp()
        self.prepared_time = None
        self.cooking_time = None
        self.food_items:List[FoodItem] = [FoodItem(order_id, item_id,  1, "stove") for item_id in items]

    
    def is_finished(self):
        for item in self.food_items:
            if item.state != FoodItemState.PREPARED:
                return False

        return True
        
