from flask import Flask, request, jsonify, Response
from .models import User


app = Flask(__name__)
user_model = User()


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
    pass


@app.route('/api/v1/users/orders', methods=['POST'])
def place_new_order_for_food():
    """Adds a new order for food to the database"""
    pass


@app.route('/api/v1/users/orders', methods=['GET'])
def get_user_order_history():
    """Gets a list of orders made by a user in the past"""
    pass


@app.route('/api/v1/orders/', methods=['GET'])
def get_all_orders():
    """Retrieves all food orders from the database"""
    pass


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
