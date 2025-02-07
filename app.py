from flask import Flask, render_template, request, jsonify, session
import json
import requests
import os
import os
from PIL import Image
import geocoder
from werkzeug.security import generate_password_hash,check_password_hash
import requests
from supabase import supabase
from flask import redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your secret key'


def to_celsius(temp):
    return str(round(float(temp) - 273.15, 2))

# default route
@app.route('/')
def index():
    username = session.get('username', 'Guest')
    return render_template('index.html', username=username)

#Sign Up route
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        data = supabase.table('users').insert({"email": email,"password": password,"username":username}).execute()
        return render_template('login.html')

#login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginuser', methods=['POST'])
def loginuser():
    # Get the form data from the request
    username = request.form['username']
    password = request.form['password']
    try:
        query = (supabase.table('users').select('*').eq('username', username).execute())
        user = query.get('data', [])
        print(user)
        if user:
            user_data = user[0]
            if user_data['password'] == password:
                session['username'] = username
                return render_template('index.html', username=username)
            else:
                return "Invalid password"
        else:
            return "User not found"
    except Exception as e:
        return f"Error: {str(e)}"

#Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the session
    return render_template('index.html', username='Guest')

#Tree Tagging route
@app.route('/location', methods=['GET', 'POST'])
def home():
    print(session)
    if 'username' not in session or session['username'] == 'Guest':
        return redirect(url_for('login'))
    else:
       return render_template('location.html')

def detect_plant_species(image_path):
    API_KEY = "api key"  
    PROJECT = "k-indian-subcontinent"  
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

    # Open the image file
    with open(image_path, 'rb') as image_data:
        data = {
            'organs': ['leaf']
        }

        files = [
            ('images', (image_path, image_data))
        ]

        # Send the request
        response = requests.post(api_endpoint, files=files, data=data)
        
        # Check if the response is successful
        if response.status_code != 200:
            return None, f"Error: {response.status_code} {response.text}"

        json_result = json.loads(response.text)

        # Extract species name from the first result
        if 'results' in json_result and json_result['results']:
            first_result = json_result['results'][0]
            common_names = first_result['species'].get('commonNames', [])

            return common_names[0], None  # Return the species name
        
        return None, "No species found"


@app.route('/detect_plant_species', methods=['POST'])
def detect_plant_species_route():
    # Save the uploaded file
    uploaded_file = request.files['image']
    if uploaded_file is not None:
        # Create a temporary file
        temp_image_path = "temp.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_file.read())
    
    # Detect the plant species
    tree_species, error = detect_plant_species(temp_image_path)
    if error:
        return jsonify({'error': error}), 400
    
    #real weather information
    data = request.form
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and Longitude required'}), 400

    # Fetch real-time weather and soil data
    try:
        # Weather API
        api_key = 'weather api key'
        weather_api_url = 'https://api.openweathermap.org/data/2.5/weather'
        weather_response = requests.get(f'{weather_api_url}?lat={latitude}&lon={longitude}&appid={api_key}&units=metric')

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
        else:
            return jsonify({'error': 'Unable to fetch weather data'}), 500

        # Fetch soil data
        soil_response = requests.get(
            url="https://api-test.openepi.io/soil/type",
            params={"lat": latitude, "lon": longitude}
        )

        if soil_response.status_code == 200:
            soil_data = soil_response.json()
            most_probable_soil_type = soil_data["properties"].get("most_probable_soil_type", "Unknown")
            soil_info = {"soil_type": most_probable_soil_type}
        else:
            soil_info = {"soil_type": "Unknown"}

        # Prepare weather information
        weather_info = {
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'visibility': weather_data['visibility']
        }
        print(weather_info)

        # Return tree species, weather, and soil data
        return jsonify({
            'tree_species': tree_species,
            'weather': weather_info,
            'soil': soil_info
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    


if __name__ == '__main__':
    app.run(debug=True)
