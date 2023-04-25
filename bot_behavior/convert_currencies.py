import requests

API_KEY = '6wM6hi6LPdzTLAogKxhKOu6UDVAgmlLw'

async def get_converted_currency(currency: str = 'USD') -> str:
    url = "https://api.apilayer.com/exchangerates_data/convert?to=USD&from=" + currency + "&amount=1"
    answer = 'Сервис в данный момент не доступен'

    payload = {}
    headers= {
      "apikey": "6wM6hi6LPdzTLAogKxhKOu6UDVAgmlLw"
    }
    try:
        response = requests.request("GET", url, headers=headers, data = payload)
    except:
        return answer
    else:
        # status_code = response.status_code
        result = response.json()
        print(result)
        return str(result['result'])
