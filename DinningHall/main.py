from flask import Flask, request
from dinning_hall import Dinning_Hall
import time
import threading
import json
import requests

menu = json.load(open("menu.json", "r"))

table_list = [
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    },
    {
        "status": True
    }
]

dinning_hall = Dinning_Hall(table_list, 6, 5000, menu, "McDonald's")

ordering_service_orders = {}

app = Flask(__name__)
@app.route("/distribution", methods = ["POST"])
def distribution():
    if request.method == "POST":
        order_info = request.json
        if "pick_up_time" in order_info:
            print("Order with id "+str(order_info["order_id"])+" was prepared in "+str(time.time() - order_info["pick_up_time"]))
        else:
            print("Order with id "+str(order_info["order_id"])+" was prepared in "+str(time.time() - order_info["created_time"]))
        if order_info["order_id"] not in ordering_service_orders:
            dinning_hall.free_table(order_info["table_id"])
        else:
            order_id = order_info["order_id"]
            ordering_service_orders[order_id]["is_ready"] = True
            ordering_service_orders[order_id]["estimated_waiting_time"] = 0
            ordering_service_orders[order_id]["prepared_time"] = order_info["prepared_time"]
            ordering_service_orders[order_id]["cooking_time"] = order_info["cooking_time"]
            ordering_service_orders[order_id]["cooking_details"] = order_info["cooking_details"]
    
    return "b"

#added
@app.route("/v2/order", methods = ["POST"])
def v2_order():
    if request.method == "POST":
        order_dict = request.json

        new_order_id = dinning_hall.get_order_id_and_increment()
        order_dict["order_id"] = new_order_id
        requests.post("http://127.0.0.1:4000/order",json = order_dict)

        estimated_waiting_time = sum(
            [dinning_hall.menu[i - 1]["preparation-time"]
             for i in order_dict["items"]]
        )
        registered_time = int(time.time())

        ordering_service_orders[new_order_id] = {
            "order_id" : new_order_id,
            "is_ready" : False,
            "estimated_waiting_time" : estimated_waiting_time,
            "priority" : order_dict["priority"],
            "max_wait" : order_dict["max_wait"],
            "created_time" : order_dict["created_time"],
            "registered_time" : registered_time,
            "prepared_time" : 0,
            "cooking_time" : 0,
            "cooking_details" : None
        }

        return {
            "restaurant_id" : 0,
            "order_id" : new_order_id,
            "estimated_waiting_time" : estimated_waiting_time,
            "created_time" : order_dict["created_time"],
            "registered_time" : registered_time
        }

@app.route("/v2/order/<order_id>", methods=["GET"])
def order_check(order_id):
    if request.method == "GET":
        return ordering_service_orders[int(order_id)]


if __name__ == "__main__":
    dinning_hall.register_restaurant()
    # Running a thread for the flask application.
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=5000, host="127.0.0.1",)).start()

    # Creating the dinning hall object and running the main function.
    dinning_hall.Run_restaurant()
    
