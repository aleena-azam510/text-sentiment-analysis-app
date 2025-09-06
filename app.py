import joblib
import os
import requests
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from flask import Flask, request, render_template

# --- NLTK Data Downloads (Vercel-friendly) ---
# This ensures NLTK data is available in the Vercel build environment.
try:
    _ = nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    _ = nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    _ = nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# --- Model & Vectorizer Download Function ---
# Replace with the direct download URLs from your Google Drive
MODEL_URL = "https://drive.google.com/uc?export=download&id=1z-W6MK-RtWOAFpy-UqjBvFDeZAw2maVg"
VECTORIZER_URL = "https://drive.google.com/uc?export=download&id=1GWheWhMdMjtQBL42kPxsn3-4tlS95bmj"

MODEL_FILE = "sentiment_model.joblib"
VECTORIZER_FILE = "tfidf_vectorizer.joblib"

def download_file(url, filename):
    """Downloads a file from a URL if it doesn't already exist."""
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded {filename}.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")
            raise

# Download the files during the build process
download_file(MODEL_URL, MODEL_FILE)
download_file(VECTORIZER_URL, VECTORIZER_FILE)

app = Flask(__name__)

# --- Load the Model and Vectorizer ---
# Now, load the files from the local directory
model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)


# --- Preprocessing & Prediction Functions ---
# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

# Prediction function
def predict_sentiment(text):
    processed_text = preprocess_text(text)
    text_tfidf = vectorizer.transform([processed_text])
    prediction = model.predict(text_tfidf)
    return "Positive" if prediction[0] == 1 else "Negative"


# --- Web Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        review = request.form['review']
        sentiment = predict_sentiment(review)
        return render_template('result.html', review=review, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)