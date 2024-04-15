from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import io
from PIL import Image
import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Setup logging
logging.basicConfig(level=logging.INFO)

# MongoDB setup
client = MongoClient("mongodb+srv://arafehryan:ryan123@dogs.iyycswl.mongodb.net/?retryWrites=true&w=majority&appName=dogs")
db = client.DogBreedClassifier
predictions_collection = db.predictions

# Load the trained model
model = load_model('/Users/ryanarafeh/Desktop/breedfinder/server/final_dog_breed_classifier.h5')

# Load the breed names
with open('/Users/ryanarafeh/Desktop/breedfinder/server/breed_names.json', 'r') as f:
    breed_names = json.load(f)

def format_breed_name(breed_name):
    name_without_prefix = breed_name.split('-', 1)[-1] if '-' in breed_name else breed_name
    formatted_name = ' '.join(word.capitalize() for word in name_without_prefix.split('_'))
    return formatted_name

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify(error="Please upload a file"), 400

        file = request.files['file']
        img_bytes = io.BytesIO(file.read())
        img = Image.open(img_bytes).convert('RGB')
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        processed_image = preprocess_input(img_array_expanded_dims)

        prediction = model.predict(processed_image)
        breed_index = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction)
        breed_name = breed_names[breed_index]
        formatted_breed_name = format_breed_name(breed_name)
        confidence_percentage = round(confidence * 100, 2)
        
        # Insert the prediction results into the MongoDB collection
        predictions_collection.insert_one({
            "timestamp": datetime.utcnow(),
            "breed_name": formatted_breed_name,
            "confidence": confidence_percentage
        })

        return jsonify(breed_name=formatted_breed_name, confidence=f"{confidence_percentage}%")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify(error=str(e)), 500

# Route to retrieve prediction history from MongoDB
@app.route('/history', methods=['GET'])
def get_history():
    try:
        predictions = list(predictions_collection.find({}, {'_id': 0, 'timestamp': 1, 'breed_name': 1, 'confidence': 1}).sort('timestamp', -1))
        return jsonify(predictions)
    except Exception as e:
        logging.error(f"An error occurred when fetching history: {str(e)}")
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, port=9000)