import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timedelta
from bus_scraper import BusAPI
#class scrape_class:
    #def get_times(live=True):
        #if live:
            #url = "https://www.oxfordbus.co.uk/stops/340001182OPP"
            #response = requests.get(url)
            #print(response.status_code)   # 200 = success
            #print(response.text[:500])    # peek at the raw HTML
            #return response.text
        #else:
            #p = Path("busses.txt")
            #print(p.exists())
            #print(p.is_file())
            #print(p.read_text())
            #with p.open() as f:
                #response = f.read()
            #print("It's local")
        #return response
    #response_text = get_times()
    #soup = BeautifulSoup(response_text, "html.parser")
    #links = soup.find_all("li", {"class": "departure-board__item"})
    #print(len(links),"different busses")
    # loop starts here

    #base_time = datetime.strptime("15:45", "%H:%M")
    #base_time = datetime.now()
    #bus_time = soup.find_all("div", {"class": "single-visit__arrival-time__cell"})
    #def format_time(bus_time, base_time):
        #for item in bus_time:
            #text = item.get_text(strip=True)
            #if "mins" in text:
                #minutes = int(text.split()[0])
                #departure = base_time + timedelta(minutes=minutes)
                #print(departure.strftime("%H:%M"))
            #else:
                #print(text)
    #link = links[0]
    #print(format_time(bus_time, base_time))
    #print(link)

if __name__ == "__main__":
    api = BusAPI()
    print(api.get_data())