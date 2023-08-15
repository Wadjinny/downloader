#%% %%
import requests
import re
from video_providers.all_server_links import get_links_from_episode

def get_drive_ids_from_episode(episode_link):
    def get_ids(link):
        if 'export=download' in link:
            return re.findall(r'id=(.*)', link)[0]
        else:
            return re.findall(r'/d/(.*)/', link)[0]
    server_links = get_links_from_episode(episode_link)
    drive_links = list(filter(lambda x: 'drive.google.com' in x, server_links))
    drive_id = list(map(get_ids, drive_links))
    return drive_id

#%%
# episode_link  = "https://witanime.tv/episode/boruto-naruto-next-generations-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
# get_drive_ids_from_episode(episode_link)
# %%
