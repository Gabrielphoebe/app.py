from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration for external APIs
IPSTACK_API_KEY = 'your_ipstack_api_key'
OPENWEATHER_API_KEY = 'your_openweather_api_key'


def get_location(ip):
    response = requests.get(f'http://api.ipstack.com/{ip}?access_key={IPSTACK_API_KEY}')
    data = response.json()
    return data['city']


def get_weather(city):
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric')
    data = response.json()
    return data['main']['temp']


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'Visitor')
    client_ip = request.remote_addr

    # For local testing, replace client_ip with a known IP address.
    if client_ip == '127.0.0.1':
        client_ip = 'your_test_ip_address'

    location = get_location(client_ip)
    temperature = get_weather(location)

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}"
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
