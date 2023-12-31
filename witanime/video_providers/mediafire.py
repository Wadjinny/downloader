# %% %%
import requests
import re
import mediafire_dl


def filter_mediafire_links(all_server_links):
    links = list(filter(lambda x: "mediafire.com" in x, all_server_links))
    return links


def download_mediafire_links(mediafire_links, output_path, ouptut_file):
    if len(mediafire_links) == 0:
        print(f"No mediafire links found for {ouptut_file}")
        return False
    for link in mediafire_links:
        try:
            if mediafire_dl.download(link, str(output_path / ouptut_file), quiet=False):
                return True
            else:
                print(f"Error downloading from mediafire, trying next link")
        except ValueError:
            print(f"Error downloading {link}")
    else:
        print(f"all {len(mediafire_links)} mediafire links failed")
        return False


def download_from_mediafire_witanime(all_server_links, output_path, ouptut_file):
    mediafire_links = filter_mediafire_links(all_server_links)
    return download_mediafire_links(mediafire_links, output_path, ouptut_file)


# %%
if __name__ == "__main__":
    episode_link = "https://witanime.tv/episode/bleach-sennen-kessen-hen-ketsubetsu-tan-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
    assert len(filter_mediafire_links(episode_link)) > 0

# %%
