import m3u8
import requests
import json
from urllib.parse import urlparse
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"}


class YoutubeVideo:
    def __init__(self, pos, video, **kwargs):
        self.pos = pos
        video = video.find('iframe')
        self.video_url = video['src']

    def json(self):
        return {
            'position': self.pos,
            'video_url': self.video_url,
        }

    def __str__(self):
        return f"""video_url: {self.video_url}"""

    def __repr__(self):
        return f"""video_url = {self.video_url}"""


class GamespotVideo:
    def __init__(self, pos, video, **kwargs):
        self.pos = pos
        self.root = None
        self.segment_num = None
        self.segment_duration = None
        self.get_video(video)

    def json(self):
        return {
            'position': self.pos,
            'root': self.root,
            'segment_num': self.segment_num,
            'segment_max_max': self.segment_duration
        }

    def get_video(self, v_data):
        v_data = v_data.find('div', {'class': 'js-video-player-new'})
        m3u8_url = json.loads(v_data['data-video'])['videoStreams']['adaptive_stream']

        if 'video.gamespot.com' in m3u8_url:
            full_root = self._get_full_root(m3u8_url, "360h700k")
        elif 'mt-rv-v1.gamespot.com' in m3u8_url:
            full_root = self._get_full_root(m3u8_url, "3200")
        elif 'cdn.jwplayer.com' in m3u8_url:
            r = requests.get(m3u8_url, headers=headers)
            m3u8_master = m3u8.loads(r.text)
            playlists = m3u8_master.data['playlists'][:-1]
            m3u8_url = list(filter(lambda x: '1280x' in x['stream_info']['resolution'], playlists))[0]
            full_root = m3u8_url['uri'].replace(".m3u8", "")
        else:
            raise Exception("wrong video link, did not recognized")

        self.root = full_root

        r = requests.get(full_root + ".m3u8", headers=headers)
        if r.status_code != 200:
            raise Exception("wrong video link, status code != 200")

        m3u8_master = m3u8.loads(r.text)
        self.segment_num = len(m3u8_master.data['segments'])
        self.segment_duration = m3u8_master.data['segments'][0]['duration']

    @staticmethod
    def _get_full_root(m3u8_url, resolution):
        url = urlparse(m3u8_url)
        path = url.path.split("/")
        head = f"{url.scheme}://{url.netloc}"
        root, value = "/".join(path[:-1]), "_".join(path[-1].split("_")[:-1])
        return f"{head}{root}/{value}_{resolution}"
