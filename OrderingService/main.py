from flask import Flask, request
from ordering_service import OrderManager
from restaurant import Restaurant
from order import Order
import time
import threading

order_manager = OrderManager(10)

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        restaurant_dict = request.json

        restaurant = Restaurant(restaurant_dict)
        order_manager.add_restaurant(restaurant)
        return {
            "status" : "ok"
        }, 200

@app.route("/menu", methods = ["GET"])
def menu():
    if request.method == "GET":
        return order_manager.get_menu()

@app.route("/order", methods = ["POST"])
def order():
    if request.method == "POST":
        order_json = request.json
        for i in range(len(order_json["orders"])):
            order = Order(order_json["orders"][i], threading.Condition())

            order_manager.add_order(order)

            with order.condition:
                order.condition.wait()
            order_json["orders"][i] = order.response_to_order()
        return order_json

if __name__ == "__main__":
    # Running a thread for the flask application.
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=9000, host="127.0.0.1",)).start()

    order_manager.run_manager()
