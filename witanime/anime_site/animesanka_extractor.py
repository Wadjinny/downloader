# %%
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import re

# %%


def get_search_results_link(search_term):
    search_term = quote(search_term)
    url = f"https://www.anime-sanka.com/search?q={search_term}&max-results=128"

    payload = {}
    headers = {
        "authority": "www.anime-sanka.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.anime-sanka.com/2022/04/bleach-1080p.html",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version-list": '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.170", "Chromium";v="115.0.5790.170"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.2.0"',
        "sec-ch-ua-wow64": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    # #Blog1 > div.blog-posts.hfeed.row > div > article > div > div.mobile-index-thumbnail > div > div.mobile-index-thumbnail > div > a
    ahref = soup.select(
        "#Blog1 > div.blog-posts.hfeed.row > div > article > div > div.mobile-index-thumbnail > div > div.mobile-index-thumbnail > div > a"
    )
    ahref = [link["href"] for link in ahref]
    return ahref


# %%


def get_all_episodes_server_link(episodes_link):
    url = episodes_link
    payload = {}
    headers = {
        "authority": "www.anime-sanka.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "fr,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://www.anime-sanka.com/search?q=bleach&max-results=48",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version-list": '"Not/A)Brand";v="99.0.0.0", "Google Chrome";v="115.0.5790.170", "Chromium";v="115.0.5790.170"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"6.2.0"',
        "sec-ch-ua-wow64": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    # #snippet-single > div > div > section.tab-content-sanka.content2-sanka > div > a
    links = soup.select(
        "#snippet-single > div > div > section.tab-content-sanka.content2-sanka > div > a"
    )
    links = [link["href"] for link in links]
    if len(links) == 0:
        print("No links found")
        return []
    link = links[0]
    link = link.replace("tube.animesanka.com", "watch.animesanka.com")
    link = link.replace("d.animesanka.xyz", "watch.animesanka.com")
    link = link.replace("dw.anime-sanka.com", "watch.animesanka.com")
    link = link.replace("www.animesanka.club", "watch.animesanka.com")
    link = link.replace("tv.animesanka.net", "watch.animesanka.com")
    link = link.replace("www.animesanka.club", "watch.animesanka.com")
    link = link.replace("www.animesanka.com", "watch.animesanka.com")
    link = link.replace("www.animesanka.net", "watch.animesanka.com")
    link = link.replace("prwd.animesanka.club", "watch.animesanka.com")
    link = link.replace("onsanka.xyz", "watch.animesanka.com")
    prefix = "https://ar.anime-sanka.com/"
    anime_link = prefix + link

    response = requests.request("GET", anime_link, headers=headers, data=payload)
    response = response.text
    search_link = link.replace("watch.animesanka.com", "prwd.animesanka.club")
    # search for the line containing the link
    # ", {id: '2088894109015915446', link: 'https://prwd.animesanka.club/2021/02/bleach.html'}"
    # select id

    id = re.search(f", {{id: '(.*)', link: '{search_link}'}}", response).group(1)

    url = f"https://prwd.animesanka.club/feeds/posts/default/{id}?alt=json-in-script"

    payload = {}
    headers = {
        "authority": "prwd.animesanka.club",
        "accept": "*/*",
        "accept-language": "fr,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://ar.anime-sanka.com/",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = response.text
    # unescape the string
    response = response.encode().decode("unicode-escape").replace("\/", "/")
    # select all line with <option
    option_lines = re.findall(r"<option(.*?)<\/option>", response, re.S)
    episodes_list = []
    if "@" in option_lines[0]:
        for line in option_lines:
            episode_num = re.search(r"value=.(\d+).", line).group(1)
            # regex to select the link begin with http and end with space
            links = re.findall(r"(http.*?)[\s|'|\"]", line)
            episodes_list.append((episode_num, links))
    else:
        movie_links = []
        try:
            for line in option_lines:
                links = re.findall(r"(http.*?)[\s|'|\"]", line)[0]
                movie_links.append(links)
            episodes_list.append(("1", movie_links))
        except Exception as e:
            print(option_lines)
            print(response)
            raise e
    # print(episodes_list[:3])
    return episodes_list


# %%
