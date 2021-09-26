

import threading
from domain.order import FoodItem
from domain.food_item import FoodItem, FoodItemState
import config
import datetime
import time

class Cook:
    def __init__(self, kitchen, rank=2, proficiency=2, name="Anonymous", catch_phrase="Don't"):
        self.rank = rank    
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase
        self.kitchen = kitchen
        self.food_to_prepare = []

    
    def start_working(self, apparatus_collection):
        while True:
            if not self.is_available():
                continue

            for order in self.kitchen.order_list:
                for i, food_item in enumerate(order.food_items):
                    if food_item.state == FoodItemState.NOT_DISTRIBUTED and self.is_apparatus_available(food_item, apparatus_collection):
                        order.items_processed[i] = True
                        threading.Thread(target=self.prepare_food_item, args=(food_item, apparatus_collection)).start() ###()


    def prepare_food_item(self, food_item: FoodItem):
        food_item.state = FoodItemState.IN_PREPARATION
        time.sleep(food_item.preparation_time * config.TIME_UNITS)
        food_item.state = FoodItemState.PREPARED


    def is_available(self):
        return self.proficiency < len(self.food_to_prepare)

    
    def is_apparatus_available(self,  food_item, apparatus_collection):
        if not food_item.apparatus:
            return True

        for apparatus in apparatus_collection[food_item.apparatus]:
            if apparatus.is_free:
                apparatus.is_free = False

                return True
        
        return False

