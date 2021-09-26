
import enum
from domain import kitchen

class FoodItemState(enum.Enum):
    NOT_DISTRIBUTED = 1,
    IN_PREPARATION = 2,
    PREPARED = 3


class FoodItem:
    def __init__(self, order_id, item_id, preparation_time) -> None:
        self.order_id = order_id
        self.item_id = item_id
        self.estimated_preparation_time = None
        self.preparation_time = preparation_time
        self.state:FoodItemState = FoodItemState.NOT_DISTRIBUTED
        self.cook_id = None