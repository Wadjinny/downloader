#%%
from requests import get, head, post, packages
from bs4 import BeautifulSoup as soup


def get_size(content):
	size_in_bytes = len(content)
	size_in_mb = round( size_in_bytes / 1024 / 1024, 2 )
	return size_in_mb


class File:
	def __init__(self, name='',  url='', res=''):
		self.headers = res.headers
		self.name = name.replace(':', '')
		self.url = url
		self.content = res.content
		self.size = get_size(res.content)

		self.info = f'Name: {self.name}\nUrl: {self.url}\nSize: {self.size}'

	def save(self, path=''):
		open( path+self.name, 'wb' ).write(self.content)

	def save_as(self, name, path=''):
		open( name, 'wb' ).write(self.content)



class _4shared:
    def get_name_from_vid_id(vid_id):
            url = 'https://www.4shared.com/video/'+vid_id
            return soup( get(url).text, 'html.parser' ).find('div', {'class':'file-name'}).text\

    def get_vid_url(vid_id):
            url = 'https://www.4shared.com/web/embed/file/'+vid_id
            vid_url = soup( get(url).text, 'html.parser' ).find('source')['src']
            return vid_url

    def download(vid_id):
            url = 'https://www.4shared.com/web/embed/file/'+vid_id
            file_name = _4shared.get_name_from_vid_id(vid_id)
            res = get( _4shared.get_vid_url(vid_id) ) 

            return File(url=url, name=file_name, res=res)

    def available(vid_id):
        url = 'https://www.4shared.com/video/'+vid_id
        res = get(url).text
        if 'The file link that you requested is not valid' in res:
            return False
        else:
            return True
        
        
# %%
_4shared.download('3uHXdB6Pku')