import os
import vk_api

vk_session = vk_api.VkApi(os.getenv('VK_LOGIN'), os.getenv('VK_PASS'))
vk_session.auth()

VK = vk_session.get_api()

print(VK.wall.post(message='Hello world!'))
