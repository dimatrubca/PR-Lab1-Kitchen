from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)


@app.route('/order', methods=['POST'])
def receive_order():
    order = request.json

    print(order)

    return jsonify(order)