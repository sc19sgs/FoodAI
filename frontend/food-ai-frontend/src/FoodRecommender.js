import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FoodRecommender = () => {
  const [dish, setDish] = useState(null);

  // Fetch a random dish from the backend
  const fetchDish = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/get_dish');
      setDish(response.data);
    } catch (error) {
      console.error('Error fetching dish:', error);
    }
  };

  // Run when component mounts
  useEffect(() => {
    fetchDish();
  }, []);

  // Handle user feedback
  const handleFeedback = async (liked) => {
    try {
      await axios.post('http://127.0.0.1:5000/feedback', { dishId: dish.id, liked });
      fetchDish(); // Fetch the next dish after feedback
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  if (!dish) return <div>Loading...</div>;

  return (
    <div className="food-recommender">
      <h2>Do you like this dish?</h2>
      <img src={dish.image} alt={dish.name} width="300" height="400" />
      <h3>{dish.name}</h3>
      <button onClick={() => handleFeedback(true)}>Like 👍</button>
      <button onClick={() => handleFeedback(false)}>Dislike 👎</button>
    </div>
  );
};

export default FoodRecommender;
