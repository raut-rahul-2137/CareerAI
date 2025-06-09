from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .resume_processor import handle_file_upload, predict_category
import traceback
from django.conf import settings
import logging
import sys
import os
import pickle
import nltk
from nltk.corpus import stopwords
import re
import PyPDF2
import docx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def extract_text_from_pdf(file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
    return text

def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {str(e)}")
    return text

def extract_text_from_txt(file):
    text = ""
    try:
        text = file.read().decode('utf-8')
    except Exception as e:
        print(f"Error reading TXT: {str(e)}")
    return text

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def roadmap(request):
    return render(request, 'roadmap.html')

def software_engineer_roadmap(request):
    return render(request, 'software_engineer_roadmap.html')

def data_science_roadmap(request):
    return render(request, 'data_science_roadmap.html')

def ux_designer_roadmap(request):
    return render(request, 'ux_designer_roadmap.html')

def product_manager_roadmap(request):
    return render(request, 'product_manager_roadmap.html')

def devops_engineer_roadmap(request):
    return render(request, 'devops_engineer_roadmap.html')

def machine_learning_engineer_roadmap(request):
    return render(request, 'machine_learning_engineer_roadmap.html')

def full_stack_developer_roadmap(request):
    return render(request, 'full_stack_developer_roadmap.html')

def cloud_architect_roadmap(request):
    return render(request, 'cloud_architect_roadmap.html')

def cybersecurity_analyst_roadmap(request):
    return render(request, 'cybersecurity_analyst_roadmap.html')

def ai_engineer_roadmap(request):
    return render(request, 'ai_engineer_roadmap.html')

def mobile_developer_roadmap(request):
    return render(request, 'mobile_developer_roadmap.html')

def data_engineer_roadmap(request):
    return render(request, 'data_engineer_roadmap.html')

def business_analyst_roadmap(request):
    return render(request, 'business_analyst_roadmap.html')

def ui_designer_roadmap(request):
    return render(request, 'ui_designer_roadmap.html')

def qa_engineer_roadmap(request):
    return render(request, 'qa_engineer_roadmap.html')

def system_administrator_roadmap(request):
    return render(request, 'system_administrator_roadmap.html')

@require_http_methods(["GET", "POST"])
def assessment(request):
    prediction = None
    error = None
    debug_info = None

    if request.method == 'POST' and request.FILES.get('resume'):
        try:
            resume_file = request.FILES['resume']
            file_name = resume_file.name
            file_size = resume_file.size
            file_type = resume_file.content_type

            # Extract text based on file type
            if file_name.endswith('.pdf'):
                text = extract_text_from_pdf(resume_file)
            elif file_name.endswith('.docx'):
                text = extract_text_from_docx(resume_file)
            elif file_name.endswith('.txt'):
                text = extract_text_from_txt(resume_file)
            else:
                raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT files.")

            if not text.strip():
                raise ValueError("Could not extract text from the file. Please ensure the file is not empty and is properly formatted.")

            # Clean the text
            cleaned_text = cleanResume(text)

            # Load the model and make prediction
            model_path = os.path.join(settings.BASE_DIR, 'career_guide', 'models', 'clf.pkl')
            tfidf_path = os.path.join(settings.BASE_DIR, 'career_guide', 'models', 'tfidf.pkl')
            encoder_path = os.path.join(settings.BASE_DIR, 'career_guide', 'models', 'encoder.pkl')

            with open(model_path, 'rb') as f:
                clf = pickle.load(f)
            with open(tfidf_path, 'rb') as f:
                tfidf = pickle.load(f)
            with open(encoder_path, 'rb') as f:
                encoder = pickle.load(f)

            # Transform the text
            tfidf.fit([cleaned_text])
            features = tfidf.transform([cleaned_text])

            # Make prediction
            prediction = clf.predict(features)
            prediction = encoder.inverse_transform(prediction)[0]

            debug_info = {
                'file_name': file_name,
                'file_size': f"{file_size / 1024:.2f} KB",
                'file_type': file_type,
            }

        except Exception as e:
            error = str(e)
            print(f"Error processing resume: {str(e)}")

    return render(request, 'assessment.html', {
        'prediction': prediction,
        'error': error,
        'debug_info': debug_info
    }) 