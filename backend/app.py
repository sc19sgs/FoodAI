from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dummy data: list of dishes
dishes = [
    {"id": 1, "name": "Pizza Margherita", "image": "/images/pizza.jpg", "tags": ["cheese", "italian", "vegetarian"]},
    {"id": 2, "name": "Chicken Tikka", "image": "/images/tikka.jpg", "tags": ["spicy", "indian", "chicken"]},
    {"id": 3, "name": "Caesar Salad", "image": "/images/salad.jpg", "tags": ["healthy", "vegatarian"]},
]

@app.route('/get_dish', methods=['GET'])
def get_dish():
    """Serve one dish image at a time"""
    # Just pick a random dish for now
    import random
    dish = random.choice(dishes)
    return jsonify(dish)

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    # Store feedback in future (just print for now)
    print(f"Feedback received {data}")
    return jsonify({"message": "Feedback Received"})

if __name__ == '__main__':
    app.run(debug=True)
