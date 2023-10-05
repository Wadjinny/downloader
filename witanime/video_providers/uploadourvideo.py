# %%
import requests
import re
from bs4 import BeautifulSoup
import json
from witanime.utils.async_downloader import dowload_from_url
from pathlib import Path

# %%


def upload_download(url, output_dir, ouptut_file):
    session = requests.Session()
    url = url.replace("watch", "embed")
    try:
        session = requests.Session()
        response = session.get(url)
        response = response.text
        # file: "https://uploadourvideo.com/files/AF3yzihROV/720.mp4"
        mp4_url = re.findall(r'file: "(.*?)"', response)[0]
        dowload_from_url(
            mp4_url,
            output_dir=Path(output_dir),
            filename=ouptut_file,
            headers=session.headers,
        )
        return True
    except Exception as e:
        print(e)
        return False


url = "https://uploadourvideo.com/embed/AF3yzihROV"
# upload_download(url, "output_dir", "ouptut_file")

# %%


def filter_upload_links(server_links):
    upload_links = list(filter(lambda x: "uploadourvideo.com" in x, server_links))
    return upload_links


# %%
def upload_dowload_handler(all_server_links, output_dir, ouptut_file):
    upload_links = filter_upload_links(all_server_links)
    if len(upload_links) == 0:
        print(f"No uploadourvideo.com links found for {ouptut_file}")
        return False
    for upload_link in upload_links:
        if upload_download(upload_link, output_dir, ouptut_file):
            return True
        else:
            print(f"Error downloading from uploadourvideo.com, trying next link")
    else:
        print(f"all {len(upload_links)} uploadourvideo.com links failed")
        return False


# %%
