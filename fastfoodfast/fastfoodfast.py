"""
Definitions for Flask Route Functions to implement the API endpoints:
GET /api/v1/orders
GET /api/v1/orders/<orderID>
POST /api/v1/orders
PUT /api/v1/orders/<orderID>
DELETE /api/v1/orders/<orderID>

POST /api/v1/menu-items
GET /api/v1/menu-items
"""
from flask import Flask, jsonify, request, abort, Response
from .models import Order, Menu, OrderNotFound, BadRequest


app = Flask(__name__)
order_model = Order()
menu_model = Menu()


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
        message = 'Successfully updated status of order with id {}'.format(order_id)
        return jsonify(message), 200
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


# Routes for Handling Food Menu


@app.route('/api/v1/menu-items', methods=['POST'])
def add_new_menu_item():
    """
    Adds a new food item to the menu from POST request data. Returns the created menu item and
    a status code of 201 if successful, otherwise returns help text and a status code of 400
    """
    try:
        menu_item = request.get_json()
        created_item = menu_model.create_menu_item(menu_item)
        response = jsonify(created_item)
        response.headers['Location'] = '/api/v1/menu-items/{}'.format(created_item['item-id'])
        return response, 201
    except Exception as e:
        help_text = """
        Menu Item should be represtented as:
        {
            'item': '<item-name>',
            'unit': '<measurement-unit>',
            'rate': <unit-cost>
        }
        'item', and 'rate' are compulsory
        'unit' for example piece, pack, etc: is optional
        """
        response = {'help': e.args[0] + '\n' + help_text}
        return jsonify(response), 400

@app.route('/api/v1/menu-items')
def get_all_menu_items():
    """Returns all availabe food items in the Menu model with 200 status code"""
    menu_items = menu_model.get_all()
    return jsonify({'menu-items': menu_items}), 200
