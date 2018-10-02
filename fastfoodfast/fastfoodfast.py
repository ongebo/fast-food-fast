from flask import Flask, request, jsonify, Response
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .models import User, Order


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key'
jwt = JWTManager(app)
user_model = User()
order_model = Order()


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
        return jsonify({'token': token}), 201
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


@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_specific_order():
    """Retrieves a specific food order from the database"""
    pass


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order_status():
    """Updates the status of an order in the database"""
    pass


@app.route('/api/v1/menu', methods=['GET'])
def get_food_items():
    """Retrieves all the available food items in the menu"""
    pass


@app.route('/api/v1/menu', methods=['POST'])
def add_menu_item():
    """Adds a new food menu item to the database"""
    pass


@app.errorhandler(404)
def resource_not_found(error):
    """Displays an error message when a 404 error occurs"""
    return jsonify({'error': '404 - The requested resource does not exist'}), 404
