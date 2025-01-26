from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
app = Flask(__name__)

load_dotenv()

API_KEY = os.environ.get("TRIP_ADVISOR_API_KEY")

URL = "https://api.content.tripadvisor.com/api/v1/location/search"
URLIMG = "https://api.content.tripadvisor.com/api/v1/location/locationId/photos"
URLRVW = "https://api.content.tripadvisor.com/api/v1/location/locationId/reviews"

# two decorators, same function
@app.route('/')
def index():
    
    return render_template('home.html', the_title='Tiger Home Page')

@app.route('/profile')
def profile():
    return render_template('profile.html', the_title='Tiger Home Page')


@app.route('/city')
def city():
    # city search ##################
    search_info = request.args.get('q')
    
    params = {
        'key': API_KEY,
        'searchQuery': search_info,
        'category': "attractions",
        'language': 'en'
    }
    
    res = requests.get(URL, params=params)
    results_data = res.json()
    
    # img search ####################
    
    # # stores location ids to help search through image database
    # location_ids = []
    
    # # gets the data file from the first retrieval and gets the location_ids for the area that was searched
    # for i in results_data.get('data'):
    #     location_ids.append(i.get('location_id'))
    #     print(location_ids)
        
    # for location_id in location_ids:
    #     params_id = {
    #         'locationId': location_id,
    #         'key': API_KEY,
    #         'language': 'en',
    #         'limit': '1'
    #     }

    #     URLIMG = "https://api.content.tripadvisor.com/api/v1/location/" + str(location_id) + "/photos"
    #     res_imgs = requests.get(URLIMG, params=params_id)
    #     print(res_imgs.json())
    #     print(type(res_imgs))
    #     # largest_image_url = res_imgs["data"][0]["images"]["original"]["url"]
    #     # print(largest_image_url)
    
    
    for i in results_data.get('data'):
        location_id = i.get('location_id')
        print(location_id)
        
        params_id = {
            'locationId': location_id,
            'key': API_KEY,
            'language': 'en',
            'limit': '1'
        }

        URLIMG = "https://api.content.tripadvisor.com/api/v1/location/" + str(location_id) + "/photos"
        res_imgs = requests.get(URLIMG, params=params_id)
        print(res_imgs.json())
        print(type(res_imgs))
        
        i['location_id'] = res_imgs.json()
        # largest_image_url = res_imgs["data"][0]["images"]["original"]["url"]
        # print(largest_image_url)
        
    return (render_template('city.html', results=results_data))

BASE_URL = 'https://aa-api-edbb11e7d431.herokuapp.com/'
AIRPORTS_BASE = '/airports?code=<code>'

@app.route('/airport')
def airport():
    res = requests.get(BASE_URL + AIRPORTS_BASE.replace('<code>', 'DFW'))
    results_data = res.json()
    
    return results_data





@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

if __name__ == '__main__':
    app.run(debug=True)
