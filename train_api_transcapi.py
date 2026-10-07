

import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

station = input()
station_start_id = 'RAD'
station_end_id = ''
trip_id = []
train_arrival_time = []

API = "https://api.transcapi.com/v1"
HEADERS = {"X-Api-Key": "16fd7fb95c60b8d4a117fde061b2bf13ea657772"}
UK = ZoneInfo("Europe/London")

def uk_time(iso):
    return datetime.fromisoformat(iso).astimezone(UK).strftime("%H:%M") if iso else "--:--"


board = requests.get(f"{API}/rail/station_timetables/{station_start_id}.json", headers=HEADERS).json()

for message in board["messages"]:
    print("!", message)
for d in board["departures"]:
    if d["destination"] in ["Oxford", "Banbury"]:
        trip_id.append(d["trip_id"])
        train_arrival_time.append(uk_time(d["aimed_departure_time"]))  
        note = d["cancel_reason"] or d["delay_reason"] or ""
        print(f"{uk_time(d['aimed_departure_time'])}  exp {uk_time(d['expected_departure_time'])}  "
            f"plat {d['platform'] or '-':>3}  {d['destination']:<24} {d['status']:<9} {note}")

def follow_up(trip_id):
    train_following = input("Please enter the aimed departure time of your train")
    count = 0
    for time in train_arrival_time:
        if time == train_following:
            follow_up = requests.get(f"{API}/rail/services/{trip_id[count]}.json", headers=HEADERS).json()
            print(follow_up)
        count += 1
        
#follow_up(trip_id)
            
    
    
    
