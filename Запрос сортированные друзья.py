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
    response = vk.friends.get(fields="bdate, first_name, last_name")
    if response['items']:
        a = sorted(response['items'], key=lambda x: x['last_name'])
        for i in a:
            if not 'bdate' in i:
                print(i['last_name'] + ' ' + i["first_name"] + ' no birthdate')
            else:
                print(i['last_name'] + ' ' + i["first_name"] + " " + i['bdate'])


if __name__ == '__main__':
    main()