import unittest
import requests

auth_token = ''
url_to_make_del_dir = 'https://cloud-api.yandex.net/v1/disk/resources/'
my_headers = {'Authorization': auth_token}
dir_name = 'TestDirName'


def create_folder():
    my_params = {'path': '/' + dir_name}
    r = requests.put(url_to_make_del_dir, headers=my_headers, params=my_params)
    return r.status_code


def get_folders_list():
    r = requests.get(url_to_make_del_dir,
                     headers=my_headers,
                     params={'path': '/', 'fields': '_embedded.items.name, _embedded.items.type'})
    flist = [item['name'] for item in r.json()['_embedded']['items'] if item['type'] == 'dir']
    return r.status_code, flist


def delete_folder():
    my_params = {'path': '/' + dir_name, 'permanently': True}
    r = requests.delete(url_to_make_del_dir, headers=my_headers, params=my_params)
    return r.status_code


class AppTests(unittest.TestCase):
    def test_dir_making(self):
        status, folders = get_folders_list()
        self.assertEqual(status, requests.codes.ok)
        if dir_name in folders:
            self.assertEqual(delete_folder(), requests.codes.no_content)
        self.assertEqual(create_folder(), requests.codes.created)
        status, folders = get_folders_list()
        self.assertEqual(status, requests.codes.ok)
        self.assertIn(dir_name, folders)

    def test_dir_exists(self):
        status, folders = get_folders_list()
        self.assertEqual(status, requests.codes.ok)
        if dir_name not in folders:
            self.assertEqual(create_folder(), requests.codes.created)
        self.assertEqual(create_folder(), requests.codes.conflict)


if __name__ == '__main__':
    unittest.main()

