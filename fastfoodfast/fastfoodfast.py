from flask import Flask, jsonify, request
from .models import Order


app = Flask(__name__)
order_model = Order()


@app.route('/')
def index_page():
    return 'Welcome to Fast-Food-Fast!'


@app.route('/api/v1/orders')
def get_all_orders():
    orders = order_model.get_all()
    result = {'orders': orders}
    return jsonify(result)


@app.route('/api/v1/orders/<int:id>')
def get_a_specific_order(id):
    pass


@app.route('/api/v1/orders', methods=['POST'])
def place_a_new_order():
    pass


@app.route('/api/v1/orders/<int:id>', methods=['PUT'])
def update_order_status(id):
    pass
