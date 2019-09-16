import os
import re
from urllib.request import urlopen
from http.client import IncompleteRead

import vk_api

group_id = -108338390

login, password = os.getenv('VK_LOGIN'), os.getenv('VK_PASS')
vk_session = vk_api.VkApi(login=login, password=password, api_version='5.101')

try:
    vk_session.auth()
except vk_api.AuthError as error:
    print(error)

VK = vk_session.get_api()
tools = vk_api.VkTools(vk=VK)
params = dict(owner_id=group_id)
videos = tools.get_all_iter(method='video.get', max_count=200, values=params, limit=10000)

with open('videos.txt', 'a') as file:
    try:
        for vid in videos:
            print(vid)
            link_str = 'https://vk.com/video{}_{}'.format(group_id, vid['id'])
            page = urlopen(link_str, timeout=5)
            content = page.read()
            link = content.decode('utf-8', "ignore")
            string = re.compile('<source src=\\\\"([^"]*)\\\\"')
            urls = string.findall(link)
            for i in ['1080.mp4', '720.mp4', '360.mp4', '240.mp4']:
                for url in urls:
                    try:
                        if i in url:
                            source = url.replace('\\/', '/')
                            reg = re.compile(r'/([^/]*\.mp4)')
                            name = reg.findall(source)[0]
                            source = source.split('?')[0]
                            print(source)
                            file.write(source + "\n")
                            print('Processing {}...'.format(name))
                            break
                    except Exception as e:
                        print(e)
    except IncompleteRead as error:
        print(error)
        pass
