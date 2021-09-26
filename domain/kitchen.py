from typing import List
from domain.menu import RestaurantMenu
from domain.order import FoodItem, Order
import threading

from .cook import Cook
from .cooking_aparatus import Oven, Stove


class Kitchen():
    def __init__(self, cooks_n = 2, ovens_n = 1, stoves_n=2) -> None:
        self.order_list:List[Order] = []
        self.menu:RestaurantMenu = RestaurantMenu()
        self.cooks = [Cook(self) for i in range(cooks_n)]
        self.cooking_apparatus = {
            "oven": [Oven() for i in range(ovens_n)],
            "stove": [Stove() for i in range(stoves_n)] 
        }


    def run_simulation(self):
        for cook in self.cooks:
            threading.Thread(target=cook.start_working, args=(self.cooking_apparatus,)).start() # lambda?

        while True:
            self.order_list[:] = [order for order in self.order_list if not order.is_finished()]

    def receive_order(self, order: Order):
        self.order_list.append(order)
        
        # for item_id in order.items:
        #     food_item = FoodItem(order_id=order.order_id, item_id=item_id, preparation_time=self.get_preparation_time(item_id))
        #     self.food_items_list.append(food_item)

        return
        

    def get_preparation_time(self, item_id):
        for item in self.menu.foods:
            if item['id'] == item_id:
                return item['preparation-time']
        
        print("get_preparation_time exception")
        return None

    
