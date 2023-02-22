import requests
from datetime import datetime


class WeatherAPIFacade:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_forecast(self, city_name, language):
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.api_key}&lang={language}&units=metric'
        response = requests.get(url)
        response_data = response.json()
        forecast_data = response_data['list']
        city_data = response_data['city']
        city_name = city_data['name']
        forecast = []
        print(city_name + ":")
        if language == "ua":
            for data in forecast_data:
                date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
                date_str = date.strftime('%d.%m.%Y')
                temp = data['main']['temp']
                clouds = data['weather'][0]['description']
                wind_dir = self.deg_to_dir(data['wind']['deg'])
                forecast.append(f'\nДата: {date_str}, Тепература: {temp}°C, Хмарність: {clouds}, Напрямок вітру: {wind_dir}')
        else:
            for data in forecast_data:
                date = datetime.strptime(data['dt_txt'], '%Y-%m-%d %H:%M:%S')
                date_str = date.strftime('%d-%m-%Y')
                temp = data['main']['temp']
                clouds = data['weather'][0]['description']
                wind_dir = self.deg_to_dir(data['wind']['deg'])
                forecast.append(f'\nDate: {date_str}, temperature: {temp}°C, cloud cover: {clouds}, wind direction: {wind_dir}')
        return '\n'.join(forecast)

    @staticmethod
    def deg_to_dir(degrees):
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
    print(forecast)
