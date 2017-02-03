import os
import json
import shutil
from jinja2 import Environment, ChoiceLoader, FileSystemLoader


def strftime(value, format):
    return value.strftime(format)


def youtube_playlist(playlist_id):
    import urllib.request
    import datetime

    videos = []
    pageToken = ''
    while True:
        # The key is restricted to some IP https://console.developers.google.com/apis/credentials?project=documentation-151710
        url = "https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" + playlist_id + "&key=AIzaSyCLXG1nmMPfJ_fWgTlikFpc5f_7LVyhioE&part=snippet&maxResults=50&pageToken=" + pageToken
        with urllib.request.urlopen(url) as data:
            content = json.loads(data.read().decode())
            for item in content["items"]:
                video = {}
                video['id'] = item['snippet']['resourceId']['videoId']
                video['date'] = datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
                video['title'] = item['snippet']['title']
                videos.append(video)
            if 'nextPageToken' not in content:
                break
            pageToken = content['nextPageToken']
    return videos


def youtube_channel(channel_id):
    import xml.etree.ElementTree as ET
    import urllib.request
    import datetime

    url = "https://www.youtube.com/feeds/videos.xml?max-results=50&channel_id=" + channel_id
    videos = []
    with urllib.request.urlopen(url) as f:
        root = ET.parse(f).getroot()
        for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
            video = {}
            video['id'] = entry.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
            video['date'] = datetime.datetime.strptime(entry.find('{http://www.w3.org/2005/Atom}published').text, '%Y-%m-%dT%H:%M:%S+00:00')
            video['title'] = entry.find('{http://www.w3.org/2005/Atom}title').text
            videos.append(video)
    return videos


class Theme:
    def __init__(self, export_dir):
        self._export_dir = export_dir

        if os.path.exists(os.path.join(export_dir, 'theme')):
            shutil.rmtree(os.path.join(export_dir, 'theme'))
        shutil.copytree('theme', os.path.join(export_dir, 'theme'))

        self._env = Environment(loader=ChoiceLoader([
            FileSystemLoader(os.path.join(export_dir, 'theme')),
        ]))
        self._env.filters['strftime'] = strftime
        self._env.filters['youtube_channel'] = youtube_channel
        self._env.filters['youtube_playlist'] = youtube_playlist
        self._env.filters['theme'] = self._theme

    def _theme(self, asset_file):
        """
        Add a checksum to theme file from the template to avoid cache
        issues
        """
        import hashlib

        path = os.path.join(self._export_dir, 'theme', asset_file)
        if not os.path.exists(path):
            path = os.path.join('theme', asset_file)

        h = hashlib.md5()
        with open(path, 'rb') as f:
            h.update(f.read())
        return 'theme/' + asset_file + '?sum=' + h.hexdigest()


    def render(self, template, root='.', **kwargs):
        template = self._env.get_template(template)
        return template.render(root=root, **kwargs)
