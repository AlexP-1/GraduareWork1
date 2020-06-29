
import requests
import json
import time

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
USER_ID = input('Введите ID пользователя ')


class User:

    def __init__(self, USER_ID):
        if str(USER_ID).isdigit():
            self.user_id = USER_ID
        else:
            time.sleep(1 / 3)
            self.params = {
                'access_token': TOKEN,
                'v': 5.89,
                'screen_name': USER_ID
            }
            response = requests.get(
                'https://api.vk.com/method/utils.resolveScreenName',
                params=self.params
            ).json()
            self.USER_ID = response['response']['object_id']
        self.params = {
            'access_token': TOKEN,
            'v': 5.89,
            'user_id': self.user_id,
        }

    def get_user_groups(self):
        self.params['extended'] = 1
        self.params['fields'] = 'members_count'
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params=self.params).json()
        return response

    def group_set(self):
        groups_set = [item['id'] for item in User.get_user_groups(self)['response']['items']]
        return groups_set

    def get_friends(self):
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=self.params
        ).json()
        friends_id = [item for item in response['response']['items']]
        return friends_id


def uncommon_group(user_id):
    main_user = User(user_id)
    time.sleep(1/3)
    friends_set = main_user.get_friends()
    time.sleep(1/3)
    group_set = main_user.group_set()
    print('Checking friends and their groups . . .')
    counter = 1
    for friend_id in friends_set:
        user = User(friend_id)
        time.sleep(1/3)
        try:
            new_group_set = user.group_set()
        except KeyError:
            print(f'Пользователь id{friend_id} имеет закрытый профиль или заблокирован')
            print(f'{counter}/{len(friends_set)}')
            counter += 1
            continue
        group_set = set(group_set) - set(new_group_set)
        print(f'{counter}/{len(friends_set)}')
        counter += 1
    return group_set


def get_data():
    data = []
    user = User(USER_ID)
    unique_groups = uncommon_group(USER_ID)
    for group in user.get_user_groups()['response']['items']:
        if group['id'] in unique_groups:
            try:
                data.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})
            except KeyError:
                continue
    return data


def dump_json():
    with open('groups.json', 'w', encoding='utf-8') as fo:
        json.dump(get_data(), fo, ensure_ascii=False, indent=2)


dump_json()
