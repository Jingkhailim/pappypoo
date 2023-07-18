import requests
import time
import csv
import os
print("Current working directory:", os.getcwd())
urls= ["http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=CCL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=CEL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=CGL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=DTL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=EWL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=NEL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=NSL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=BPL",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=SLRT",
       "http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime?TrainLine=PLRT"]

# import csv
coordinates_mrt = []
with open('mrtsg.csv','r') as file:
    reader = csv.reader(file)
    for i in reader:
        coordinates_mrt.append([i[2],i[5],i[6]])
# print(coordinates_mrt)

payload = {}
headers = {
  'AccountKey': 'obIam575TG64JvFfa1M7Tw==',
  'Accept': 'application/json', 

}
file = open('testing.txt','a')
allasabove=[]

# Python 3 program for the
# haversine formula
import math
 

def fetch_weather_data():
    url = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data.")
        return None

def extract_data(response_data):
    data = []
    for item in response_data['area_metadata']:
        name = item['name']
        latitude = item['label_location']['latitude']
        longitude = item['label_location']['longitude']
        forecast = None
        for forecast_item in response_data['items'][0]['forecasts']:
            if forecast_item['area'] == name:
                forecast = forecast_item['forecast']
                break
        data.append([name, latitude, longitude, forecast])
    return data



# Python 3 program for the
# haversine formula
def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c



for url in urls:
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.status_code)
    json_data = response.json()
    value_list = json_data['value']
    print(value_list)
    time.sleep(3)
    # print(str(value_list))
    # print(type(str(value_list)))
    # allasabove.append(value_list)
    # with open("examples.csv", mode='a', newline='') as file:
    #   writer = csv.writer(file)
    #   for i in value_list:

    #      writer.writerow([i['Station'],i['StartTime'],i['EndTime'],i['CrowdLevel']])
    with open("examples.csv", mode='a', newline='') as file:
      writer = csv.DictWriter(file,fieldnames=['Station','StartTime','EndTime','CrowdLevel','X','Y','Weather','Area'])
      for i in value_list:
          for o in coordinates_mrt:
              
              if i['Station']==o[0]:
                  i['X'],i['Y']=float(o[1]),float(o[2])

                  lat1,lon1=float(o[1]),float(o[2])
                  # print("Initial:",o[1],o[2])
                  smallest_distance = 0
                  counter = 0
                  weather = 'ERROR'
                  areasss = ''


                  weather_data = fetch_weather_data()
                  if weather_data:
                    extracted_datas = extract_data(weather_data)
                    # save_to_csv(extracted_data)
                    # print(extracted_datas)
                    # print("Data successfully scraped and saved to weather_forecast.csv")
                    for n in extracted_datas:
                        if counter==0:
                                # print(n[1],n[2])
                                lat2 = n[1]
                                lon2 = n[2]
                                
                                smallest_distance = haversine(lat1, lon1,lat2, lon2)
                                weather = n[3]
                                areasss=n[0]
                                counter+=1
                        else:
                            lat2 = n[1]
                            lon2 = n[2]
                            new_distance = haversine(lat1, lon1,lat2, lon2)
                            if smallest_distance > new_distance:
                                weather = n[3]
                                smallest_distance=new_distance
                                areasss=n[0]
                    i['Weather'] = weather
                    i['Area']=areasss
                    break

          writer.writerow(i)

          
        #  writer.writerow([i['Station'],i['StartTime'],i['EndTime'],i['CrowdLevel']])
# file.write("{}\n".format(allasabove))



# print(response.text)