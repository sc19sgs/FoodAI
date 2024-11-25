from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Dummy data: list of dishes
dishes = [
    {"id": 1, "name": "Pizza Margherita", "image": "/images/pizza.jpg", "tags": ["cheese", "italian", "vegetarian"]},
    {"id": 2, "name": "Chicken Tikka", "image": "/images/tikka.jpg", "tags": ["spicy", "indian", "chicken"]},
    {"id": 3, "name": "Caesar Salad", "image": "/images/salad.jpg", "tags": ["healthy", "vegatarian"]},
    {"id": 4, "name": "Spaghetti", "image" : "/images/spaghetti.jpg", "tags": ["pasta", "italian"]},
    {"id": 5, "name": "Hot Dog", "image": "/images/hotdog.jpg", "tags": ["american", "beef"]},
    {"id": 6, "name": "Pancakes", "image": "/images/pancake.jpg", "tags": ["dessert"]},
    {"id": 7, "name": "Chocolate Milkshake", "image": "/images/chocolatemilkshake.jpg", "tags": ["dessert", "chocolate"]},
]

user_preferences = {"liked": [], "disliked": []}

@app.route('/get_dish', methods=['GET'])
def get_dish():
    """Serve one dish based on preferences"""
    if user_preferences["liked"]:
        liked_tags = set(user_preferences["liked"])
        filtered_dishes = [d for d in dishes if liked_tags.intersection(set(d["tags"]))]
        if filtered_dishes:
            return jsonify(random.choice(filtered_dishes))

    return jsonify(random.choice(dishes))

@app.route('/feedback', methods=['POST'])
def feedback():
    """Receive feedback from user"""
    data = request.json
    dish_id = data['dishId']
    liked = data['liked']
    
    for dish in dishes:
        if dish['id'] == dish_id:
            if liked:
                user_preferences["liked"].extend(dish["tags"])
            else:
                user_preferences["disliked"].extend(dish["tags"])
    
    return jsonify({"message": "Feedback received"})


if __name__ == '__main__':
    app.run(debug=True)
