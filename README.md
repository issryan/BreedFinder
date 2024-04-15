# Dog Breed Classification App

## Introduction
This project integrates machine learning, web development, and database management to create an application that classifies dog breeds from images. It uses the Stanford Dog Breed dataset for model training.

## Development Process

### 1. Model Training
**Notebook:** `train_dog_classification_model.ipynb`

#### Objective
Develop a robust machine learning model to accurately classify dog breeds from images.

#### Choice of Model: MobileNet
- **Why MobileNet?** MobileNet is selected for its efficiency on devices with limited resources. It utilizes depthwise separable convolutions, which reduces computational demands without a significant loss in accuracy, making it ideal for web applications.

#### Data Preparation
- **Dataset:** Stanford Dog Breed dataset.
- **Preprocessing:** Images are standardized in size and normalized.
- **Augmentation:** Techniques like rotation and flipping are applied to enhance model robustness.

#### Model Accuracy vs. Confidence Score
- **Model Accuracy:** Measures the overall performance during testing, indicating the frequency of correct breed identification.
- **Confidence Score:** When a user submits an image, the model provides a confidence score with its prediction, reflecting the probability associated with the model's prediction.

#### Challenges
- **Data Imbalance:** Addressed through weighted loss functions and augmented training data.
- **Model Selection:** MobileNet was chosen for its balance between efficiency and performance.

### 2. Backend Development

#### Objective
Create a scalable and secure backend capable of handling API requests for dog breed classification and managing user interactions.

#### Process
- **Flask Setup:** Selected Flask for its simplicity and flexibility, facilitating quick RESTful API endpoint setup.
- **Integration with the Model:** The trained model is integrated into the Flask app, which involves loading the model and handling image data from POST requests.
- **Database Integration:** MongoDB is used for storing user data and logs, aiding in session management and historical data analysis.

#### Challenges
- Ensuring secure and efficient image data handling.
- Integrating the Python machine learning model with Flask.
- Ensuring compatibility of dependency versions.

### 3. Frontend Development
**File:** `App.jsx`

#### Objective
Design a user-friendly interface that enables easy interaction with the application.

#### Process
- **React Framework:** Utilized to construct a responsive and interactive UI.
- **Component Design:** Structured into components like Image Upload, Results Display, and Header.
- **State Management:** Employed React’s state management to control component states, particularly for image data and classification results.

#### Challenges
- Ensuring browser compatibility.
- Implementing an intuitive design to simplify user interactions.

## References
- Howard, A. G., et al. (2017). MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. [arXiv:1704.04861](https://arxiv.org/abs/1704.04861).
- Khosla, Aditya, et al. "Novel Dataset for Fine-Grained Image Categorization: Stanford Dogs." Proc. CVPR Workshop on Fine-Grained Visual Categorization (FGVC), 2011. http://vision.stanford.edu/aditya86/ImageNetDogs/
- [Stanford Dogs Dataset on Kaggle](https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset) - Provides the dataset used for training the machine learning model.
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Keras Documentation](https://keras.io/)
