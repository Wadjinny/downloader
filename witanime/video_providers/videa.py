# %%
import requests
import re
from bs4 import BeautifulSoup
import json
from witanime.utils.async_downloader import dowload_from_url
from pathlib import Path

# %%
link = "https://videa.hu/player?v=nBbe5GGys9pv3ARl"
session = requests.Session()
response = session.get(link)
response = response.text
soup = BeautifulSoup(response, "html.parser")
video_links = soup.find_all("video")
video_links


# %%


def okru_download(url, output_dir, ouptut_file):
    ...


def filter_okru_links(server_links):
    ...


def okru_dowload_witanime(all_server_links, output_dir, ouptut_file):
    ...


# %%
