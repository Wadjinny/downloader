# %% %%
import requests
import re
from witanime.anime_site.witanime_extractor import get_links_from_episode
from pathlib import Path
import subprocess


# %%
def get_mega_links_from_episode(episode_link):
    server_links = get_links_from_episode(episode_link)
    mega_links = list(filter(lambda x: "mega.nz" in x, server_links))

    mega_embed_links = list(filter(lambda x: "mega.nz/embed" in x, mega_links))
    mega_embed_links = [link.replace("embed", "file") for link in mega_embed_links]

    mega_file_links = list(filter(lambda x: "mega.nz/file" in x, mega_links))
    mega_file_links.extend(mega_embed_links)

    return mega_file_links


# %%
def meganz_dowload(episode_link, output_dir, ouptut_file):
    """wrapper for megatools, use megadl command to download"""

    meganz_links = get_mega_links_from_episode(episode_link)
    if len(meganz_links) == 0:
        print(f"No mega links found for {ouptut_file}")
        return False
    # megatools is required, check if it is installed, dont display output
    try:
        subprocess.run(["megadl", "--version"], stdout=subprocess.DEVNULL, check=True)
    except FileNotFoundError:
        print("megatools is required")
        return False

    for link in meganz_links:
        try:
            print(f"Downloading {link}")
            subprocess.run(
                ["megadl", link, "--path", str(output_dir / ouptut_file)], check=True
            )
            return True
        except subprocess.CalledProcessError:
            print(f"Error downloading {link}")
            print(f"you may visit {episode_link} to download it manually")


# %%
if __name__ == "__main__":
    episode_link = (
        "https://witanime.lol/episode/one-piece-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
    )
    get_mega_links_from_episode(episode_link)
    # TEST DOWNLOAD
    meganz_links = get_mega_links_from_episode(episode_link)
    # output_dir = Path("temp")
    # output_dir.mkdir(exist_ok=True)

    # meganz_dowload(meganz_links, output_dir=output_dir, ouptut_file="test.mp4")
# %%
