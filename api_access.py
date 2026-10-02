import json
import requests
import csv
import os

print(os.getcwd())

place = input("Please enter your station")
gazetteer_id = ''
atco_area_code = ''
administrativeareacode = ''
locality_code = ''

all_api_key = ["83e28b77f9fbea2f10bf45cccc88d7dcaab9b9e4", "9c22cc6cf07837921f40bd189d76ec9a7c28314a"]

api_key_used = all_api_key[1]

#requests
bus_location_request = requests.get(f"https://data.bus-data.dft.gov.uk/api/v1/datafeed/?api_key={api_key_used}")
dataset_id_request = requests.get(f"https://data.bus-data.dft.gov.uk/api/v1/dataset/?adminArea=340&noc=OXBC&status=published&limit=25&offset=0&api_key={api_key_used}")
fares_request = requests.get(f"https://data.bus-data.dft.gov.uk/api/v1/fares/dataset/?api_key={api_key_used}")
bus_stop_request = requests.get(f"https://naptan.api.dft.gov.uk/v1/access-nodes?atcoAreaCodes={atco_area_code}&dataFormat=csv")


#print(bus_stop_request.text)
print(bus_location_request)

data_set = dataset_id_request.json()
fares = fares_request.json()
#bus_location = bus_location_request.json()





#list: "company name", "noc"
noc_list = [
    ["Blackpool Transport", "BLAC"],
    ["AC Williams", "WMSA"],
    ["Pilkingtonbus", "NWBT"],
    ["Phil Haines Coaches", "HAIN"],
    ["Panther Travel", "PNTR"],
    ["Tanat Valley Coaches", "TANV"],
    ["Nu-Venture", "NVTR"]
]






for option in data_set["results"]: 
    for value in option["localities"]:
        if value["name"].lower() == place.lower():
            gazetteer_id = value["gazetteer_id"]
            #print(gazetteer_id)
            #print(option["operatorName"], option["noc"])

with open('data/Localities.csv', newline='', encoding='utf-8') as f:
    data = csv.reader(f)
    
    
    #check what number each header correspond to in the Localities.csv file
    """header = next(atco_data)
    for number, name in enumerate(header):
        print(number, name)"""
    
     
    for row in data:
        if row[0] == gazetteer_id:
            administrativeareacode = row[11]
            locality_code = row[0]
            
            print("Station:", row[1])
            print("Locality code:", row[0])
            print(row[11])
            




#print data_set.results
"""for option in data_set["results"]:
    print(option)"""


#print noc and location
"""for value in fares["results"]:
    for noc in value["noc"]:
        print(noc, value["description"])"""
        
        
print(gazetteer_id)