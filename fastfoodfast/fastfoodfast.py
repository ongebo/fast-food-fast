"""
Definitions of API routes for managing users, orders, and food menu data.
"""

from flask import Flask, request, jsonify, Response
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .models import Users, Orders, Menu
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)
Swagger(app)
CORS(app)
users_model = Users()
orders_model = Orders()
menu_model = Menu()


@app.route('/api/v1/auth/signup', methods=['POST'])
@swag_from('docs/register.yml')
def register_a_user():
    """Creates a new user account"""
    try:
        user_data = request.get_json()
        users_model.register_user(user_data)
        return jsonify({'message': 'you were successfully registered!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/auth/login', methods=['POST'])
@swag_from('docs/login.yml')
def login_a_user():
    """Logs in a registered user"""
    try:
        data = request.get_json()
        user = users_model.get_user(data['username'])
        if not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'wrong password'}), 401
        token = create_access_token(identity=user['username'])
        response_body = {
            'message': 'You have been successfully logged in!',
            'admin': users_model.is_admin(user['username']),
            'token': token
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/users/orders', methods=['POST'])
@jwt_required
@swag_from('docs/place_order.yml')
def place_new_order_for_food():
    """Adds a new order for food to the database"""
    try:
        order = request.get_json()
        customer = get_jwt_identity()
        created_order = orders_model.create_order(order, customer)
        return jsonify(created_order), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/users/orders', methods=['GET'])
@jwt_required
@swag_from('docs/order_history.yml')
def get_user_order_history():
    """Gets a list of orders made by a user in the past"""
    try:
        customer = get_jwt_identity()
        orders = orders_model.get_order_history(customer)
        return jsonify({'orders': orders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@swag_from('docs/orders.yml')
def get_all_orders():
    """Retrieves all food orders from the database"""
    try:
        identity = get_jwt_identity()
        if not users_model.is_admin(identity):
            return jsonify({'error': 'only admin can get all orders'}), 401
        return jsonify({'orders': orders_model.get_all_orders()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/v1/orders/<order_id>', methods=['GET'])
@jwt_required
@swag_from('docs/order.yml')
def get_specific_order(order_id):
    """Retrieves a specific food order from the database"""
    try:
        if not users_model.is_admin(get_jwt_identity()):
            return jsonify({'error': 'only admin can fetch a specific order'}), 401
        order = orders_model.get_specific_order(order_id)
        return jsonify(order), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/v1/orders/<order_id>', methods=['PUT'])
@jwt_required
@swag_from('docs/update_order.yml')
def update_order_status(order_id):
    """Updates the status of an order in the database"""
    try:
        status = request.get_json()
        if not users_model.is_admin(get_jwt_identity()):
            return jsonify({'error': 'only admin can update order status'}), 401
        orders_model.update_order_status(order_id, status)
        return jsonify({'message': 'successfully updated order status'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/menu', methods=['GET'])
@jwt_required
@swag_from('docs/menu.yml')
def get_food_items():
    """Retrieves all the available food items in the menu"""
    try:
        menu = menu_model.get_food_menu()
        return jsonify({'menu': menu}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/api/v1/menu/<int:identity>', methods=['GET'])
@jwt_required
def get_food_item(identity):
    """Retrieves specific food item from the menu"""
    try:
        item = menu_model.get_specific_menu_item(identity)
        return jsonify(item), 200
    except Exception as e:
        return jsonify(str(e)), 404


@app.route('/api/v1/menu', methods=['POST'])
@jwt_required
@swag_from('docs/menu_item.yml')
def add_menu_item():
    """Adds a new food menu item to the database"""
    try:
        if not users_model.is_admin(get_jwt_identity()):
            return jsonify({'error': 'you are not an administrator'}), 401
        menu_item = request.get_json()
        created_item = menu_model.add_menu_item(menu_item)
        return jsonify(created_item), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.errorhandler(404)
def resource_not_found(error):
    """Displays an error message when a 404 error occurs"""
    return jsonify({'error': '404 - The requested resource does not exist'}), 404
