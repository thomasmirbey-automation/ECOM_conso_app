import requests
from datetime import datetime

def get_NASA_data(url,lat,long,start_date,end_date,api_key):
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

    latitude = float(lat)
    longitude = float(long)
    start_date = str(start_date) 
    end_date = str(end_date)

    parameters = "T2M,RH2M,ALLSKY_SFC_SW_DWN"

    response_format = "json"

    params = {
        "start": start_date,
        "end": end_date,
        "latitude": latitude,
        "longitude": longitude,
        "community": "sb",  
        "parameters": parameters,
        "format": response_format,
        "user": "ThomasM2568",  
        "header": True,
        "time-standard": "lst", 
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, params=params, headers=headers)

    if (response.status_code == 200):
        #print(response.json())
        #print(f"Error: {response.status_code}")
        #print(response.text)
        # Extract the values for "All Sky Surface Shortwave Downward Irradiance"
        irradiance_values = response.json()['properties']['parameter']['ALLSKY_SFC_SW_DWN']

        d={}
        for timestamp, value in irradiance_values.items():
            #formatted_date=timestamp
            #data in W/m²
            # Parse the string into a datetime object
            parsed_date = datetime.strptime(str(timestamp), "%Y%m%d%H")

            # Format the datetime object as "YYYY/MM-DD - HH:MM"
            formatted_date = parsed_date.strftime("%Y/%m/%d - %H:%M")
            d[str(formatted_date)]=value
        return d
    else:
        return 0




'''
api_key = " MT3OO5rAXdt2JNwI75yCNc20mwIhuIkXtPqpUreI"

url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

lat = 40.7128  
long = -74.0060

start_date = "20220101" 
end_date = "20220102"  # Example end date (YYYYMMDD)

#start_date = "20231129" 
#end_date = "20231130"
print(get_NASA_data(url,lat,long,start_date,end_date,api_key))'''