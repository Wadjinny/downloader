#%% search
import requests
from bs4 import BeautifulSoup as bs
import re
import gdown 
from pathlib import Path
#to url encode
from urllib.parse import quote
from witanime.video_providers.drive import get_drive_ids_from_episode
from witanime.video_providers.mediafire import get_mediafire_links_from_episode


import argparse


#%% search
def get_search_results_link(search_term):
    search_term = quote(search_term)
    url = f"https://witanime.org/?search_param=animes&s={search_term}"

    payload={}
    headers = {
    'authority': 'witanime.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '_ga=GA1.1.2071926742.1692061864; cf_clearance=XfaGiHbqrdN5zPchSNvJB6QhxyTKEnRdzYm9dGJnOCI-1692061865-0-1-4e523320.202ebdf0.119b4fa-160.2.1692061865; _ga_8MM0QDL0KJ=GS1.1.1692061863.1.1.1692062159.0.0.0',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = response.text
    soup = bs(response, 'html.parser')
    # .hover.ehover6>.overlay
    links = soup.select('.hover.ehover6>.overlay')
    links = [link['href'] for link in links]
    # print(f"{len(links) = }")
    return links



# %% epsides list
def get_episodes_list(anime_link):
    payload={}
    headers = {
    'authority': 'witanime.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': '_ga=GA1.1.2071926742.1692061864; cf_clearance=XfaGiHbqrdN5zPchSNvJB6QhxyTKEnRdzYm9dGJnOCI-1692061865-0-1-4e523320.202ebdf0.119b4fa-160.2.1692061865; _ga_8MM0QDL0KJ=GS1.1.1692061863.1.1.1692062159.0.0.0',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", anime_link, headers=headers, data=payload)

    response = response.text
    soup = bs(response, 'html.parser')
    # .hover.ehover6>.overlay
    episodes = soup.select('.hover.ehover6>.overlay')
    episodes = [episode['href'] for episode in episodes]
    episodes_size = len(episodes)
    # print(f"{episodes_size = }")
    # print(f"{episodes[:10] = }")
    return episodes

def download_from_mediafire(episode_link, output_path):
    import mediafire_dl
    mediafire_links = get_mediafire_links_from_episode(episode_link)
    if len(mediafire_links) == 0:
        print(f"No mediafire links found for {episode_link}")
        return
    for link in mediafire_links:
        try:
            mediafire_dl.download(link, str(output_path),quiet=False)
            return
        except ValueError:
            print(f"Error downloading {link}")
            print(f"you may visit {episode_link} to download it manually")

def clean(output_dir):
    if len(list(output_dir.iterdir())) <= 1:
        output_dir.rmdir()    
# %%
def main():
    parser = argparse.ArgumentParser(description='Download anime from witanime.org')
    parser.add_argument('search_term', metavar='search_term', type=str)
    args = parser.parse_args()
    search_term = args.search_term
    search_results = get_search_results_link(search_term)
    if len(search_results) == 0:
        print("No results found")
        return
    for i, result in enumerate(search_results):
        print(f"{i+1}. {result}")
    anime_index = input("Enter anime index: ")
    anime_link = search_results[int(anime_index)-1]

    episodes_link = get_episodes_list(anime_link)
    print(f'{len(episodes_link)} episodes found')
    output_dir = Path(anime_link.split('/')[-2])
    output_dir.mkdir(exist_ok=True)
    for i, episode_link in enumerate(episodes_link):
        try:
            drive_ids = get_drive_ids_from_episode(episode_link)
            ouptut_file = f"{anime_link.split('/')[-2]}_EP{i+1}.mp4"
            print(f"{i+1}/{len(episodes_link)} {ouptut_file}")
            if len(drive_ids) == 0:
                print(f"No drive links found for {ouptut_file}")
                clean(output_dir)
                return
            for drive_id in drive_ids:
                try:
                    if not gdown.download(id=drive_id, output=str(output_dir/ouptut_file)):
                        print(f"Failed to download from Drive, trying mediafire")
                        download_from_mediafire(episode_link, output_dir/ouptut_file)
                    break
                except ValueError:
                            print(f"Error downloading https://drive.google.com/file/d/{drive_id}/view")
                            print(f"you may visit {episode_link} to download it manually")
                            download_from_mediafire(episode_link, output_dir/ouptut_file)
        except KeyboardInterrupt:
            print("Exiting...")
            # if output_dir is empty delete it
            clean(output_dir)
            return

if __name__ == "__main__":
    main()
# %%
