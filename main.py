from time import sleep

import requests
import pandas as pd

from_date = '07.10.2023'


def get_cities():
    url = "https://www.oref.org.il/Shared/Ajax/GetCitiesMix.aspx?lang=he"
    request = requests.get(url)
    jsonFormat = request.json()
    cities = []
    for item in jsonFormat:
        cities.append(item['label_he'])
    return cities


def get_data(cities):
    data_list = []
    for city in cities:
        url = 'https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=he&fromDate=' + from_date + '&toDate=&mode=0&city_0=' + city
        request = requests.get(url)
        request.raise_for_status()
        jsonFormat = request.json()
        print(jsonFormat)
        for item in jsonFormat:
            if item.get('category_desc') == 'ירי רקטות וטילים':
                if ',' in item['data']:
                    data_values = item['data'].split(', ')
                    for data_value in data_values:
                        data_list.append({'alertDate': item['alertDate'], 'date': item['date'], 'time': item['time'],
                                          'city': data_value})
                else:
                    data_list.append({'alertDate': item['alertDate'], 'date': item['date'], 'time': item['time'], 'city': item['data']})
    df = pd.DataFrame(data_list)
    df.to_excel('lastRockets.xlsx', index=False)


if __name__ == '__main__':
    cities = get_cities()
    get_data(cities)
