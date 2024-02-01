from flask import Flask, jsonify, render_template, request
import requests
import os
import yaml
from dotenv import load_dotenv

load_dotenv()  # 讀取環境資料

app = Flask(__name__)
app.config['SECRET_KEY'] = '#92$-5+zz6q&)gv%5g+5(j1ho#3(%oh=i4hg9+^o!jhwwhxvta'


@app.route('/')
def index():
    return "Welcome to Weather API"


@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e),
        "description": "The server encountered an internal error and was unable to complete your request."
    }
    return jsonify(response), 500


@app.route('/api/locations', endpoint='locations-endpoint')
def locations():
    location_data = parse_swagger_yaml_locations()
    return jsonify(location_data)


@app.route('/api/weather/test', endpoint='test-endpoint')
def fetch_weather_data_test():
    weather_data = fetch_weather_data('臺南市')
    return jsonify(weather_data)


@app.route('/api/weather/<locationname>', methods=['GET', 'POST'], endpoint='weather-endpoint')
def weather(locationname):
    weather_data = fetch_weather_data(locationname)
    return jsonify(weather_data)


@app.route('/weather-page', methods=['GET', 'POST'], endpoint='weather-page-endpoint')
def weather_page():
    selected_location = '臺南市'
    if request.method == 'POST':
        selected_location = request.form.get('location')

    weather_data = fetch_weather_data(selected_location)
    return render_template('weather.html',
                           locations=weather_data['records']['location'],
                           location_name=selected_location
                           )


def fetch_weather_data(locationname):
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = os.getenv("WEATHER_URL")

        # 檢查環境變數是否正確設定
        if not api_key or not url:
            raise ValueError(
                "The API key or URL is not set in the environment variables.")

        # 將授權金鑰加入到請求標頭中
        headers = {
            'Authorization': api_key
        }
        params = {
            'format': 'JSON',
            'locationName': locationname
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"HTTP error": str(http_err)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def parse_swagger_yaml_locations():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    yaml_file_path = os.path.join(current_directory, 'v1.yaml')
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        swagger_data = yaml.safe_load(file)
        locations = swagger_data['paths']['/v1/rest/datastore/F-C0032-001']['get']['parameters']
        for param in locations:
            if param['name'] == 'locationName':
                return param['items']['enum']
    return []


if __name__ == '__main__':
    app.run(debug=True)
