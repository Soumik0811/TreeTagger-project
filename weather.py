import requests
from dotenv import load_dotenv
import os  
from dataclasses import dataclass

# Load environment variables from a .env file
load_dotenv()

# Define a data class to store weather data
@dataclass
class WeatherData:
    
    temperature: float
    humidity: int
    wind_speed: float
    visibility: float
    

# Fetch the API key from environment variables
api_key = os.getenv('API_KEY')

# Function to get latitude and longitude for a given city, state, and country
def get_lan_lon(city_name, state_code, country_code, API_key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}').json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

# Function to get current weather data based on latitude and longitude
def get_current_weather(lat, lon, API_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    
    
    # Extract relevant data from the API response
    data = WeatherData(
    
        temperature=resp.get('main').get('temp'),
        humidity=resp.get('main').get('humidity'),
        wind_speed=resp.get('wind').get('speed'),
        visibility=resp.get('visibility') / 1000 
        
    )
    
    return data

def main(city_name,state_name,country_name):
    lat, lon = get_lan_lon('Chennai', 'TN', 'India', api_key)
    weather_data = get_current_weather(lat,lon,api_key)
    return weather_data


if __name__ == "__main__":
    lat, lon = get_lan_lon('Chennai', 'TN', 'India', api_key)
    print(get_current_weather(lat, lon, api_key))
