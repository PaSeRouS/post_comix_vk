import requests

def get_wall_upload_url(vk_token, version):
    url = "https://api.vk.com/method/photos.getWallUploadServer"

    params = {
        'group_id': '212629556',
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    wall_upload_data = response.json()
    return wall_upload_data['response']['upload_url']


def upload_picture_to_vk(filename, vk_token, version):
    with open(filename, 'rb') as picture:
        wall_upload_url = get_wall_upload_url(vk_token, version)

        wall_files = {
            'photo': picture
        }

        response = requests.post(wall_upload_url, files=wall_files)
        response.raise_for_status()

    return response.json()


def save_picture(upload_data, vk_token, version):
    url = "https://api.vk.com/method/photos.saveWallPhoto"

    params = {
        'server': upload_data['server'],
        'photo': upload_data['photo'],
        'hash': upload_data['hash'],
        'group_id': '212629556',
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def post_picture_to_vk(filename, vk_token, version, alt_text):
    upload_data = upload_picture_to_vk(filename, vk_token, version)
    save_data = save_picture(upload_data, vk_token, version)
    post_on_wall(save_data, vk_token, version, alt_text)


def post_on_wall(save_data, vk_token, version, alt_text):
    url = "https://api.vk.com/method/wall.post"

    owner_id = save_data['response'][0]['owner_id']
    photo_id = save_data['response'][0]['id']

    params = {
        'owner_id': '-212629556',
        'from_group': 0,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': alt_text,
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()