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
values = {'owner_id': group_id}
videos = tools.get_all_iter(method='video.get', max_count=8, values=values, limit=10000)

print('Video loading is finished! Starting parse!')

with open('videos.txt', 'a', encoding='utf-8') as file:
    try:
        for i, vid in enumerate(videos):
            link_str = 'https://vk.com/video{}_{}'.format(group_id, vid['id'])
            page = urlopen(link_str, timeout=5)
            content = page.read()
            page.close()
            link = content.decode('utf-8', "ignore")
            string = re.compile('<source src=\\\\"([^"]*)\\\\"')
            urls = string.findall(link)
            for url in urls:
                if 'video_hls.php' not in url:
                    if '1080.mp4' in url or '720.mp4' in url or '360.mp4' in url or '240.mp4':
                        try:
                            source = url.replace('\\/', '/')
                            reg = re.compile(r'/([^/]*\.mp4)')
                            name = reg.findall(source)[0]
                            clear_link = source.split('?')[0]
                            file.write(clear_link + "\n")
                            print('[{}] Processing {}'.format(i, clear_link))
                            break
                        except Exception as e:
                            print(e)
    except IncompleteRead as error:
        print(error)

print('Finish!')
exit(0)
