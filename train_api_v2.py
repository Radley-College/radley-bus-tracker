

import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

API = "https://api.transcapi.com/v1"
HEADERS = {"X-Api-Key": "16fd7fb95c60b8d4a117fde061b2bf13ea657772"}
UK = ZoneInfo("Europe/London")

def uk_time(iso):
    return datetime.fromisoformat(iso).astimezone(UK).strftime("%H:%M") if iso else "--:--"

class TRAINAPI:
    def __init__(self, station_start_id='RAD'):
        
        self.station_start_id = station_start_id
        
        self.params = {
            "from_offset": 0,
            "to_offset": 240,
            "limit": 100
        }
        
        self.board = requests.get(f"{API}/rail/station_timetables/{station_start_id}.json", headers=HEADERS, params=self.params).json()

    def __call__(self):
        
        all_train_data = ()
        
        for message in self.board.get("messages", []):
            print("!", message)
            
        for d in self.board["departures"]:
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
            
            if passes_oxford:
                time_str = uk_time(d['aimed_departure_time'])
                exp_time = f"exp {uk_time(d['expected_departure_time'])}"
                platform = f"plat {d['platform'] or '-':>3}"
                destination = d['destination']
                status = d['status']
                
                oxford_arr = "--:--"
                for stop in stops[oxford_index:]:
                    if stop.get("crs_code") == "OXF":
                        oxford_arr = uk_time(stop.get('expected_arrival_time') or stop.get('aimed_arrival_time'))
                        break
                
                arrival_string = f"arrival time: {oxford_arr}"
                
                single_train_tuple = (
                    time_str, 
                    exp_time, 
                    platform, 
                    destination, 
                    status, 
                    arrival_string
                )

                all_train_data += (single_train_tuple,)

        return all_train_data


if __name__ == "__main__":
    train_api = TRAINAPI(station_start_id='RAD')
    
    final_data = train_api()
    print(final_data)