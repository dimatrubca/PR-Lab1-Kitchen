from datetime import datetime
import logging
from typing import List
from domain.menu import RestaurantMenu
from domain.order import FoodItem, Order
import threading
import requests
import service
from settings import OVENS, STOVES

import utils
from .cook import Cook
from .cooking_aparatus import CookingAparatus

logger = logging.getLogger(__name__)


class Kitchen():
    def __init__(self, ovens_n=OVENS, stoves_n=STOVES) -> None:
        self.order_list:List[Order] = []
        self.menu:RestaurantMenu = RestaurantMenu()
        self.cooks = utils.read_cooks(self)
        self.cooking_apparatus = {
            "oven": [CookingAparatus("oven") for i in range(ovens_n)],
            "stove": [CookingAparatus("stove") for i in range(stoves_n)] 
        }

        self.order_list_mutex = threading.Lock()
        self.apparatus_mutex = threading.Lock()
        
    


    def run_simulation(self):
        for cook in self.cooks:
            threading.Thread(target=cook.start_working).start() 

        while True:
            finished_orders = False

            for order in self.order_list:
                if order.is_finished():
                    logging.info(f"order {order.order_id} is ready!")

                    finished_orders = True
                    order.cooking_time = datetime.utcnow().timestamp() - order.received_time
                    distribution = utils.order_to_distribution(order)

                    service.send_distribution_request(distribution)

            if finished_orders:
                self.order_list_mutex.acquire()
                self.order_list[:] = [order for order in self.order_list if not order.is_finished()]
                self.order_list_mutex.release()


    def receive_order(self, request_order):
        order_id = request_order['order_id']
        table_id = request_order['table_id']
        waiter_id = request_order['waiter_id']
        items = request_order['items']
        priority = request_order['priority']
        max_wait = request_order['max_wait']
        pick_up_time = request_order['pick_up_time']

        order = Order(order_id, table_id, waiter_id, items, priority, pick_up_time, max_wait, self.menu)

        self.order_list.append(order)


    
