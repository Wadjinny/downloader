#%% search
import requests
from bs4 import BeautifulSoup as bs
import re
import gdown 
from pathlib import Path

#%% search
def get_search_results_link(search_term):
    search_term = search_term.replace(" ", "+")
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


#%%
def get_drive_from_yonaplay(yonaplay_link):
    payload={}
    headers = {
    'authority': 'yonaplay.org',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'cf_clearance=l0bMMjK_AWLsUIOqYzF3qCSRSmw0CZ1l5s4Dx7P8_Gc-1692061916-0-1-4e523320.202ebdf0.119b4fa-0.2.1692061916',
    'pragma': 'no-cache',
    'referer': 'https://witanime.org/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", yonaplay_link, headers=headers, data=payload)

    response = response.text
    # https://drive.google.com/file/d/1Pk56A0la0_SufhDDxeOwltT9k4y7cbPw/preview
    drive_id = re.search(r"https://drive.google.com/file/d/(.*?)/preview", response).group(1)
    # print(f"{drive_id = }")
    return drive_id

# %% id 
def get_drive_id_from_episode(episode_link):
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

    response = requests.request("GET", episode_link, headers=headers, data=payload)

    response = response.text
    drive_id = re.search(r"https://drive.google.com/file/d/(.*?)/preview", response)
    if drive_id:
        drive_id = drive_id.group(1)
    else:
        yonaplay_id = re.search(r"https://yonaplay.org/embed.php\?id=\d+", response).group()
        drive_id = get_drive_from_yonaplay(yonaplay_id)
    # print(f"{drive_id = }")
    return drive_id
    
#%% mediafire
def get_mediafire_from_episode(episode_link):
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

    response = requests.request("GET", episode_link, headers=headers, data=payload)

    response = response.text
    # https://www.mediafire.com/file/3vtjsfemuw5arv4/%5BWitanime.com%5D_RZKHISHNK_BD-FHD.mp4/file
    mediafire_link = re.search(r"https://www.mediafire.com/file/.*/.*/file", response)
    if mediafire_link:
        mediafire_link = mediafire_link.group()
    else:
        yonaplay_id = re.search(r"https://yonaplay.org/embed.php\?id=\d+", response).group()
        drive_id = get_drive_from_yonaplay(yonaplay_id)
    # print(f"{drive_id = }")
    return drive_id

# %%
def main():
    # search_term = "no game no life"
    search_term = input("Enter search term: ")
    search_results = get_search_results_link(search_term)
    for i, result in enumerate(search_results):
        print(f"{i+1}. {result}")
    anime_index = input("Enter anime index: ")
    anime_link = search_results[int(anime_index)-1]

    episodes_link = get_episodes_list(anime_link)
    print(f'{len(episodes_link)} episodes found')
    output_dir = Path(anime_link.split('/')[-2])
    output_dir.mkdir(exist_ok=True)
    for i, episode_link in enumerate(episodes_link):
        drive_id = get_drive_id_from_episode(episode_link)
        ouptut_file = f"{anime_link.split('/')[-2]}_EP{i+1}.mp4"
        
        print(f"{i+1}/{len(episodes_link)} {ouptut_file}")
        try:
            gdown.download(id=drive_id, output=str(output_dir/ouptut_file), quiet=False)
        except ValueError:
            print(f"Error downloading https://drive.google.com/file/d/{drive_id}/preview")
            print(f"you may visit {episode_link} to download it manually")

if __name__ == "__main__":
    main()
# %%
