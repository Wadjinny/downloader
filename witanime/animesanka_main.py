# %% search
from pathlib import Path
from witanime.anime_site.animesanka_extractor import (
    get_search_results_link,
    get_all_episodes_server_link,
)
from witanime.video_providers.drive import drive_dowload, filter_drive_ids
from witanime.video_providers.mediafire import (
    download_mediafire_links,
    filter_mediafire_links,
)
from witanime.video_providers.meganz import meganz_dowload, filter_meganz_links
from witanime.video_providers.okru import okru_dowload_witanime

import argparse
from glob import glob


def clean(output_dir):
    if len(glob(f"{output_dir}/*.mp4")) == 0:
        print("Deleting directory")
        for f in output_dir.glob("*"):
            f.unlink()
        output_dir.rmdir()


def main():
    parser = argparse.ArgumentParser(description="Download anime from anime-sanka")
    parser.add_argument("search_term", metavar="search_term", type=str)
    # add boolean argument -r, if present range will be asked, by default it will False
    parser.add_argument("-r", action="store_true", help="download range of episodes")

    args = parser.parse_args()
    search_term = args.search_term
    search_results = get_search_results_link(search_term)
    if len(search_results) == 0:
        print("No results found")
        return
    max_letters = max([len(result) for result in search_results])
    for i, result in enumerate(search_results):
        print(f"{i+1}. {result:<{max_letters}} .{i+1}")
    anime_index = input("Enter anime index: ")
    anime_link = search_results[int(anime_index) - 1]
    anime_name = anime_link.split("/")[-1].replace("html", "")
    episodes_link = get_all_episodes_server_link(anime_link)[::-1]
    print(f"{len(episodes_link)} episodes found")

    output_dir = Path(anime_name)
    output_dir.mkdir(exist_ok=True)
    if args.r:
        selection = input("episode range: ")
        # remove spaces
        selection = selection.replace(" ", "")
        # for example 1, 3-5, 7
        selector = [False] * len(episodes_link)
        for part in selection.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                selector[start - 1 : end] = [True] * (end - start + 1)
            else:
                selector[int(part) - 1] = True
        episodes_link = [
            link for link, select in zip(episodes_link, selector) if select
        ]

    for epside_num, all_server_links in episodes_link:
        try:
            ouptut_file = f"{anime_name}_EP{epside_num}.mp4"
            print(f"{epside_num}/{len(episodes_link)} {ouptut_file}")
            drive_ids = filter_drive_ids(all_server_links)
            print("Downloading from google drive")
            if drive_dowload(drive_ids, output_dir, ouptut_file):
                continue

            print("Downloading from mediafire")
            mediafire_links = filter_mediafire_links(all_server_links)
            if download_mediafire_links(mediafire_links, output_dir, ouptut_file):
                continue

            print("Downloading from mega.nz")
            meganz_links = filter_meganz_links(all_server_links)
            if meganz_dowload(meganz_links, output_dir, ouptut_file):
                continue

            print("Downloading from ok.ru")
            if okru_dowload_witanime(all_server_links, output_dir, ouptut_file):
                continue

            print("Failed to download from all links")
            print("Skipping...")
        except KeyboardInterrupt:
            print("Exiting...")
            # if output_dir is empty delete it
            clean(output_dir)
            return
    clean(output_dir)


if __name__ == "__main__":
    main()
# %%
