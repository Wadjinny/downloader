# %%
import requests
import re


def get_links_from_yonaplay(yonaplay_link):
    payload = {}
    headers = {
        "authority": "yonaplay.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "cf_clearance=hx.b8jbx60dDMs494q5igh5N7taWSCwAyKbJ05pWOiY-1693370057-0-1-14edac47.f3a2f694.db7bb4f5-0.2.1693370057",
        "pragma": "no-cache",
        "referer": "https://witanime.pics/",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", yonaplay_link, headers=headers, data=payload)

    response = response.text
    server_links = re.findall("go_to_player\('(.*?)'\)", response)
    return server_links


# %%
if __name__ == "__main__":
    display(get_links_from_yonaplay("https://yonaplay.org/embed.php?id=630"))

# %%
