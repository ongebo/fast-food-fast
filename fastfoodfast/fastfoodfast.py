from flask import Flask, jsonify, abort, request, session
from .models import Order


app = Flask(__name__)
order_model = Order()

@app.route('/api/v1/customer/orders', methods=['POST'])
def place_new_order():
    if not session['customer_logged_in']:
        abort(401)
    items = request.form['items']
    cost = request.form['cost']
    order = order_model.create_order(session['username'], items, cost)
    return jsonify(order), 201
