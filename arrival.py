"""Код телеграм-бота, который собирает необходимую информацию о прибытии рейсов и отправлет пользователю"""

#pip install requests bs4

import requests
from bs4 import BeautifulSoup
import json

url = "https://airportufa.ru/scoreboard/arrival/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.811 Yowser/2.5 Safari/537.36"
}

"""Функция-парсер. Собирает информацию о прибытии всех рейсов и сохраняет в json файле"""
def get_data(url):
    response = requests.get(url=url, headers=headers)
    with open("index.html", "w") as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all('a', class_='b-scoreboard-card')

    arrival_dict = {}     #словарь для записи информации о всех прибывающих рейсах

    """В блоке for считаваем с кода страницы необходимые для нас данные про каждый рейс и добавляем в словарь arrival_dict"""
    for card in cards:
        time = card.find('time', class_='text-primary').text.strip()
        city = card.find('div', class_='b-scoreboard-card__title').text.strip()
        url = f'https://airportufa.ru{card.get("href")}'
        status = card.find('div', class_='b-scoreboard-card__td_status').find('span', class_='b-scoreboard-card__info').text.strip()
        terminal = card.find('div', class_='b-scoreboard-card__td_terminal').find('span', class_='b-scoreboard-card__info').text.strip()

        id = url.split("/")[-2]     #id будем применять как ключ к элементу в ловаре arrival_dict

        arrival_dict[id] = {
            "time": time,
            "city": city,
            "url": url,
            "status": status,
            "terminal": terminal
        }

    with open('arrival_dict.json', 'w') as file:               #Записываем полученные данные в файл json
        json.dump(arrival_dict, file, indent=4, ensure_ascii=False)

"""Функция-парсер. Возвращает словарь только с ожидаемыми и отмененными рейсами. Исключает уже прибывшие рейсы"""
def check_update(url):

    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.811 Yowser/2.5 Safari/537.36"
    }

    url = "https://airportufa.ru/scoreboard/arrival/"
    response = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    cards = soup.find_all('a', class_='b-scoreboard-card')

    expected = {}        #словарь для записи информации о ожидаемых рейсах

    """В блоке for считаваем с кода страницы необходимые для нас данные про ожидаемые рейсы и добавляем в словарь expected"""
    for card in cards:
        status = card.find('div', class_='b-scoreboard-card__td_status').find('span', class_='b-scoreboard-card__info').text.strip()

        if status == "Прилетел":
            continue
        else:
            time = card.find('time', class_='text-primary').text.strip()
            city = card.find('div', class_='b-scoreboard-card__title').text.strip()
            url = f'https://airportufa.ru{card.get("href")}'
            status = card.find('div', class_='b-scoreboard-card__td_status').find('span', class_='b-scoreboard-card__info').text.strip()
            terminal = card.find('div', class_='b-scoreboard-card__td_terminal').find('span', class_='b-scoreboard-card__info').text.strip()

            id = url.split("/")[-2]    #id будем применять как ключ к элементу в ловаре expected

            expected[id] = {
                "time": time,
                "city": city,
                "url": url,
                "status": status,
                "terminal": terminal
            }

    return expected

def main():
    print('Запуск парсера...')
    get_data(url)

if __name__ == "__main__":
    main()