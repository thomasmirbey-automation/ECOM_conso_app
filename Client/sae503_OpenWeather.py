import requests
import json
def get_city_data(city,APIkey):
    
    try:
        url = "http://api.openweathermap.org/data/2.5/weather?q="+str(city)+",fr&lang=fr&units=metric&APPID="+str(APIkey)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return(json.loads(response.text))
             
    except Exception as e:
        #print(e)
        return {}


def extract_city_data(dictionnaire):
    try:
        coord=dictionnaire['coord']
        #print(coord)
        weather=dictionnaire['weather'][0]
        #print(weather)
        main=dictionnaire['main']
        #print(main)
        return coord,weather,main
    
    except Exception as e:
        
        return 0,0,0
        
 
"""a=get_city_data("Paris","e5906fc1e4373743e5427b4675940341")

print(extract_city_data(a))"""