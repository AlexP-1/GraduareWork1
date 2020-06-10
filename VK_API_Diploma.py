from pprint import pprint
import requests
import json
import time


OAUTH_URL = 'https://oauth.vk.com/authorize'
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
OAUTH_PARAMS = {
    'client_id': '7496921',
    'display': 'page',
    'scope': 'notify, friends, photos, status, groups',
    'response_type': 'token',
    'v': 5.107
}


class User:

    def __init__(self, token, user_id: int):
        self.token = token
        self.user_id = int(user_id)

    def get_params(self):
        return {
            'access_token': token,
            'v': 5.107,
        }

    def get_user_groups(self):
        """
        return Выводит все группы пользователя по его ID
        """
        params = self.get_params()
        params['user_id'] = self.user_id
        params['extended'] = '1'
        params['fields'] = 'name', 'members_count'
        response = requests.get('https://api.vk.com/method/groups.get', params).json()
        groups_ids_names_dict = {}
        for group_item in response['response']['items']:
            if not group_item.get('deactivated') == 'banned':
                groups_ids_names_dict.update(
                    {group_item['id']:
                         {'members_count': group_item['members_count'], 'name': group_item['name']}
                     }
                )
            else:
                print(f'Группа {group_item["id"]} забанена, не добавлена в список')
        return groups_ids_names_dict

    def get_group_members(self, group_id):
        """
        param group_id: id группы
        return: список всех участников сообщества. 'filter'='friend' должен возвращать только друзей
        """
        params = self.get_params()
        params['group_id'] = group_id
        params['filter'] = 'friends'
        response = requests.get('https://api.vk.com/method/groups.getMembers', params)
        return response.json()


user = User(token, 171691064)


if __name__ == '__main__':

    friends_groups_dict = {}
    json_list = []

    for key, value in user.get_user_groups().items():
        if user.get_group_members(key)['response']['count'] != 0:
            pass
        else:
            friends_groups_dict = {'groupid': key,
                                   'groupname': value['name'],
                                   'members_count': value['members_count']}
            json_list.append(friends_groups_dict)
        time.sleep(1/3)
        print('Requesting  VK API . . .')

    with open('groups.json', 'w', encoding='utf-8') as fo:
        json.dump(json_list, fo, ensure_ascii=False, indent=2)
