import requests
import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.getenv("API_WEATHER_KEY")  # Replace YOUR_API_KEY with your API key



class API_Weather:
    """
    A class to fetch weather data for a specified city using the OpenWeatherMap API.

    This class provides a method to retrieve weather information, which includes
    temperature, humidity, wind speed, and other relevant weather details for a given city.

    Methods:
        get_weather_data(city): Fetches weather data for the specified city and returns it as a dictionary
            containing:
            - City (str): Name of the city.
            - Country (str): Country code of the city.
            - Temperature (float): Current temperature in Celsius.
            - Feels like (float): Feels-like temperature in Celsius.
            - Min Temperature (float): Minimum temperature in Celsius.
            - Max Temperature (float): Maximum temperature in Celsius.
            - Humidity (int): Humidity percentage.
            - Weather (str): Description of the weather.
            - Wind Speed (float): Wind speed in meters per second.
            - Cloudiness (int): Cloudiness percentage.
            - Visibility (int): Visibility in meters.
    """
    
    def __init__(self):
        """Initializes the API_Weather class."""
        pass
    
    def __kelvin_to_celsius(self,kelvin):
        """
        Converts temperature from Kelvin to Celsius.

        Args:
            kelvin (float): Temperature in Kelvin.

        Returns:
            float: Temperature in Celsius.
        """
        return kelvin - 273.15
    def get_weather_data(self, city):
        """
        Fetches weather data for a specified city.

        Args:
            city (str): The name of the city for which to retrieve weather data.

        Returns:
            dict: A dictionary containing weather information, including:
                - City
                - Country
                - Temperature
                - Feels like temperature
                - Min Temperature
                - Max Temperature
                - Humidity
                - Weather
                - Wind Speed
                - Cloudiness
                - Visibility
        """
        url = f"{BASE_URL}appid={API_KEY}&q={city}"
        response = requests.get(url=url).json()
        city_name = response.get("name")
        country = response.get("sys", {}).get("country")
        temperature = self.__kelvin_to_celsius(response.get("main", {}).get("temp", 0))
        feels_like = self.__kelvin_to_celsius(response.get("main", {}).get("feels_like", 0))
        temp_min = self.__kelvin_to_celsius(response.get("main", {}).get("temp_min", 0))
        temp_max = self.__kelvin_to_celsius(response.get("main", {}).get("temp_max", 0))
        humidity = response.get("main", {}).get("humidity")
        weather_description = response.get("weather", [{}])[0].get("description")
        wind_speed = response.get("wind", {}).get("speed")
        cloudiness = response.get("clouds", {}).get("all")
        visibility = response.get("visibility")

        return {
            "City": city_name,
            "Country": country,
            "Temperature": round(temperature, 2),
            "Feels like": round(feels_like, 2),
            "Min Temperature": round(temp_min, 2),
            "Max Temperature": round(temp_max, 2),
            "Humidity": humidity,
            "Weather": weather_description,
            "Wind Speed": wind_speed,
            "Cloudiness": cloudiness,
            "Visibility": visibility
        }
