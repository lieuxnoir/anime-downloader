import logging
import requests
import re
from bs4 import BeautifulSoup

from anime_downloader.extractors.base_extractor import BaseExtractor


class RapidVideo(BaseExtractor):
    def _get_data(self):
        url = self.url
        logging.debug('Calling Rapid url: {}'.format(url))
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        # TODO: Make these a different function. Can be reused in other classes
        #       too
        title_re = re.compile(r'"og:title" content="(.*)"')
        image_re = re.compile(r'"og:image" content="(.*)"')

        try:
            stream_url = soup.find_all('source')[0].get('src')
        except IndexError:
            stream_url = None
        try:
            title = str(title_re.findall(r.text)[0])
            thumbnail = str(image_re.findall(r.text)[0])
        except Exception as e:
            title = ''
            thumbnail = ''
            logging.debug(e)
            pass

        return {
            'stream_url': stream_url,
            'meta': {
                'title': title,
                'thumbnail': thumbnail,
            },
        }