from domain.order import Order

def request_order_to_order(request_order):
    order_id = request_order['order_id']
    table_id = request_order['table_id']
    waiter_id = request_order['waiter_id']
    items = request_order['items']
    priority = request_order['priority']
    max_wait = request_order['max_wait']
    pick_up_time = request_order['pick_up_time']

    order = Order(order_id, table_id, waiter_id, items, priority, pick_up_time, max_wait)

    return order

def order_to_distribution(order: Order):
    distribution = {
        "order_id": order.order_id,
        "table_id": order.table_id,
        "waiter_id": order.waiter_id,
        "items": order.items,
        "priority": order.priority,
        "max_wait": order.max_wait,
        "pick_up_time": order.pick_up_time,
        "cooking_time": order.cooking_time,
        "cooking_details": [{ "food_id": food_item.item_id, "cook_id": food_item.cook_id} for food_item in order.food_items ]
    }

    return distribution