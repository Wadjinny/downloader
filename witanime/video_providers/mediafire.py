# %% %%
import requests
import re
from witanime.anime_site.witanime_extractor import get_links_from_episode
import mediafire_dl


def get_mediafire_links_from_episode(episode_link):
    all_server_links = get_links_from_episode(episode_link)
    links = list(filter(lambda x: "mediafire.com" in x, all_server_links))
    return links


def download_from_mediafire(episode_link, output_path, ouptut_file):
    mediafire_links = get_mediafire_links_from_episode(episode_link)
    if len(mediafire_links) == 0:
        print(f"No mediafire links found for {episode_link}")
        return False
    for link in mediafire_links:
        try:
            mediafire_dl.download(link, str(output_path/ouptut_file), quiet=False)
            return True
        except ValueError:
            print(f"Error downloading {link}")
            print(f"you may visit {episode_link} to download it manually")


# %%
if __name__ == "__main__":
    episode_link = "https://witanime.tv/episode/bleach-sennen-kessen-hen-ketsubetsu-tan-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
    assert len(get_mediafire_links_from_episode(episode_link)) > 0

# %%
