from random import randint
import time
import threading
import requests
import random
client_id_ = 0
client_id_lock = threading.Lock()

def Generate_order(menu,client_id):
    nr_dishes = random.randint(1,5)
    items = [random.randint(1,menu["restaurant_data"][0]["menu_items"]) for _ in range(nr_dishes)] 
    priority = random.randint(1,5)
    max_time = max([menu["restaurant_data"][0]["menu"][i]["preparation-time"] for i in items])

    return {
    "client_id": client_id,
    "orders": [
        {
            "restaurant_id":0,
            "items": items,
            "priority": priority,
            "max_wait": max_time*1.3,
            "created_time": int(time.time())
        }
    ]
    }


def Client_Life(client_id):
    response = requests.get("http://localhost:9000/menu")
    menu = response.json()
    
    order = Generate_order(menu,client_id)
    order_response = requests.post("http://localhost:9000/order", json = order)

    estimated_waiting_time = order_response["orders"][0]["estimated_waiting_time"]
    order_id = order_response["orders"][0]["order_id"]
    time.sleep(estimated_waiting_time*1.8)

    order_status_response = requests.get(f"http://localhost:5000/v2/order/{order_id}") 
    if order_status_response["is_ready"]:
        print("Order is ready!")
    else: 
        print("Order is not ready!")
    
    time.sleep(5)


while True:
    if threading.active_count() < 8 :
        threading.Thread(target=Client_Life, args = (client_id_,)).start()
        client_id_ += 1


