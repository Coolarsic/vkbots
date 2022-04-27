import vk_api


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()
    photos = vk.photos.get(group_id='211020313', album_id='285252237')
    for i in photos['items']:
        for j in i['sizes']:
            print(f"Width: {j['width']}, height: {j['width']}, url: {j['url']}")


if __name__ == '__main__':
    main()