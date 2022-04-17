from random import randint
import requests


def get_random_comix_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    xkcd_data = response.json()
    return randint(1, xkcd_data['num'])


def get_comix_picture(random_number):
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()

    xkcd_data = response.json()

    return xkcd_data['img'], xkcd_data['alt']


def download_picture(url, filename, params={}):
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
