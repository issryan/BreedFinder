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

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})

# MongoDB setup
client = MongoClient("mongodb+srv://arafehryan:ryan123@dogs.iyycswl.mongodb.net/?retryWrites=true&w=majority&appName=dogs")
db = client.DogBreedClassifier
predictions_collection = db.predictions

# Load the trained model
model = load_model('/Users/ryanarafeh/Desktop/breedfinder/server/final_dog_breed_classifier.h5')

# Load the breed names
with open('/Users/ryanarafeh/Desktop/breedfinder/server/breed_names.json', 'r') as f:
    breed_names = json.load(f)
print("Loaded breed names:", breed_names)

def format_breed_name(breed_name):
    # Remove the numeric prefix
    name_without_prefix = breed_name.split('-', 1)[-1] if '-' in breed_name else breed_name
    # Replace underscores with spaces and capitalize each word
    formatted_name = ' '.join(word.capitalize() for word in name_without_prefix.split('_'))
    return formatted_name

@app.route('/')
def index():
    # Example route to test the database insertion
    predictions_collection.insert_one({"test": "data"})
    return 'Connected to MongoDB and data inserted!'

@app.route('/predict', methods=['POST'])
def predict():
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
    confidence = np.max(prediction)  # Get the maximum probability
    breed_name = breed_names[breed_index]
    formatted_breed_name = format_breed_name(breed_name)

    # Convert confidence to percentage
    confidence_percentage = round(confidence * 100, 2)

    return jsonify(breed_name=formatted_breed_name, confidence=f"{confidence_percentage}%")

@app.route('/history', methods=['GET'])
def get_history():
    predictions = list(predictions_collection.find({}, {'_id': 0, 'timestamp': 1, 'breed_name': 1, 'confidence': 1}).sort('timestamp', -1))
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True, port=9000)
