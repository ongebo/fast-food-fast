from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/api/v1/orders/<int:id>')
def get_specific_order(id):
    order = 'order' + str(id)
    result = None
    for order in orders:
        if order['id'] == id:
            result = order
    return jsonify({order: result})


orders = list()
