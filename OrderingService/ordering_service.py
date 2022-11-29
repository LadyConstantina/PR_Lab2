import queue
import threading
import requests
import time
from queue import PriorityQueue
from restaurant import Restaurant

class OrderManager:
    def __init__(self, n_threads):
        self.n_threads = n_threads
        self.order_queue = queue.PriorityQueue()
        #self.order_id = 0
        self.restaurants = []

        self.order_queue_lock = threading.Lock()
        self.restaurants_lock = threading.Lock()

    def get_menu(self):
        menu_dict = {
            "restaurants" : len(self.restaurants),
            "restaurants_data" : []
        }
        for restaurant in self.restaurants:
            menu_dict["restaurants_data"].append(restaurant.to_dict())
        return menu_dict

    def add_restaurant(self, restaurant):
        self.restaurants_lock.acquire()
        self.restaurants.append(restaurant)
        self.restaurants_lock.release()

    def add_order(self, order):
        self.order_queue_lock.acquire()
        self.order_queue.put((-order.created_time, order))
        self.order_queue_lock.release()

    def order_sending(self):
        while True:
            self.order_queue_lock.acquire()
            if self.order_queue.qsize() <= 0:
                self.order_queue_lock.release()
                continue
            else:
                order = self.order_queue.get()[1]
                self.order_queue_lock.release()

                self.restaurants_lock.acquire()
                restaurant = self.restaurants[order.restaurant_id]
                self.restaurants_lock.release()

                order.add_restaurant_details(restaurant)

                response = requests.post(order.restaurant_address + "/v2/order",
                              json = order.to_v2_order())

                order.add_restaurant_response(response.json())

                with order.condition:
                    order.notify()

    def run_manager(self):
        for i in range(self.n_threads):
            threading.Thread(target=self.order_sending, name=f"sender - {i}").start()
            time.sleep(1)
