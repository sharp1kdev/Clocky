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
videos = tools.get_all(method='video.get', max_count=8, values=params, limit=400)
print('Loaded {} videos!'.format(videos['count']))

with open('videos.txt', 'a') as file:
    try:
        for vid in videos['items']:
            link_str = 'https://vk.com/video{}_{}'.format(group_id, vid['id'])
            page = urlopen(link_str, timeout=5)
            content = page.read()
            page.close()
            link = content.decode('utf-8', "ignore")
            string = re.compile('<source src=\\\\"([^"]*)\\\\"')
            urls = string.findall(link)
            i = ['1080.mp4', '720.mp4', '360.mp4', '240.mp4']
            if i in urls:
                for url in urls:
                    try:
                        source = url.replace('\\/', '/')
                        reg = re.compile(r'/([^/]*\.mp4)')
                        name = reg.findall(source)[0]
                        source = source.split('?')[0]
                        file.write(source + "\n")
                        print('Processing {}...'.format(source))
                        break
                    except Exception as e:
                        print(e)
    except IncompleteRead as error:
        print(error)
        pass

print('Finish!')
exit(0)
