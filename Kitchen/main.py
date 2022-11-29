from flask import Flask, request
from kitchen import Kitchen
import json
import threading

menu = json.load(open("menu.json","r"))


kitchen = Kitchen(4,menu)

app = Flask(__name__)
@app.route("/order",methods = ["POST"])
def order():
    if request.method == "POST":
        order_dict = request.json
        kitchen.add_order(order_dict)

    return "a"

if __name__ == "__main__":
    # Running a thread for the flask application.
    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=4000, host="127.0.0.1",)).start()

    # Creating the dinning hall object and running the main function.
    #dinning_hall_obj = DinningHall(dinning_hall_settings)
    kitchen.Run_kitchen()
