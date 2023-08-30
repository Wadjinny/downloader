# %% %%
import requests
import re
import gdown
from witanime.anime_site.witanime_extractor import get_links_from_episode
from pathlib import Path


# %%
def get_drive_ids_from_episode(episode_link):
    def get_ids(link):
        if "export=download" in link:
            return re.findall(r"id=(.*)", link)[0]
        else:
            return re.findall(r"/d/(.*)/", link)[0]

    server_links = get_links_from_episode(episode_link)
    drive_links = list(filter(lambda x: "drive.google.com" in x, server_links))
    drive_id = list(map(get_ids, drive_links))
    return drive_id


# %%
def drive_dowload(episode_link, output_dir, ouptut_file):
    drive_ids = get_drive_ids_from_episode(episode_link)
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
            print(f"you may visit {episode_link} to download it manually")
            return False
        else:
            print(f"all {len(drive_ids)} drive links failed")
            return False


# %%
if __name__ == "__main__":
    episode_link = "https://witanime.tv/episode/niehime-to-kemono-no-ou-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-18/"
    assert len(get_drive_ids_from_episode(episode_link)) > 0
# %% TEST DOWNLOAD
# drive_ids = ["1EmNTL-XPia0FgPPkuXXcDYVGQnZ6yvnP"]
# temp_dir = Path("temp")
# temp_dir.mkdir(exist_ok=True)

# drive_dowload(drive_ids, output_dir=temp_dir, ouptut_file="test")

# for file in temp_dir.glob("*"):
#     file.unlink()
# temp_dir.rmdir()
