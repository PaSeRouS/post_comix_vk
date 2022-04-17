import os

from dotenv import load_dotenv

from picture_functions import download_picture
from picture_functions import get_comix_picture
from picture_functions import get_random_comix_number
from vk_api_functions import post_picture_to_vk


if __name__ == '__main__':
    load_dotenv()

    vk_token = os.getenv('VK_TOKEN')
    vk_group = os.getenv('VK_GROUP')
    version = 5.131
    filename = 'comix.png'

    random_number = get_random_comix_number()
    img_data, alt_text = get_comix_picture(random_number)

    try:
        download_picture(img_data, filename)
        post_picture_to_vk(filename, vk_token, vk_group, version, alt_text)
    finally:
        os.remove(filename)
