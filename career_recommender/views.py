from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
# from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Create your views here.

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')

def assessment(request):
    if request.method == 'POST':
        # Get form data
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        skills = request.POST.getlist('skills')
        traits = request.POST.getlist('traits')

        # Process the data and generate recommendations
        recommendations = generate_recommendations(education, experience, skills, traits)
        
        return render(request, 'assessment.html', {
            'recommendations': recommendations,
            'form_submitted': True
        })
    
    return render(request, 'assessment.html')

def generate_recommendations(education, experience, skills, traits):
    # This is a placeholder for the actual AI recommendation logic
    # In a real application, you would:
    # 1. Load a trained model
    # 2. Preprocess the input data
    # 3. Make predictions
    # 4. Return formatted recommendations
    
    # For now, return some example recommendations
    return [
        {
            'title': 'Software Developer',
            'match_score': 85,
            'description': 'Perfect for your technical skills and analytical mindset.',
            'required_skills': ['Programming', 'Problem Solving', 'Team Collaboration']
        },
        {
            'title': 'Data Scientist',
            'match_score': 80,
            'description': 'Great match for your analytical skills and interest in data.',
            'required_skills': ['Data Analysis', 'Statistics', 'Machine Learning']
        },
        {
            'title': 'UX/UI Designer',
            'match_score': 75,
            'description': 'Matches your creative traits and design skills.',
            'required_skills': ['Design', 'User Research', 'Prototyping']
        }
    ]
