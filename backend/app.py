from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity



app = Flask(__name__)
CORS(app)

# Load feedback from CSV for collaborative filtering
feedback_data = pd.read_csv('feedback.csv', header=None, names=['dish_id', 'liked'])
feedback_data['user_id'] = 1  # Assuming a single user for simplicity now

# Create Dataset for Surprise
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(feedback_data[['user_id', 'dish_id', 'liked']], reader)

# Train model
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)


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

# Vectorise dishes
dishes_df = pd.DataFrame(dishes)
tfidf = TfidfVectorizer()
dishes_vectors = tfidf.fit_transform(dishes_df['tags'].apply(lambda tags: " ".join(tags))).toarray()

user_preferences = {"liked": []} # To store liked dishes' IDs

@app.route('/get_dish', methods=['GET'])
def get_dish():
    """Serve one dish based on preferences"""
    if user_preferences["liked"]:
        return recommend()  # Call the recommend function if there are preferences
    
    return jsonify(random.choice(dishes))


@app.route('/feedback', methods=['POST'])
def feedback():
	data = request.json
	dish_id = data['dishId']
	liked = data['liked']
	
	if liked:
		user_preferences['liked'].append(dish_id)
		
	# Save to CSV for more feedback data later
	with open('feedback.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([dish_id, liked])
		
	return jsonify({"message": "Feedback received"})

@app.route('/recommend', methods=['GET'])
def recommend():
    if not user_preferences['liked']:
        return jsonify({"error": "No preferences available"}), 400

    liked_dish_vectors = [dishes_vectors[i] for i in range(len(dishes)) if dishes[i]['id'] in user_preferences['liked']]
    
    if liked_dish_vectors:
        user_vector = np.mean(liked_dish_vectors, axis=0).reshape(1, -1)

        # Get a list of dishes that the user hasn't seen yet
        non_interacted_dishes = [dish for dish in dishes if dish['id'] not in user_preferences['liked']]
        non_interacted_indices = [i for i in range(len(dishes)) if dishes[i]['id'] not in user_preferences['liked']]

        # Vectorise the non-interacted dishes only
        non_interacted_vectors = [dishes_vectors[i] for i in non_interacted_indices]

        # Calculate cosine similarity between user vector and non-interacted dish vectors
        if non_interacted_vectors:
            similarities = cosine_similarity(user_vector, non_interacted_vectors)
            recommended_index = np.argmax(similarities.flatten())
            recommended_dish = non_interacted_dishes[recommended_index]

            return jsonify(recommended_dish)
    
    # If no new dishes are available
    return jsonify({"error": "No dishes found"}), 404


	
    # Recommendation function
@app.route('/collab_recommend', methods=['GET'])
def collab_recommend():
    if feedback_data.empty:
        return jsonify({"error": "No feedback available for collaborative filtering"}), 400

    predictions = []
    for dish in dishes:
        prediction = algo.predict(1, dish['id']).est  # Predict for our single user
        predictions.append((dish['id'], prediction))

    # Find dish with highest prediction
    recommended_dish_id = max(predictions, key=lambda x: x[1])[0]
    recommended_dish = next(d for d in dishes if d['id'] == recommended_dish_id)

    return jsonify(recommended_dish)



if __name__ == '__main__':
    app.run(debug=True)
