from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image
import io
import json

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})

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


if __name__ == '__main__':
    app.run(debug=True, port=9000)
