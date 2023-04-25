import requests
# import json

API_KEY = "4ca1e300971635777c09ef709a23276b"

async def get_weather_temp(lat: str, lon: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&lang=ru" % (lat, lon, API_KEY)
    answer = 'Сервис в данный момент не доступен'
    try:
        response = requests.get(url)
    except:
        return answer
    else:
        result = response.json()
        try:
            current = result['weather'][0]["description"]
        except:
            return answer
        else:
            return str(current)