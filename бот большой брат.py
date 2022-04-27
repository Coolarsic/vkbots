import vk_api


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo(['static/img/Picture1.png', 'static/img/Picture2.png', 'static/img/Picture3.png'], '{album_id}', '{group_id}')


if __name__ == '__main__':
    main()