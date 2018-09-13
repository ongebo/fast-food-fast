from flask import Flask, session, jsonify, abort
from .models import Order


app = Flask(__name__)
order_model = Order()

@app.route('/api/v1/customer/orders/<int:id>')
def get_specific_user_order(id):
    if not session.get('customer_logged_in'):
        abort(401)
    return jsonify(order_model.read(id))


@app.route('/api/v1/admin/orders/<int:id>')
def get_specific_order(id):
    if not session.get('admin_logged_in'):
        abort(401)
    return jsonify(order_model.read(id))
