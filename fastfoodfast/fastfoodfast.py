"""
Definitions for Flask Route Functions to implement the API endpoints:
GET /api/v1/orders
GET /api/v1/orders/<orderID>
POST /api/v1/orders/<orderID>
PUT /api/v1/orders/<orderID>
DELETE /api/v1/orders/<orderID>
"""
from flask import Flask, jsonify, request, abort, Response
from .models import Order, OrderNotFound, BadRequest


app = Flask(__name__)
order_model = Order()


@app.route('/')
def index_page():
    return jsonify('Welcome to Fast-Food-Fast!')


@app.route('/api/v1/orders')
def get_all_orders():
    """Returns JSON representation of all orders in the model"""
    orders = order_model.get_all()
    result = {'orders': orders}
    return jsonify(result), 200


@app.route('/api/v1/orders/<int:id>')
def get_a_specific_order(id):
    try:
        order = order_model.get_order(id)
        return jsonify(order)
    except OrderNotFound:
        abort(404)


@app.route('/api/v1/orders', methods=['POST'])
def place_a_new_order():
    try:
        order = request.get_json()
        created_order = order_model.create_order(order)
        return jsonify(created_order), 201
    except:
        help_text = """
        order should have the format:
        {
            'items': [
                {'item': '<item-name>', 'quantity': <number>, 'cost': <number>},
                {'item': '<item-name>', 'quantity': <number>, 'cost': <number>}
            ],
            'status': '<order-status>',
            'total-cost': <number>,
            'order-id': <number>
        }
        status: can be pending, accepted or complete
        status, total-cost, and order-id are optional
        items: compulsory
        """
        return jsonify({'help': help_text}), 400


@app.route('/api/v1/orders/<int:id>', methods=['PUT'])
def update_order_status(id):
    try:
        order_model.update_order_status(id, request.get_json())
        response = Response('', status=200, mimetype='application/json')
        return response
    except Exception as e:
        if isinstance(e, OrderNotFound):
            abort(404)
        return jsonify('Bad Request!'), 400


@app.route('/api/v1/orders/<int:id>', methods=['DELETE'])
def delete_specific_order(id):
    try:
        order_model.delete_order(id)
        return jsonify('NO CONTENT'), 204
    except OrderNotFound:
        abort(404)


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify('404 - The requested resource does not exist'), 404
