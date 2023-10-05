# %%
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import re

# base 64 decoder

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "fr,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referrer": "https://www.zimabadk.com/",
}


# %% search
def get_search_results_link(search_term):
    search_term = quote(search_term)
    types = ["anime", "film"]
    all_links = []
    for type in types:
        url = f"https://www.zimabadk.com/filter/type/{type}/text/{search_term}/"
        # print(url)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=100)
        response = response.text
        soup = BeautifulSoup(response, "html.parser")
        # .container>slice--blocks>a
        links = soup.select(".container>slice--blocks>a")
        links = [link["href"] for link in links]
        all_links += links
    return all_links


# %% epsides list
def get_episodes_list(anime_link):
    response = requests.request("GET", anime_link, headers=headers, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    # .episodes-list a
    links = soup.select(".episodes-list a")
    links = [link["href"] for link in links]
    return links[::-1]


anime_link = "https://www.zimabadk.com/anime/naruto/"
# get_episodes_list(anime_link)
# %%

episode_link = "https://www.zimabadk.com/jigokuraku-e-11/"


def get_links_from_episode(episode_link):
    response = requests.request("GET", episode_link, headers=headers, timeout=100)
    response = response.text
    soup = BeautifulSoup(response, "html.parser")
    server_links = soup.select("servers-links .server")
    server_links = [link["data-code"] for link in server_links]

    download_link = soup.select("download--servers a")
    download_link = [link["href"] for link in download_link]
    return server_links + download_link


# get_links_from_episode(episode_link)

# %%
if __name__ == "__main__":
    ...
# %%
