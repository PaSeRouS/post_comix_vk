import os

from dotenv import load_dotenv

from picture_functions import download_picture, get_picture, get_random_number
from vk_api_functions import post_picture_to_vk


if __name__ == '__main__':
    load_dotenv()

    vk_token = os.getenv('VK_TOKEN')
    version = 5.131
    filename = 'comix.png'

    random_number = get_random_number()
    img_data, alt_text = get_picture(random_number)

    download_picture(img_data, filename)
    post_picture_to_vk(filename, vk_token, version, alt_text)
    os.remove(filename)
