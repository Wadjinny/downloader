#%% %%
import requests
import re
from witanime.video_providers.all_server_links import get_links_from_episode

def get_mediafire_links_from_episode(episode_link):
    all_server_links = get_links_from_episode(episode_link)
    links = list(filter(lambda x: 'mediafire.com' in x, all_server_links))
    return links

#%%
episode_link  = "https://witanime.tv/episode/bleach-sennen-kessen-hen-ketsubetsu-tan-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
# get_mediafire_links_from_episode(episode_link)

# %%
