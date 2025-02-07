import requests

def get_geolocation(api_key):
    # Google Maps Geolocation API endpoint
    endpoint = "https://www.googleapis.com/geolocation/v1/geolocate"
    
    # Define the parameters (empty body works as well for approximate location)
    payload = {
        "considerIp": True  # This will use the user's IP address to estimate location
    }
    
    # Parameters include the API key in the URL
    params = {
        "key": api_key
    }
    
    # Make a POST request to the Google Maps Geolocation API
    response = requests.post(endpoint, json=payload, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract latitude and longitude
        location = data['location']
        latitude = location['lat']
        longitude = location['lng']
        accuracy = data.get('accuracy', 'N/A')
        return latitude, longitude, accuracy
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
api_key = "AIzaSyA7mrFisKp_ipRDuhCh6IpiC_WYlbZKKvQ"
location = get_geolocation(api_key)
print("Location:", location)
