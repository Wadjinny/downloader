# %%
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

from witanime.video_providers.yonaplay import get_links_from_yonaplay
import re

# base 64 decoder
import base64

# witanime headers

site_extension = "rest"
headers = {
    "authority": f"witanime.{site_extension}",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "cookie": "_ga=GA1.1.2071926742.1692061864; cf_clearance=XfaGiHbqrdN5zPchSNvJB6QhxyTKEnRdzYm9dGJnOCI-1692061865-0-1-4e523320.202ebdf0.119b4fa-160.2.1692061865; _ga_8MM0QDL0KJ=GS1.1.1692061863.1.1.1692062159.0.0.0",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}


# %% search
def get_search_results_link(search_term):
    global headers, site_extension
    search_term = quote(search_term)
    url = f"https://witanime.{site_extension}/?search_param=animes&s={search_term}"

    response = requests.request("GET", url, headers=headers, timeout=100)

    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    # .hover.ehover6>.overlay
    links = soup.select(".hover.ehover6>.overlay")
    links = [link["href"] for link in links]
    # print(f"{len(links) = }")
    return links


# %% epsides list
def get_episodes_list(anime_link):
    global headers

    response = requests.request("GET", anime_link, headers=headers, timeout=100)

    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    # .hover.ehover6>.overlay
    episodes = soup.select(".hover.ehover6>.overlay")
    # onclick="openEpisode('aHR0cHM6Ly93aXRhbmltZS5sYXQvZXBpc29kZS9ib3J1dG8tbmFydXRvLW5leHQtZ2VuZXJhdGlvbnMtJWQ4JWE3JWQ5JTg0JWQ4JWFkJWQ5JTg0JWQ5JTgyJWQ4JWE5LTEv')"

    # episodes = [re.search(r"openEpisode\('(.*)'\)", episode["onclick"]).group(1)
    #             for episode in episodes]
    episodes_links = []
    for episode in episodes:
        episode = re.search(r"openEpisode\('(.*)'\)", episode["onclick"]).group(1)
        episode = base64.b64decode(episode).decode("utf-8")
        episodes_links.append(episode)

    # print(f"{episodes_size = }")
    # print(f"{episodes[:10] = }")
    return episodes_links


# %%


def get_links_from_episode(episode_link):
    global headers
    payload = {}
    response = requests.request("GET", episode_link, headers=headers, data=payload)

    response = response.text

    soup = BeautifulSoup(response, "html.parser")
    server_links = soup.select("#episode-servers a")
    server_links = [
        base64.b64decode(a["data-url"]).decode("utf-8") for a in server_links
    ]

    download_links = soup.select(".quality-list a")
    download_links = [
        base64.b64decode(a["data-url"]).decode("utf-8") for a in download_links
    ]
    download_links = download_links[::-1]
    server_links.extend(download_links)
    yonaplay_id = list(filter(lambda x: "yonaplay" in x, server_links))
    # print(yonaplay_id)
    if yonaplay_id:
        yonaplay_id = yonaplay_id[0]
        yonaplay_server_links = get_links_from_yonaplay(yonaplay_id)
        server_links.extend(yonaplay_server_links)
    else:
        print("no yonaplay")

    return server_links


link = (
    "https://witanime.pics/episode/soul-eater-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
)
get_links_from_episode(link)
# %%
if __name__ == "__main__":
    episode_link = "https://witanime.icu/episode/jigokuraku-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-13/"
    get_links_from_episode(episode_link)
    ...
# %%

# %%
