from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/api/v1/orders')
def get_all_orders():
    return jsonify({'orders': orders})


orders = list()
