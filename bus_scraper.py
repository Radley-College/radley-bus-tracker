import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timedelta

class BusAPI:
    def __init__(self):
        pass
    def __fetch_data(self):
        """Fetches data from the remote source, and scrapes it into the cache"""
        url = "https://www.oxfordbus.co.uk/stops/340001182OPP"
        response = requests.get(url)
        #print(response.status_code)  # 200 = success
        #print(response.text[:500])  # peek at the raw HTML
        bus_list = []
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        links = soup.find_all("li", {"class": "departure-board__item"})
        base_time = datetime.now()
        bus_time = soup.find_all("div", {"class": "single-visit__arrival-time__cell"})
        for item in bus_time:
            text = item.get_text(strip=True)
            if "mins" in text:
                minutes = int(text.split()[0])
                departure = base_time + timedelta(minutes=minutes)
                bus_list.append(departure.strftime("%H:%M"))
            else:
                bus_list.append(text)
        # fetch from remote
        # clean & standardise
        # store to cache EVENTUALLY
        return bus_list
    def get_data(self):
        """Checks if the cache is fresh. Refreshes if needed. Returns the data."""

        data = self.__fetch_data()
        return data

if __name__ == "__main__":
    api = BusAPI()
    data = api.get_data()
    print(data)