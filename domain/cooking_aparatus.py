

class CookingAparatus:
    def __init__(self) -> None:
        self.is_available = True


class Stove(CookingAparatus):
    def __init__(self) -> None:
        super().__init__()

    
class Oven(CookingAparatus):
    def __init__(self) -> None:
        super().__init__()