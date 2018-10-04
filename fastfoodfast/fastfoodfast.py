from flask import Flask, request, jsonify, Response
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .models import User, Order, Menu


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)
user_model = User()
order_model = Order()
menu_model = Menu()


@app.route('/api/v1/auth/signup', methods=['POST'])
def register_a_user():
    """Creates a new user account"""
    try:
        user_data = request.get_json()
        created_user = user_model.register_user(user_data)
        return jsonify(created_user), 201
    except Exception as e:
        response = Response(str(e), status=400, mimetype='text/plain')
        return response


@app.route('/api/v1/auth/login', methods=['POST'])
def login_a_user():
    """Logs in a registered user"""
    try:
        data = request.get_json()
        user = user_model.get_user(data['username'])
        if not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'wrong password'}), 401
        token = create_access_token(identity=user['username'])
        return jsonify({'token': token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/users/orders', methods=['POST'])
@jwt_required
def place_new_order_for_food():
    """Adds a new order for food to the database"""
    try:
        order = request.get_json()
        customer = get_jwt_identity()
        created_order = order_model.create_order(order, customer)
        return jsonify(created_order), 201
    except:
        help_text = """
        You posted invalid data for an order. Ensure you follow these rules:
        
        1. order should have the format:
        {
            'items': [
                {'item': '<item-name>', 'quantity': <number>, 'cost': <number>},
                {'item': '<item-name>', 'quantity': <number>, 'cost': <number>}
            ],
            'status': 'order-status',
            'total-cost': number,
            'order-id': number
            
        }
        status: can be 'pending', 'accepted' or 'complete'
        status, total-cost, and order-id are optional
        items: compulsory
        
        2. <item-name> cannot be an empty string, and can only contain letters, numbers and spaces
        3. <number> for 'quantity' and 'cost' cannot be zero or negative
        """
        response = Response(help_text, status=400, mimetype='text/plain')
        return response


@app.route('/api/v1/users/orders', methods=['GET'])
@jwt_required
def get_user_order_history():
    """Gets a list of orders made by a user in the past"""
    try:
        customer = get_jwt_identity()
        orders = order_model.get_order_history(customer)
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404


@app.route('/api/v1/orders/', methods=['GET'])
@jwt_required
def get_all_orders():
    """Retrieves all food orders from the database"""
    try:
        identity = get_jwt_identity()
        if not order_model.is_admin(identity):
            return jsonify({'message': 'only admin can get all orders'}), 401
        return jsonify({'orders': order_model.get_all_orders()}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404


@app.route('/api/v1/orders/<order_id>', methods=['GET'])
@jwt_required
def get_specific_order(order_id):
    """Retrieves a specific food order from the database"""
    try:
        if not order_model.is_admin(get_jwt_identity()):
            return jsonify({'message': 'only admin can fetch a specific order'}), 401
        order = order_model.get_specific_order(order_id)
        return jsonify(order), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404


@app.route('/api/v1/orders/<order_id>', methods=['PUT'])
@jwt_required
def update_order_status(order_id):
    """Updates the status of an order in the database"""
    try:
        status = request.get_json()
        if not order_model.is_admin(get_jwt_identity()):
            return jsonify({'message': 'only admin can update order status'}), 401
        order_model.update_order_status(order_id, status)
        return jsonify({'message': 'successfully updated order status'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/api/v1/menu', methods=['GET'])
@jwt_required
def get_food_items():
    """Retrieves all the available food items in the menu"""
    try:
        menu = menu_model.get_food_menu()
        return jsonify({'menu': menu}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/v1/menu', methods=['POST'])
@jwt_required
def add_menu_item():
    """Adds a new food menu item to the database"""
    try:
        if not order_model.is_admin(get_jwt_identity()):
            return jsonify({'message': 'you are not an administrator'}), 401
        menu_item = request.get_json()
        menu_model.add_menu_item(menu_item)
        return jsonify({'message': 'correctly created new menu item'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def resource_not_found(error):
    """Displays an error message when a 404 error occurs"""
    return jsonify({'error': '404 - The requested resource does not exist'}), 404
