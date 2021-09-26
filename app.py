from domain.kitchen import Kitchen
import threading
from flask import Flask, request
from flask.json import jsonify
import utils

app = Flask(__name__)
kitchen = None



@app.route('/order', methods=['POST'])
def receive_order():
    order = request.json

    print(order)
    print("kitchen ", kitchen)
    order_ = utils.request_order_to_order(order)

    kitchen.receive_order(order_)

    return jsonify(order)




if __name__ == "__main__":
    threading.Thread(target=lambda: {
         app.run(debug=True, use_reloader=False)
    }).start()

    kitchen = Kitchen()
    print(kitchen)
    kitchen.run_simulation()