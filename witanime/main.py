#%% search
from pathlib import Path
import gdown 
from witanime.video_providers.drive import get_drive_ids_from_episode
from witanime.video_providers.mediafire import get_mediafire_links_from_episode
from witanime.anime_site.witanime import get_episodes_list, get_search_results_link
import argparse

def download_from_mediafire(episode_link, output_path):
    import mediafire_dl
    mediafire_links = get_mediafire_links_from_episode(episode_link)
    if len(mediafire_links) == 0:
        print(f"No mediafire links found for {episode_link}")
        return
    for link in mediafire_links:
        try:
            mediafire_dl.download(link, str(output_path),quiet=False)
            return
        except ValueError:
            print(f"Error downloading {link}")
            print(f"you may visit {episode_link} to download it manually")

def clean(output_dir):
    if len(list(output_dir.iterdir())) <= 1:
        print("Deleting directory")
        output_dir.rmdir()    
# %%
def main():
    parser = argparse.ArgumentParser(description='Download anime from witanime.org')
    parser.add_argument('search_term', metavar='search_term', type=str)
    args = parser.parse_args()
    search_term = args.search_term
    search_results = get_search_results_link(search_term)
    if len(search_results) == 0:
        print("No results found")
        return
    for i, result in enumerate(search_results):
        print(f"{i+1}. {result}")
    anime_index = input("Enter anime index: ")
    anime_link = search_results[int(anime_index)-1]

    episodes_link = get_episodes_list(anime_link)
    print(f'{len(episodes_link)} episodes found')
    output_dir = Path(anime_link.split('/')[-2])
    output_dir.mkdir(exist_ok=True)
    for i, episode_link in enumerate(episodes_link):
        try:
            drive_ids = get_drive_ids_from_episode(episode_link)
            ouptut_file = f"{anime_link.split('/')[-2]}_EP{i+1}.mp4"
            print(f"{i+1}/{len(episodes_link)} {ouptut_file}")
            if len(drive_ids) == 0:
                print(f"No drive links found for {ouptut_file}")
    
            for drive_id in drive_ids:
                try:
                    if not gdown.download(id=drive_id, output=str(output_dir/ouptut_file)):
                        print(f"Failed to download from Drive, trying next link")
                    else:
                        break
                except ValueError:
                            print(f"Error downloading https://drive.google.com/file/d/{drive_id}/view")
                            print(f"you may visit {episode_link} to download it manually")
                            download_from_mediafire(episode_link, output_dir/ouptut_file)
            else:
                print(f"all {len(drive_ids)} drive links failed, trying mediafire")
                download_from_mediafire(episode_link, output_dir/ouptut_file)
        except KeyboardInterrupt:
            print("Exiting...")
            # if output_dir is empty delete it
            clean(output_dir)
            return

if __name__ == "__main__":
    main()
# %%
