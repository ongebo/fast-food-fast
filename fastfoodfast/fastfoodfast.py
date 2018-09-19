"""
Definitions for Flask Route Functions to implement the API endpoints:
GET /api/v1/orders
GET /api/v1/orders/<orderID>
POST /api/v1/orders
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


@app.route('/api/v1/orders/<int:order_id>')
def get_a_specific_order(order_id):
    """Returns order with specific order_id"""
    try:
        order = order_model.get_order(order_id)
        return jsonify(order), 200
    except OrderNotFound:
        abort(404)


@app.route('/api/v1/orders', methods=['POST'])
def place_a_new_order():
    """
    Adds a new order to the orders list and returns 201 - CREATED status code
    if no exception occurs, otherwise help text with a status code of 400 - BAD REQUEST
    is returned
    """
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


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """Updates status of order with specified order_id if it exists"""
    try:
        order_model.update_order_status(order_id, request.get_json())
        response = Response('', status=200, mimetype='application/json')
        return response
    except Exception as e:
        if isinstance(e, OrderNotFound):
            abort(404)
        return jsonify('Bad Request!'), 400


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_specific_order(order_id):
    """Deletes order with id <order_id> if it exists in the orders list"""
    try:
        order_model.delete_order(order_id)
        return jsonify('NO CONTENT'), 204
    except OrderNotFound:
        abort(404)


@app.errorhandler(404)
def resource_not_found(error):
    """Called when a 404 error has occurred"""
    return jsonify('404 - The requested resource does not exist'), 404
