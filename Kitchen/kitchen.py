import threading
import time
import requests
import random
from queue import PriorityQueue 

class Dish:
    def __init__(self, dish_dict):
        self.id = dish_dict["id"]
        self.name = dish_dict["name"]
        self.preparation_time = dish_dict["preparation-time"]
        self.complexity = dish_dict["complexity"]
        self.cooking_apparatus = dish_dict["cooking-apparatus"]

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return False



class Kitchen:
    def __init__(self, n_cooks, menu):
        self.n_cooks = n_cooks
        self.menu = menu
        self.foods_queue = PriorityQueue()
        self.foods_queue_lock = threading.Lock()
        self.order_list = []
        self.order_list_lock = threading.Lock()


    def add_order(self, order):
        priority = order["priority"]
        self.foods_queue_lock.acquire()
        for item in order["items"]:
            food_dict = self.menu[item - 1]
            dish = Dish(food_dict)
            dish.order_id = order["order_id"]
            self.foods_queue.put(((time.time()+random.uniform(0,1)*priority)*(dish.order_id*0.1),dish))

        self.foods_queue_lock.release()
        order["cooking_details"] = []
        self.order_list_lock.acquire()
        self.order_list.append(order)
        self.order_list_lock.release()
    
    def cook_working(self, cook_id):
        print("Cook_working started!")
        while True:
            self.foods_queue_lock.acquire()
            if self.foods_queue.empty():
                self.foods_queue_lock.release()
                continue
            print("Cook with id "+str(cook_id)+" started cooking.")
            dish = self.foods_queue.get()[1]
            self.foods_queue_lock.release()
            time.sleep(dish.preparation_time)
            self.order_list_lock.acquire()
            for i in range(len(self.order_list)):
                if self.order_list[i]["order_id"] == dish.order_id:
                    self.order_list[i]["cooking_details"].append({
                        "food_id": dish.id,
                        "cook_id": cook_id
                    })
            
            print("Cook with id "+str(cook_id)+" finished cooking.")

            if len(self.order_list[i]["items"]) == len(self.order_list[i]["cooking_details"]):
                print("Order with id "+str(dish.order_id)+" is returned to dinning hall!")
                order = self.order_list.pop(i)
                order["prepared_time"] = int(time.time())
                if "pick_up_time" in order:
                    order["cooking_time"] = order["prepared_time"] - order["pick_up_time"]
                else:
                    order["cooking_time"] = order["prepared_time"] - order["created_time"]
                requests.post("http://127.0.0.1:5000/distribution", json = order)
            
            self.order_list_lock.release()
    
    def Run_kitchen(self):
        for i in range(self.n_cooks):
            cook = threading.Thread(target = self.cook_working, args = (i,))
            cook.start()
        


