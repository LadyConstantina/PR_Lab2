class Restaurant:
    def __init__(self, restaurant_dict):
        self.id = restaurant_dict["restaurant_id"]
        self.name = restaurant_dict["name"]
        self.address = restaurant_dict["address"]
        self.menu = restaurant_dict["menu"]
        self.menu_items = restaurant_dict["menu_items"]
        self.rating = restaurant_dict["rating"]

    def to_dict(self):
        return {
            "name" : self.name,
            "menu_items" : self.menu_items,
            "menu" : self.menu,
            "rating" : self.rating
        }