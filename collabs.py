import time
import re
import random
import urllib3
import requests
import streamlit as st
import googleapiclient.discovery
from stvis import pv_static
from pyvis.network import Network
from collections import Counter
from xml.etree import ElementTree

@st.experimental_memo(max_entries=1)
def get_data(cache=False):
    if cache: return

    urllib3.disable_warnings()
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=st.secrets["youtube_key"])

    vwiki = "https://hololive.wiki/w/api.php"
    params = {
        "action": "parse",
        "page": "Hololive Japan",
        "section": "1",
        "format": "json"
    }
    response = requests.get(url=vwiki, params=params)
    channel_names = [i['*'] for i in response.json()['parse']['links']]
    banlist = ['Mano Aloe', 'Hitomi Chris']
    channel_names = [name for name in channel_names if name not in banlist]

    # get a map of channel link to name
    channel_map = {}
    for name in channel_names:
        params = {
            "action": "query",
            "format": "xml",
            "prop": "revisions",
            "rvprop": "content",
            "titles": name,
            "rvsection": "0"
        }

        response = requests.get(url=vwiki, params=params)
        tree = ElementTree.fromstring(response.content)

        for child in tree[1][0][0][0]:
            channel_map[re.search('UC[\w\-]+',child.text).group(0)] = name

    def get_playlist(playlist_id, cursor=''):
        """Generator to get playlist items from youtube API"""

        while cursor is not None:
            # fetch data
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=cursor
            )
            try:
                response = request.execute()
            except Exception as E:
                print(E)
                return None
            
            for item in response['items']:
                yield item

            # fetch new token
            try:
                cursor = response['nextPageToken']
            except KeyError:
                cursor = None

    link_counter = {}
    for channel, name in channel_map.items():
        url_counter = Counter()
        # changing the 'UC' at the beginning to 'UU' gets you
        # the id of the uploads playlist
        upload_id = 'UU' + channel[2:]
        for item in get_playlist(upload_id):
            if item:
                for url in set(re.findall('http.+?(?=[ \n])', item['snippet']['description'])):
                    url_counter.update({url: 1})
        
        link_counter[channel] = url_counter

    collab_map = {}
    for channel in link_counter:
        channel_counter = Counter()
        pattern = r'\/channel\/(.*?((?=[\?\n\/])|$))' # extracts channel
        
        for url in link_counter[channel]:
            try:
                if 'https://t.co' in url:
                    channel_counter.update({re.search(pattern, requests.get(url, verify=False).url).group(1): link_counter[channel][url]})
                elif 'https://www.youtube.com/channel' in url:
                    channel_counter.update({re.search(pattern, url).group(1): link_counter[channel][url]})
            except AttributeError: # Usually when a shortened link is a video
                continue
            except Exception as e:
                print(e)
                print(url)
        collab_map[channel] = channel_counter

    edge_counter = Counter()
    for parent in collab_map:
        for child in collab_map[parent]:
            try:
                edge_counter.update({frozenset((channel_map[parent], channel_map[child])): collab_map[parent][child]})
            except KeyError:
                continue

    def get_channels(channel_list):
        """Get all channels in a list in bulk requests"""
        for i in range(0, len(channel_list), 50):
            request = youtube.channels().list(
                part="snippet",
                id=",".join(channel_list[i:i+50]),
                maxResults=50
            )
            response = request.execute()
            
            for item in response['items']:
                yield item

    # id to pfp map
    pfp_map = {}
    for item in get_channels(list(channel_map)):
        pfp_map[channel_map[item['id']]] = item['snippet']['thumbnails']['medium']['url']

    return channel_map, edge_counter, pfp_map, time.strftime('%b %d, %Y')

# yeet edges below this
limit = st.sidebar.slider('Minimum Collab Filter', 0, 30, 5)

# rerun and update cache
# have to do it this way because streamlit doesn't have a programmatic 
# way to clear cache, for some inane reason 
if st.sidebar.button("Rerun"):
    get_data(True)
    st.experimental_rerun()

channel_map, edge_counter, pfp_map, last_run = get_data()

r = lambda: random.randint(0,255)
random_hex = lambda: f'#{r():02X}{r():02X}{r():02X}'

net = Network(notebook=True, height='706px', width='706px', bgcolor="#222222", font_color="white", heading='')
net.barnes_hut(spring_length=100)

for node in channel_map.values():
    try:
        net.add_node(node, shape='circularImage', image=pfp_map[node], color=random_hex())
    except KeyError:
        continue

for edge in edge_counter:
    if len(edge) == 2:
        if edge_counter[edge] > limit:
            net.add_edge(*edge, value=edge_counter[edge], title=edge_counter[edge])

st.caption(f"Last run on {last_run}.")
pv_static(net)