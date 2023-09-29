# %%
import requests
import re
from bs4 import BeautifulSoup
import json
from witanime.utils.async_downloader import dowload_from_url
from pathlib import Path

# %%


def okru_download(url, output_dir, ouptut_file):
    session = requests.Session()
    try:
        response = session.get(url)
        response = response.text

        soup = BeautifulSoup(response, "html.parser")
        # div[data-module="OKVideo"]
        data = soup.find("div", {"data-module": "OKVideo"})
        data = data["data-options"]
        data = json.loads(data)

        # flashvars.metadata.videos[0].url
        video_links = json.loads(data["flashvars"]["metadata"]).get("videos")
        video_links = [i["url"] for i in video_links][::-1]

        dowload_from_url(
            video_links[0],
            output_dir=Path(output_dir),
            filename=ouptut_file,
            headers=session.headers,
        )
        return True
    except Exception as e:
        print(e)
        return False


def filter_okru_links(server_links):
    okru_links = list(filter(lambda x: "ok.ru" in x, server_links))
    return okru_links


def okru_dowload_witanime(all_server_links, output_dir, ouptut_file):
    okru_links = filter_okru_links(all_server_links)
    if len(okru_links) == 0:
        print(f"No ok.ru links found for {ouptut_file}")
        return False
    for okru_link in okru_links:
        if okru_download(okru_link, output_dir, ouptut_file):
            return True
        else:
            print(f"Error downloading from ok.ru, trying next link")
    else:
        print(f"all {len(okru_links)} ok.ru links failed")
        return False


# %%
if __name__ == "__main__":
    ok_rulink = "https://ok.ru/videoembed/4998317279819"
    okru_download(ok_rulink, ".", "test.mp4")
