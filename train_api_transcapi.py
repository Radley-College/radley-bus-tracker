

import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

station = input()
station_start_id = 'RAD'
station_end_id = ''
trip_id = []
train_arrival_time = []


params = {
    "from_offset": 0,
    "to_offset": 240,
    "limit": 100
}


API = "https://api.transcapi.com/v1"
HEADERS = {"X-Api-Key": "16fd7fb95c60b8d4a117fde061b2bf13ea657772"}
UK = ZoneInfo("Europe/London")

def uk_time(iso):
    return datetime.fromisoformat(iso).astimezone(UK).strftime("%H:%M") if iso else "--:--"


board = requests.get(f"{API}/rail/station_timetables/{station_start_id}.json", headers=HEADERS, params=params).json()

def train_schedule():
    for message in board["messages"]:
        print("!", message)
        
    for d in board["departures"]:
        service_id = d["trip_id"]
        response = requests.get(f"{API}/rail/services/{service_id}.json", headers=HEADERS)
            
        response.raise_for_status()
        train_data = response.json()
        
        stops = train_data.get("calls", [])
        radley_index = next(
            (
                i for i, stop in enumerate(stops)
                if stop.get("crs_code") == "RAD"
            ),
            None
        )
        oxford_index = next(
            (
                i for i, stop in enumerate(stops)
                if stop.get("crs_code") == "OXF"
            ),
            None
        )
        
        passes_oxford = (
            radley_index is not None
            and oxford_index is not None
            and oxford_index > radley_index
        )
        
        
        """passes_oxford = any(
            stop.get("name", "").strip().lower() == "oxford"
            for stop in stops
        )"""
        
        
        if passes_oxford:
            trip_id.append(service_id)
            train_arrival_time.append(uk_time(d['aimed_departure_time']))
            note = d["cancel_reason"] or d["delay_reason"] or ""
            
            print(
            f"{uk_time(d['aimed_departure_time'])}  "
            f"exp {uk_time(d['expected_departure_time'])}  "
            f"plat {d['platform'] or '-':>3}  "
            f"{d['destination']:<24} "
            f"{d['status']:<9} {note}"
        )

        
        """if d["destination"] in ["Oxford", "Banbury"]:
            trip_id.append(d["trip_id"])
            train_arrival_time.append(uk_time(d["aimed_departure_time"]))  
            note = d["cancel_reason"] or d["delay_reason"] or ""
            print(f"{uk_time(d['aimed_departure_time'])}  exp {uk_time(d['expected_departure_time'])}  "
                f"plat {d['platform'] or '-':>3}  {d['destination']:<24} {d['status']:<9} {note}")"""



def follow_up(trip_id):
    train_following = input("Please enter the aimed departure time of your train").strip()
    hour, minute =  train_following.split(":")
    train_following = f"{int(hour):02d}:{int(minute):02d}"
    station_arrive = input("Please enter the station you want to arrive at")
    
    for count, time in enumerate(train_arrival_time):
        if time == train_following:
            follow_up = requests.get(f"{API}/rail/services/{trip_id[count]}.json", headers=HEADERS)
            follow_up.raise_for_status()
            train_data = follow_up.json()
            
            stops = train_data.get("calls", [])
            for stop in stops:
                if stop.get("name", "").lower() == station_arrive.lower():
                    print(f"station:{stop['name']},", "exp arrival time:", uk_time(stop['aimed_arrival_time']))
        
train_schedule()
follow_up(trip_id)

    
