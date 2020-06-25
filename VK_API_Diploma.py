
import requests
import json
import time

TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = input('Введите ID пользователя ')


class User:

    def __init__(self, user_id):
        self.user_id = user_id
        self.params = {
            'access_token': TOKEN,
            'v': 5.89,
            'user_id': self.user_id
        }

    def get_user_groups(self):
        response = requests.get(
            'https://api.vk.com/method/users.getSubscriptions',
            params=self.params).json()
        groups_set = [item for item in response['response']['groups']['items']]
        return groups_set

    def get_user_friends(self):
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=self.params
        ).json()
        friends_id = [item for item in response['response']['items']]
        return friends_id


def check_groups(friends, users):
    return bool(set(friends) & set(users))


def get_group_members():
    processing_counter = 1
    counter = 1000
    offset = 0
    time.sleep(1/3)
    friends = user.get_user_friends()
    time.sleep(1/3)
    groups = user.get_user_groups()
    new_groups = groups.copy()
    print('Checking user groups')
    for group in groups:
        group_member_ids = []
        group_id = group
        params = {
            'access_token': TOKEN,
            'v': 5.89,
            'count': counter,
            'offset': offset,
            'group_id': group_id
        }
        try:
            while True:
                time.sleep(1/3)
                response = requests.get(
                    'https://api.vk.com/method/groups.getMembers',
                    params=params
                ).json()
                group_member_ids.extend(response['response']['items'])
                if len(response['response']['items']) < 1000:
                    break
                else:
                    params['offset'] += counter
                print('Requesting API . . .')
        except KeyError:
            pass
        if check_groups(friends, group_member_ids):
            new_groups.remove(group)
        print(f'{processing_counter}/{len(groups)}')
        processing_counter += 1
    return new_groups


def get_data():
    data = []
    try:
        for group in get_group_members():
            params = {
                'access_token': TOKEN,
                'v': 5.89,
                'group_id': group,
                'fields': 'members_count'
            }
            time.sleep(1/3)
            response = requests.get(
                'https://api.vk.com/method/groups.getById',
                params=params
            ).json()
            data_group = {
                'name': response['response'][0]['name'],
                'gid': response['response'][0]['id'],
                'members_count': response['response'][0]['members_count']
            }
            data.append(data_group)
    except KeyError:
        pass
    return data


def dump_json():
    with open('groups.json', 'w', encoding='UTF-8') as fo:
        json.dump(get_data(), fo, ensure_ascii=False, indent=2)


user = User(user_id)

dump_json()
