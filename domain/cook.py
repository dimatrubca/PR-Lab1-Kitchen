

import threading

from domain.cooking_aparatus import CookingAparatus
from domain.order import FoodItem
from domain.food_item import FoodItem, FoodItemState
import config
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
        self.foot_items_to_prepare = []

        logger.info(f"Cook created: {self}")

    
    def start_working(self):
        logger.info(f"{self} started working")
        while True:
            if not self.is_available():
                continue #TODO: sleep
            
            food_item, apparatus = self.find_food_item()

            if not food_item:
                continue #TODO: sleep
            else:
                self.cooking_items_cnt += 1
            
      #      print("Sleepping!")

            threading.Thread(target=self.prepare_food_item, args=(food_item, apparatus)).start()


    def find_food_item(self):
        self.kitchen.order_list_mutex.acquire()
        self.kitchen.apparatus_mutex.acquire()

        food_item, apparatus = self.search_order_list()

        if food_item is not None:
            food_item.state = FoodItemState.IN_PREPARATION

            if apparatus:
                apparatus.is_available = False

        self.kitchen.apparatus_mutex.release()
        self.kitchen.order_list_mutex.release()

        return food_item, apparatus


    def search_order_list(self):
        for order in self.kitchen.order_list:
            for food_item in order.food_items:
                if food_item.state == FoodItemState.NOT_DISTRIBUTED and self.matches_rank(food_item):
                    apparatus = None

                    if food_item.apparatus:
                        apparatus = self.find_apparatus(food_item.apparatus)

                        if apparatus is None:
                            continue
                    
                    return food_item, apparatus

        return None, None


    def prepare_food_item(self, food_item: FoodItem, apparatus: CookingAparatus):
        logging.warn(f"Cook {self.id} started preparing food item {food_item.item_id} from order {food_item.order_id}")

        food_item.cook_id = self.id
        time.sleep(food_item.preparation_time * config.TIME_UNITS / 1000)
        food_item.state = FoodItemState.PREPARED

        if apparatus:
            apparatus.is_available = True
        
        self.cooking_items_cnt -= 1

        logging.warn(f"Cook {self.id} finished preparing food item {food_item.item_id} from order {food_item.order_id}")


    def matches_rank(self, order_item: FoodItem):
        return self.proficiency in [order_item.complexity, order_item.complexity - 1]


    def is_available(self):
        return self.proficiency > self.cooking_items_cnt
    

    def find_apparatus(self, apparatus_name):
        for apparatus in self.kitchen.cooking_apparatus[apparatus_name]:
            if apparatus.is_available:
                return apparatus

        return None

    def __str__(self) -> str:
        return f"Cook: name={self.name}, rank={self.rank}, proficiency={self.proficiency}"

