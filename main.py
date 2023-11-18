import requests
import pandas as pd
from bs4 import BeautifulSoup

from_date = '07.10.2023'


def get_cities():
    url = "https://www.oref.org.il/Shared/Ajax/GetCitiesMix.aspx?lang=he"
    request = requests.get(url)
    jsonFormat = request.json()
    cities = set()
    area = {}
    for item in jsonFormat:
        cities.add(item['label_he'])
        soup = BeautifulSoup(item['mixname'], 'html.parser')
        value = soup.find('span').text
        area[item['label_he']] =value

    return cities, area


def get_data(cities, area):
    data_list = []
    for city in cities:
        url = 'https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate=' + from_date + '&toDate=&mode=0&city_0=' + city
        request = requests.get(url)
        request.raise_for_status()
        jsonFormat = request.json()
        for item in jsonFormat:
            if item.get('category_desc') == 'ירי רקטות וטילים':
                if ',' in item['data']:
                    data_values = item['data'].split(', ')
                    for data_value in data_values:
                        data_list.append({'alertDate': item['alertDate'], 'date': item['date'], 'time': item['time'],
                                          'city': data_value, 'area': area[city]})
                else:
                    data_list.append({'alertDate': item['alertDate'], 'date': item['date'], 'time': item['time'], 'city': item['data'], 'area': area[city]})
    df = pd.DataFrame(data_list)
    df.to_excel('lastRockets.xlsx', index=False)


if __name__ == '__main__':
    cities, area = get_cities()
    get_data(cities, area)
