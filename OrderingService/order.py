class Order:
    def __init__(self, order_dict, condition):
        self.restaurant_id = order_dict["restaurant_id"]
        self.items = order_dict["items"]
        self.priority = order_dict["priority"]
        self.max_wait = order_dict["max_wait"]
        self.created_time = order_dict["created_time"]

        self.condition = condition

    def notify(self):
        self.condition.notify()

    def to_v2_order(self):
        return {
            "items" : self.items,
            "priority" : self.priority,
            "max_wait" : self.max_wait,
            "created_time" : self.created_time
        }

    def add_restaurant_response(self, response_dict):
        self.order_id = response_dict["order_id"]
        self.estimated_waiting_time = response_dict["estimated_waiting_time"]
        self.registered_time = response_dict["registered_time"]

    def add_restaurant_details(self, restaurant):
        self.restaurant_address = restaurant.address

    def response_to_order(self):
        return {
            "restaurant_id" : self.restaurant_id,
            "restaurant_address" : self.restaurant_address,
            "order_id" : self.order_id,
            "estimated_waiting_time" : self.estimated_waiting_time,
            "created_time" : self.created_time,
            "registered_time" : self.registered_time
        }