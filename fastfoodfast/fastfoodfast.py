from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return jsonify('Welcome to Fast-Food-Fast')


@app.route('/api/v1/orders')
def get_all_orders():
    pass


@app.route('/api/v1/orders/<int:id>')
def get_specific_order():
    pass


@app.route('/api/v1/orders', methods=['POST'])
def create_new_order():
    pass

@app.route('/api/v1/orders/<int:id>', methods=['POST'])
def update_order_status():
    pass
