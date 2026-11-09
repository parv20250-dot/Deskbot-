import httpx

CODES= {0:"clear sky",1:"mostly clear",2:"partly cloudy",3:"overcast",45:"fog",
    48:"fog",51: "light drizzle",53:"drizzle",55:"heavy drizzle",61:"light rain",
    63: "rain",65:"heavy rain",71:"light snow",73:"snow",75:"heavy snow",80:"rain showers",
    81:"rain showers",82:"heavy showers",95:"thunderstorm",96:"thunderstorm with hail",
    99: "thunderstorm with hail"} #wmo codes
def weather(city): #dunction for weather in city
    weather_r = httpx.get("https://geocoding-api.opne-mateo.com/v1/search",
                          params={"name":city,"count":1}) #coordinates
    if not weather_r.get("results"):
        return "no city try again :((" #no coordinates found return
    place = weather_r["results"][0]
    data = httpx.get("https://api.open-mateo.com/v1/forecast", params={
        "latitude": place ["latitude"], "longitude": place["longitude"],
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
"daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
"forecast_days": 2,"timezone": "auto"}, timeout=10).json()
    #input for weather app, 2m above ground level, feels like, what it is (code above)
    #wind speed, max min and precip, forecast for 2 days, nun in 10 timeout
    current = data["current"] #current weather section
    day = data["daily"]#of day
def weather_res(i):
    code= day["weather code"][i]
    weather = CODES.get(code,"unknown")
    low = day["temperature_2m_min"][i]
    high = day["temperature_2m_max"][i]
    rain = day ["precipitation_sum"][i] #defines necessary data
    result =weather +","+str(low)+"-"+str(high)+"C,"+"rain:"+str(rain)+"mm"
    return result


    
    