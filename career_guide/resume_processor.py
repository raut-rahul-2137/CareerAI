import pickle
import docx
import PyPDF2
import re
import os
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile

# Load pre-trained model and TF-IDF vectorizer
def load_models():
    try:
        print("Loading models...", file=sys.stderr)
        # Check if all required files exist
        required_files = {
            'clf.pkl': 'Classification model',
            'tfidf.pkl': 'TF-IDF vectorizer',
            'encoder.pkl': 'Label encoder'
        }
        
        missing_files = []
        for file_name, description in required_files.items():
            if not os.path.exists(file_name):
                missing_files.append(f"{description} ({file_name})")
        
        if missing_files:
            raise FileNotFoundError(
                f"Missing required model files: {', '.join(missing_files)}. "
                "Please ensure all model files are present in the project root directory."
            )
        
        print("All model files found, loading...", file=sys.stderr)
        # Load the models
        svc_model = pickle.load(open('clf.pkl', 'rb'))
        print("SVC model loaded", file=sys.stderr)
        tfidf = pickle.load(open('tfidf.pkl', 'rb'))
        print("TF-IDF vectorizer loaded", file=sys.stderr)
        le = pickle.load(open('encoder.pkl', 'rb'))
        print("Label encoder loaded", file=sys.stderr)
        return svc_model, tfidf, le
        
    except Exception as e:
        print(f"Error loading models: {str(e)}", file=sys.stderr)
        raise

def cleanResume(txt):
    try:
        print("Cleaning resume text...", file=sys.stderr)
        cleanText = re.sub('http\S+\s', ' ', txt)
        cleanText = re.sub('RT|cc', ' ', cleanText)
        cleanText = re.sub('#\S+\s', ' ', cleanText)
        cleanText = re.sub('@\S+', '  ', cleanText)
        cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
        cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
        cleanText = re.sub('\s+', ' ', cleanText)
        print(f"Cleaned text length: {len(cleanText)}", file=sys.stderr)
        return cleanText
    except Exception as e:
        print(f"Error cleaning text: {str(e)}", file=sys.stderr)
        raise

def extract_text_from_pdf(file):
    try:
        print("Extracting text from PDF...", file=sys.stderr)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        print(f"PDF text extracted, length: {len(text)}", file=sys.stderr)
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {str(e)}", file=sys.stderr)
        raise

def extract_text_from_docx(file):
    try:
        print("Extracting text from DOCX...", file=sys.stderr)
        doc = docx.Document(file)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        print(f"DOCX text extracted, length: {len(text)}", file=sys.stderr)
        return text
    except Exception as e:
        print(f"Error extracting DOCX text: {str(e)}", file=sys.stderr)
        raise

def extract_text_from_txt(file):
    try:
        print("Extracting text from TXT...", file=sys.stderr)
        try:
            text = file.read().decode('utf-8')
        except UnicodeDecodeError:
            text = file.read().decode('latin-1')
        print(f"TXT text extracted, length: {len(text)}", file=sys.stderr)
        return text
    except Exception as e:
        print(f"Error extracting TXT text: {str(e)}", file=sys.stderr)
        raise

def handle_file_upload(uploaded_file):
    try:
        print(f"Handling file upload: {uploaded_file.name}", file=sys.stderr)
        if not isinstance(uploaded_file, InMemoryUploadedFile):
            raise ValueError("Invalid file upload")
            
        file_extension = uploaded_file.name.split('.')[-1].lower()
        print(f"File extension: {file_extension}", file=sys.stderr)
        
        if file_extension == 'pdf':
            text = extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            text = extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            text = extract_text_from_txt(uploaded_file)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
        
        if not text.strip():
            raise ValueError("No text could be extracted from the file. Please ensure the file is not empty and is properly formatted.")
            
        return text
    except Exception as e:
        print(f"Error handling file upload: {str(e)}", file=sys.stderr)
        raise

def predict_category(resume_text):
    try:
        print("Starting prediction process...", file=sys.stderr)
        svc_model, tfidf, le = load_models()
        
        # Clean and preprocess the text
        cleaned_text = cleanResume(resume_text)
        print(f"Text cleaned, length: {len(cleaned_text)}", file=sys.stderr)
        
        # Vectorize the text
        vectorized_text = tfidf.transform([cleaned_text])
        vectorized_text = vectorized_text.toarray()
        print("Text vectorized", file=sys.stderr)
        
        # Make prediction
        predicted_category = svc_model.predict(vectorized_text)
        predicted_category_name = le.inverse_transform(predicted_category)
        print(f"Prediction made: {predicted_category_name[0]}", file=sys.stderr)
        
        return predicted_category_name[0]
    except Exception as e:
        print(f"Error making prediction: {str(e)}", file=sys.stderr)
        raise 