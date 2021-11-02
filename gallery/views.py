from django import forms
from django.shortcuts import render
from .forms import CommentForm
from.models import Comment

import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

# Create your views here.
def home_view(request):
    context = {
        'name': 'Alireza'
    }
    return render(request, "home.html", context)

def comment_view(request):
    
    # configure natural language understanding API
    api_key = 'x-rPBSICgFe7jrlwdNMzstEPvlSNZEh_NVnFz32yPBWa'
    api_url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/10a2cbd9-1a19-4184-8895-7a50c5977c64'

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(api_url)

    form = CommentForm(request.POST or None)
    if form.is_valid():

        response = natural_language_understanding.analyze(
        language='en',
        text=form.cleaned_data['comment_text'],
        features=Features(emotion=EmotionOptions(document=True))).get_result()

        # Extracting anger degree from response
        anger_degree = float(response['emotion']['document']['emotion']['anger'])
        print("anger degree: ", anger_degree)
        if anger_degree <= 0.5:
            print("Anger degree of your comment is OK - ", anger_degree)
            form.save()
        else:
            print("Anger degree of your comment is too high! - ", anger_degree)    
        
    objs = Comment.objects.all()
    context = {
        'form': form,
        'comments': list(map(lambda x: x.name + ": " + x.comment_text, objs))
    }
    return render(request, "comment.html", context)

def story_view(request):
    context = {

    }
    return render(request, "story.html", context)