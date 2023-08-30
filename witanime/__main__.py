#%% search
from pathlib import Path
import gdown 
from witanime.video_providers.drive import drive_dowload
from witanime.video_providers.mediafire import download_from_mediafire
from witanime.video_providers.meganz import meganz_dowload
from witanime.anime_site.witanime_extractor import get_episodes_list, get_search_results_link
import argparse
from glob import glob


def clean(output_dir):
    if len(glob(f"{output_dir}/*.mp4")) == 0:
        print("Deleting directory")
        for f in output_dir.glob('*'):
            f.unlink()
        output_dir.rmdir()    
# %%
def main():
    parser = argparse.ArgumentParser(description='Download anime from witanime.org')
    parser.add_argument('search_term', metavar='search_term', type=str)
    # add boolean argument -r, if present range will be asked, by default it will False
    parser.add_argument('-r', action='store_true', help='download range of episodes')
    
    
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
    anime_link = search_results[int(anime_index)-1]

    episodes_link = get_episodes_list(anime_link)
    print(f'{len(episodes_link)} episodes found')
    
    output_dir = Path(anime_link.split('/')[-2])
    output_dir.mkdir(exist_ok=True)
    if args.r:
        selection = input("episode range: ")
        # remove spaces
        selection = selection.replace(' ', '')
        # for example 1, 3-5, 7
        selector = [False]*len(episodes_link)
        for part in selection.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                selector[start-1:end] = [True]*(end-start+1)
            else:
                selector[int(part)-1] = True
        episodes_link = [link for link, select in zip(episodes_link, selector) if select]

    for i, episode_link in enumerate(episodes_link):
        try:
            ouptut_file = f"{anime_link.split('/')[-2]}_EP{i+1}.mp4"
            print(f"{i+1}/{len(episodes_link)} {ouptut_file}")
            if not drive_dowload(episode_link, ouptut_file, output_dir):
                print("Downloading from mediafire")
            if not download_from_mediafire(episode_link, output_dir, ouptut_file):
                print("Downloading from mega.nz")
            if not meganz_dowload(episode_link, output_dir, ouptut_file):
                print(f"Failed to download {ouptut_file}")
            
        except KeyboardInterrupt:
            print("Exiting...")
            # if output_dir is empty delete it
            clean(output_dir)
            return

if __name__ == "__main__":
    main()
# %%
