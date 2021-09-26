

import threading
from domain.order import FoodItem
from domain.food_item import FoodItem, FoodItemState
import config
import datetime
import logging
import time

logger = logging.getLogger(__name__)

class Cook:
    def __init__(self, kitchen, id, rank=2, proficiency=2, name="Anonymous", catch_phrase="Don't"):
        self.rank = rank    
        self.proficiency = proficiency
        self.name = name
        self.catch_phrase = catch_phrase
        self.kitchen = kitchen
        self.id = id
        self.cooking_items_cnt = 0

    
    def start_working(self, apparatus_collection):
        while True:
            if not self.is_available():
                continue

            for order in self.kitchen.order_list:
                for i, food_item in enumerate(order.food_items):
                    if food_item.state == FoodItemState.NOT_DISTRIBUTED and self.is_apparatus_available(food_item, apparatus_collection):
                        food_item.state = FoodItemState.IN_PREPARATION
                        threading.Thread(target=self.prepare_food_item, args=(food_item, apparatus_collection)).start() ###()


    def prepare_food_item(self, food_item: FoodItem, apparatus_collection):
        logging.info(f"Cook {self.id} started preparing food item {food_item.item_id} from order {food_item.order_id}")

        self.cooking_items_cnt += 1
        food_item.cook_id = self.id
        time.sleep(food_item.preparation_time * config.TIME_UNITS)
        food_item.state = FoodItemState.PREPARED
        self.cooking_items_cnt -= 1

        logging.info(f"Cook {self.id} finished preparing food item {food_item.item_id} from order {food_item.order_id}")


    def is_available(self):
        return self.proficiency > self.cooking_items_cnt
    
    def is_apparatus_available(self,  food_item, apparatus_collection):
        if not food_item.apparatus:
            return True

        for apparatus in apparatus_collection[food_item.apparatus]:
            if apparatus.is_available:
                return True
        
        return False

