import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os
import pickle

class BusAPI:
    def __init__(self, cache_duration=60):
        self.cache_duration = cache_duration
        self.cached_times = None
        self.last_fetched = datetime.now()
        file_path = "Saved_Bus_Times.pkl"
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                self.cached_times = pickle.load(file)
        else:
            with open(file_path, "wb") as file:
                timescache = self.__fetch_data()
                pickle.dump(timescache, file)
                self.cached_times = timescache

    def __fetch_data(self):
        url = "https://www.oxfordbus.co.uk/stops/340001182OUT"
        response = requests.get(url)
        bus_list = []
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        base_time = datetime.now()
        bus_time = soup.find_all(
            "div", {"class": "single-visit__arrival-time__cell"}
        )
        for item in bus_time:
            text = item.get_text(strip=True)
            if "mins" in text:
                minutes = int(text.split()[0])
                departure = base_time + timedelta(minutes=minutes)
                bus_list.append(departure.strftime("%H:%M"))
            else:
                bus_list.append(text)
        bus_arrive_times = []
        george_arrival_times = []
        bus_links = soup.find_all(
            "a", {"class": "single-visit"}
        )
        for link in bus_links:
            url_two = "https://www.oxfordbus.co.uk" + link["href"]
            responsetwo = requests.get(url_two)
            response_text_two = responsetwo.text
            souptwo = BeautifulSoup(response_text_two, "html.parser")

            bus_time_two = souptwo.find_all(
                "button", {"class": "journey-list__button", "data-atcocode": "340001182OUT"}
            )
            for item in bus_time_two:
                text = item.get_text()
                time_str = text.split()[0]
                bus_arrive_times.append(time_str)
            george_time_two = souptwo.find_all(
                "button", {"class": "journey-list__button", "data-atcocode": "340000864B1"}
            )
            for item in george_time_two:
                text = item.get_text()
                time_str = text.split()[0]
                george_arrival_times.append(time_str)
        return bus_arrive_times, george_arrival_times

    def get_data(self, walk=False):
        now = datetime.now()
        if self.cached_times is None or (now - self.last_fetched) > timedelta(
                seconds=self.cache_duration
        ):
            self.cached_times = self.__fetch_data()
            self.last_fetched = now
        bus_arrive_times, george_arrival_times = self.cached_times
        if walk:
            adjusted_bus = []
            for t in bus_arrive_times:
                dt = datetime.strptime(t, "%H:%M")
                new_dt = dt - timedelta(minutes=7)
                adjusted_bus.append(new_dt.strftime("%H:%M"))
            adjusted_george = []
            for t in george_arrival_times:
                dt = datetime.strptime(t, "%H:%M")
                new_dt = dt + timedelta(minutes=5)
                adjusted_george.append(new_dt.strftime("%H:%M"))
            return adjusted_bus, adjusted_george
        return bus_arrive_times, george_arrival_times


if __name__ == "__main__":
    api = BusAPI(cache_duration=60)
    while True:
        data = api.get_data(walk=True)
        print(data)
        time.sleep(10)