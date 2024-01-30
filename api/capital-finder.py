from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        url = urlparse(self.path)
        query_params = parse_qs(url.query)

        if 'country' in query_params:
            country_name = query_params['country'][0]
            capital = self.get_country_capital(country_name)
            if capital:
                response_message = f"The capital of {country_name} is {capital}."
            else:
                response_message = f"Country '{country_name}' not found."
        elif 'capital' in query_params:
            capital_name = query_params['capital'][0]
            country = self.get_country_by_capital(capital_name)
            if country:
                response_message = f"{capital_name} is the capital of {country}."
            else:
                response_message = f"Capital '{capital_name}' not found."
        else:
            response_message = "Please provide either 'country' or 'capital' query parameter."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))

    def get_country_capital(self, country_name):
        try:
            response = requests.get(f"https://restcountries.com/v3/name/{country_name}")
            if response.status_code == 200:
                data = response.json()
                return data[0]['capital']
            else:
                return None
        except Exception as e:
            return None

    def get_country_by_capital(self, capital_name):
        try:
            response = requests.get(f"https://restcountries.com/v3/capital/{capital_name}")
            if response.status_code == 200:
                data = response.json()
                return data[0]['name']['common']
            else:
                return None
        except Exception as e:
            return None
