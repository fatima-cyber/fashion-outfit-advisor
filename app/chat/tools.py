import os
from langchain_core.tools import tool
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.tools import tool

# Get the OpenWeatherMap API key from environment variables
openweathermap_api_key = os.environ["OPENWEATHERMAP_API_KEY"]

# Define a tool for getting weather information
@tool
def get_weather(location: str) -> str:
    """Gets the weather in a given location.

    Args:
        location: A string representing the location for which to retrieve weather information.
                  The format should be "city,country" (e.g., "London,UK", "Paris,FR", "Milan,IT").
                  Do not use "United States" as the country name or state abbreviations like "OH" or "PA".
                  For US locations, use the city name followed by "US" (e.g., "New York,US", "Los Angeles,US").
                  The location string is case-insensitive, but using proper capitalization is recommended for clarity.

    Returns:
        A string containing the current weather information for the specified location.
        This includes details such as temperature, humidity, wind speed, and general weather conditions.

    Raises:
        ValueError: If the location string is not in the correct format or if the location is not found.
    """

    # Create an instance of OpenWeatherMapAPIWrapper
    weather = OpenWeatherMapAPIWrapper()
    return weather.run(location)

# Define a list of available tools; 
# #TODO: add custom tools
tools = [get_weather]