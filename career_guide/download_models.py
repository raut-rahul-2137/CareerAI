import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Create and save TF-IDF vectorizer
tfidf = TfidfVectorizer(max_features=1500, stop_words='english')
with open('models/tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

# Create and save label encoder
encoder = LabelEncoder()
with open('models/encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

# Create and save classifier
clf = OneVsRestClassifier(SVC(kernel='linear', probability=True))
with open('models/clf.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("Model files have been created and saved in the 'models' directory.") 