import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


class BusAPI:
  def __init__(self, cache_duration=60):
    # Time in seconds before the cache expires
    self.cache_duration = cache_duration
    self.cached_times = None
    self.last_fetched = None

  def __fetch_data(self):
    """Fetches data from the remote source, and scrapes it into the cache"""
    url = "https://www.oxfordbus.co.uk/stops/340001182OPP"
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
    return bus_list

  def get_data(self):
    """Checks if the cache is fresh. Refreshes if needed. Returns the data."""
    now = datetime.now()
    if self.cached_times is None or (now - self.last_fetched) > timedelta(
        seconds=self.cache_duration
    ):
      self.cached_times = self.__fetch_data()
      self.last_fetched = now
    return self.cached_times

if __name__ == "__main__":
  api = BusAPI(cache_duration=60)
  while True:
    data = api.get_data()
    print(data)
    time.sleep(10)