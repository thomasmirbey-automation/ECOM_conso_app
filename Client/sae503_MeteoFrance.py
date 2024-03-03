from meteofrance_api import MeteoFranceClient
from meteofrance_api.model import Place


def test_forecast_france(lat,long):
    """Test weather forecast results from API."""
    client = MeteoFranceClient()

    weather_forecast = client.get_forecast(latitude=float(lat), longitude=float(long))
    """for element in weather_forecast.daily_forecast:
        print(element)"""
    return weather_forecast.daily_forecast

#print(test_forecast_france(48.8075,2.24028))