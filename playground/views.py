# views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_protect
import joblib

@csrf_protect
def mood_detection_form(request):
    print(request.POST)
    return render(request, 'hello.html')
# views.py
from django.http import JsonResponse




def get_recommendations_view(request):
    if request.method == 'POST':
        # Create variable to store the collected data from the form
        weather = request.POST.get('weather')
        music = request.POST.get('music')
        color = request.POST.get('color')
        food = request.POST.get('food')
        energy = request.POST.get('energy')

        
        # Client ID, Client secret to generate access token for validating api purposes
        client_id = '2055710caae24602bda237249c21644a'
        client_secret = '0cdcdb884b1c4d029bf36a5b312cb1fd'

        # Call a function to get the mood of the user by sending to a ml model
        genres=get_mood(weather, music, color, food, energy)
        

        # Obtain the access token
        access_token = get_spotify_access_token(client_id, client_secret)
        recommendations = get_spotify_recommendations(genres,access_token)
        
        # Pass the recommendations to the display page
        return render(request, 'display.html', {'recommendations': recommendations})

    # Handle other HTTP methods if needed
    return JsonResponse({'error': 'Invalid request method'})

def get_mood(weather, music, color, food, energy):
    
    # loads the catboost classifier
    clf = joblib.load(r'C:\Users\kamal\Documents\Django_yt\playground\static\ml_models\ml_model.joblib')


    # Predict the mood based on user inputs
    mood_test = clf.predict([weather, music, color, food, energy])

    # Creating a mood mapping to the recommended genres
    mood_mapping = {'High Energy and Positive': ['pop', 'electronic', 'Feel-Good Indie', 'pop-rock'],
                     'Moderate Energy and Neutral': ['indie', 'folk', 'jazz'],
                     'Low Energy and Potentially Negative': ['blues', 'classical', 'downtempo']}

    string = ''.join(mood_test)
    

    genres_recommendations = mood_mapping.get(string, [])  # Get recommended genres based on predicted mood
    return genres_recommendations

    

def get_spotify_recommendations(recommendations,access_token):
  
    params = {
        'seed_genres': recommendations,
        'limit': 10,
        
    }

    headers = {'Authorization': f'Bearer {access_token}'}

    # Make a recommendation request to Spotify API
    response = requests.get('https://api.spotify.com/v1/recommendations', params=params, headers=headers)

    # Return the relevant part of the Spotify API response
    return response.json().get('tracks')

import base64
import requests

def get_spotify_access_token(client_id, client_secret):
    # Spotify API endpoint for obtaining access token
    token_url = 'https://accounts.spotify.com/api/token'

    # Concatenate client ID and client secret with a colon and base64 encode
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')

    # Request headers
    headers = {
        'Authorization': f'Basic {credentials}',
    }

    # Request body parameters
    data = {
        'grant_type': 'client_credentials',
    }

    try:
        # Make a POST request to obtain the access token
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extract the access token from the response
        access_token = response.json().get('access_token')
        return access_token
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

