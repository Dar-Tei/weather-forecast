import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class WeatherAPIFacade:
    """
      A class that serves as a facade to the OpenWeatherMap API for getting weather forecast data.

      Args:
          api_key (str): The API key to use when making requests to the OpenWeatherMap API.

      Attributes:
          API_URL (str): The base URL of the OpenWeatherMap API.
          api_key (str): The API key to use when making requests to the OpenWeatherMap API.

      Methods:
          get_forecast(city_name, language): Gets the weather forecast data for a given city and language.
          _parse_en(data): Parses the forecast data for the English language.
          _parse_ua(data): Parses the forecast data for the Ukrainian language.
          _deg_to_dir(degrees, language): Converts wind direction in degrees to a cardinal direction.
      """

    API_URL = 'http://api.openweathermap.org/data/2.5/forecast'

    def __init__(self, api_key):
        """
            Initializes an instance of the WeatherAPIFacade class with the given API key.

            Args:
                api_key (str): The API key to use when making requests to the OpenWeatherMap API.
        """

        self.api_key = api_key

    def get_forecast(self, city_name, language):
        """
            Gets the weather forecast data for a given city and language.

            Args:
                city_name (str): The name of the city for which to get the weather forecast data.
                language (str): The language code for which to display the weather forecast data.

            Returns:
                str: A string containing the parsed weather forecast data.
        """

        url = f'{self.API_URL}?q={city_name}&appid={self.api_key}&lang={language}&units=metric'
        response = requests.get(url)
        response_data = response.json()
        forecast_data = response_data['list']
        city_data = response_data['city']
        city_name = city_data['name']
        forecast = []
        logging.info(city_name + ":")
        if language == "ua":
            for data in forecast_data:
                forecast.append(self._parse_ua(data))
        else:
            for data in forecast_data:
                forecast.append(self._parse_en(data))
        return '\n'.join(forecast)

    def _parse_ua(self, data):
        """
            Parses the forecast data for the Ukrainian language.

            Args:
                data (dict): The forecast data item to parse.

            Returns:
                str: A string containing the parsed forecast data for the Ukrainian language.
        """
        
        date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date_str = date.strftime('%d.%m.%Y')
        temp = data['main']['temp']
        clouds = data['weather'][0]['description']
        wind_dir = self._deg_to_dir(data['wind']['deg'], language="ua")
        return f'\nДата: {date_str}, Температура: {temp}°C, Хмарність: {clouds}, Напрямок вітру: {wind_dir}'

    def _parse_en(self, data):
        """
            Parses the forecast data for the English language.

            Args:
                data (dict): The forecast data item to parse.

            Returns:
                str: A string containing the parsed forecast data for the English language.
        """
        
        date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date_str = date.strftime('%d-%m-%Y')
        temp = data['main']['temp']
        clouds = data['weather'][0]['description']
        wind_dir = self._deg_to_dir(data['wind']['deg'], language="en")
        return f'\nDate: {date_str}, Temperature: {temp}°C, Cloud Cover: {clouds}, Wind Direction: {wind_dir}'

    @staticmethod
    def _deg_to_dir(degrees, language="en"):
        """
           Converts wind direction from degrees to compass direction.

           Args:
               degrees (float): Wind direction in degrees.
               language (str): Language code (default: "en").

           Returns:
               str: Compass direction.
        """

        if language == "ua":
            compass = ['Пн', 'Пн.Сх', 'Сх', 'Пв.Сх', 'Пв.', 'Пв.Зх', 'Зх', 'Пн.Зх']
        else:
            compass = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = int((degrees / 45) + 0.5) % 8
        return compass[index]


if __name__ == '__main__':
    api_key = input('Enter API key: ')
    city_name = input('Enter city name: ')
    language = input('Enter language code (e.g. "en" for English): ')
    weather_api = WeatherAPIFacade(api_key)
    forecast = weather_api.get_forecast(city_name, language)
    logging.info(forecast)
