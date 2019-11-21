import requests
import json

malaga_lat = -4.43
malaga_lon = 36.71
url = 'https://api.darksky.net/forecast/{}/{},{}?exclude=[currently, minutely, alerts, flags]&lang=en&units=si'
# Mapping between fontawesome icons and darksky icons
# fontawesome icons:
# sun, snowflake, cloud-sun, cloud-sun-rain, cloud-rain, smog
# darksky icons:
# clear-day, clear-night, rain, snow, sleet, wind, fog, cloudy, partly-cloudy-day, partly-cloudy-night

iconMapping = {
    'clear-day': 'sun',
    'clear-night': 'sun',
    'rain': 'cloud-rain',
    'snow': 'snowflake',
    'sleet': 'snowflake',
    'wind': 'sun',
    'fog': 'smog',
    'cloudy': 'cloud-sun',
    'partly-cloudy-day': 'cloud-sun',
    'partly-cloudy-night': 'cloud-sun'
}

def downloadWeatherForecast(lat, lon):
    '''
    Download weather data and returns a json
    with the response
    '''
    with open ('secrets.json') as file:
        data = json.load(file)
        apikey = data['darkSkyAPIKEY']

    request_url = url.format(apikey, lat, lon)
    response = requests.get(request_url)
    if response.status_code >= 400:
        raise RuntimeError('Error with the request. Code:' + str(response.status_code))

    return response.json()

def todayForecast(lat, lon):
    '''
    Returns minimum and maximum temperatures,
    a weather summary and an icon for today's
    forecast at (lat, lon)
    '''
    data = downloadWeatherForecast(lat, lon)
    return data['daily']['data'][0]['temperatureMin'], data['daily']['data'][0]['temperatureMax'], data['hourly']['summary'], data['hourly']['icon']