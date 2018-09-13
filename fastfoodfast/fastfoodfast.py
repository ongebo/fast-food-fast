from flask import Flask, session, jsonify, abort
from .models import Order, orders


app = Flask(__name__)
order_model = Order()


@app.route('/api/v1/customer/orders')
def get_customer_order_history():
    if not session.get('customer_logged_in'):
        abort(401)
    history = order_model.read_order_history(session['username'])
    return jsonify(history)


@app.route('/ap1/v1/admin/orders')
def get_all_orders():
    if not session.get('admin_logged_in'):
        abort(401)
    return jsonify(order_model.read_orders())
