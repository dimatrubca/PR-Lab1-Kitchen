from domain.order import Order

def request_order_to_order(request_order):
    print("r order=", request_order)
    order_id = request_order['order_id']
    table_id = request_order['table_id']
    waiter_id = request_order['waiter_id']
    items = request_order['items']
    priority = request_order['priority']
    max_wait = request_order['max_wait']
    pick_up_time = request_order['pick_up_time']

    order = Order(order_id, table_id, waiter_id, items, priority, pick_up_time, max_wait)

    return order