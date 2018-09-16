from flask import Flask, jsonify, request, abort, Response
from .models import Order, OrderNotFound, BadRequest


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
        response = Response(str(created_order), status=201, mimetype='application/json')
        response.headers['Location'] = '/api/v1/orders/{}'.format(created_order['order-id'])
        return response
    except:
        bad_request = {
            'help': 'order should take the form:\n'
            '{\n'
            '  "items": [\n'
            '    {"item": <name>, "quantity": <number>, "cost": <number>},\n'
            '    {"item": <name>, "quantity": <number>, "cost": <number>},\n'
            '    {"item": <name>, "quantity": <number>, "cost": <number>},\n'
            '  ]\n'
            '}\n'
        }
        response = Response(str(bad_request), status=400, mimetype='application/json')
        return response


@app.route('/api/v1/orders/<int:id>', methods=['PUT'])
def update_order_status(id):
    try:
        order_model.update_order_status(id, request.get_json())
        response = Response('', status=200, mimetype='application/json')
        return response
    except OrderNotFound:
        abort(404)
    except BadRequest:
        response = Response('Bad Request!', status=400, mimetype='application/json')
        return response
    except:
        return 'Bad Request!', 400


@app.errorhandler(404)
def resource_not_found():
    return '404 - The requested resource does not exist', 404
