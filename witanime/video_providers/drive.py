# %% %%
import requests
import re
import gdown
from witanime.anime_site.witanime_extractor import get_links_from_episode
from pathlib import Path


# %%
def filter_drive_ids(server_links):
    def get_ids(link):
        if "export=download" in link:
            return re.findall(r"id=(.*)", link)[0]
        else:
            return re.findall(r"/d/(.*)/", link)[0]

    drive_links = list(filter(lambda x: "drive.google.com" in x, server_links))
    drive_id = list(map(get_ids, drive_links))
    return drive_id


def drive_dowload(drive_ids, output_dir, ouptut_file):
    if len(drive_ids) == 0:
        print(f"No drive links found for {ouptut_file}")
        return False
    for drive_id in drive_ids:
        try:
            if gdown.download(id=drive_id, output=str(output_dir / ouptut_file)):
                return True
            else:
                print(f"Failed to download from Drive, trying next link")
        except ValueError:
            print(f"Error downloading https://drive.google.com/file/d/{drive_id}/view")
            return False
        else:
            print(f"all {len(drive_ids)} drive links failed")
            return False


# %%
def drive_dowload_witanime(episode_link, output_dir, ouptut_file):
    all_server_links = get_links_from_episode(episode_link)
    drive_ids = filter_drive_ids(all_server_links)
    return drive_dowload(drive_ids, output_dir, ouptut_file)
