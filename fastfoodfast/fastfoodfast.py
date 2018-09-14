from flask import Flask, jsonify, abort, request, session
from .models import Order


app = Flask(__name__)
order_model = Order()


@app.route('/api/v1/admin/orders/<int:id>', methods=['PUT'])
def update_order_status(id):
    if not session['admin_logged_in']:
        abort(401)
    customer = request.form['customer']
    items = request.form['items']
    cost = request.form['cost']
    status = request.form['status']
    order_model.update_order(id, customer, items, cost, status)
