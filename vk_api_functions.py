import requests


def get_wall_upload_url(vk_token, vk_group, version):
    url = "https://api.vk.com/method/photos.getWallUploadServer"

    params = {
        'group_id': vk_group,
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    wall_upload_data = response.json()
    error_checking(wall_upload_data)

    return wall_upload_data['response']['upload_url']


def upload_picture_to_vk(filename, vk_token, vk_group, version):
    with open(filename, 'rb') as picture:
        wall_upload_url = get_wall_upload_url(vk_token, vk_group,  version)

        wall_files = {
            'photo': picture
        }

        response = requests.post(wall_upload_url, files=wall_files)
        response.raise_for_status()

        returned_data = response.json()
        error_checking(returned_data)

    return returned_data


def save_picture(server, photo, photo_hash, vk_token, vk_group, version):
    url = "https://api.vk.com/method/photos.saveWallPhoto"

    params = {
        'server': server,
        'photo': photo,
        'hash': photo_hash,
        'group_id': vk_group,
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    returned_data = response.json()
    error_checking(returned_data)

    return returned_data


def post_picture_to_vk(filename, vk_token, vk_group, version, alt_text):
    upload_data = upload_picture_to_vk(filename, vk_token, vk_group, version)
    save_data = save_picture(
        upload_data['server'],
        upload_data['photo'],
        upload_data['hash'],
        vk_token,
        vk_group,
        version
    )

    post_on_wall(
        save_data['response'][0]['owner_id'],
        save_data['response'][0]['id'],
        vk_token,
        vk_group,
        version,
        alt_text
    )


def post_on_wall(owner_id, photo_id, vk_token, vk_group, version, alt_text):
    url = "https://api.vk.com/method/wall.post"

    params = {
        'owner_id': f'-{vk_group}',
        'from_group': 0,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': alt_text,
        'access_token': vk_token,
        'v': version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    posted_data = response.json()
    error_checking(posted_data)


def error_checking(responsed_data):
    if 'error' in responsed_data:
        raise requests.exceptions.HTTPError(responsed_data['error'])
