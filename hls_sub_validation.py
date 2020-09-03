'''
# curl -XPOST -H'Content-type:application/json' 'http://localhost:8001/hlsmanifest/' -d '{"asset_name": "playlist.m3u8","base_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/"}' | python -m json.tool
https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
'''
import re
import sys
import json
import requests
import threading
from datetime import datetime


def requesting(s_url):
    sub_response = requests.get(s_url)
    print(sub_response.text)


def recursion_requested_manifest(url, subtitles):

    if len(subtitles) == 1:
        sub_url = f'{url}{subtitles[0]}'
        # print('!' * 150)
        # print(sub_url)
        x = threading.Thread(target=requesting, args=(sub_url,))
        x.start()
    else:
        mid1 = subtitles[:len(subtitles) // 2]
        mid2 = subtitles[len(subtitles) // 2:]
        recursion_requested_manifest(url, mid1)
        recursion_requested_manifest(url, mid2)


def iterated_requested_manifest(url, subtitles):
    for sub in subtitles:
        sub_url = f'{url}{sub}'
        # print('!' * 150)
        # print(sub_url)
        sub_response = requests.get(sub_url)
        print(sub_response.text)


def print_url(response, base_url):
    subtitles = response.json()["asset_chunks"]["subtitles"]
    subtitles = list(subtitles.values())
    recursion_requested_manifest(base_url, subtitles)
    # iterated_requested_manifest(sub_temp, subtitles)

def get_base_url_and_asset_name(url):
    pattern = r'\w*\.m3u8(\?.*)?'
    match = re.search(pattern, url)
    base_url = url.split(match.group())[0]
    return base_url, match.group()

if __name__ == "__main__":
    startTime = datetime.now()

    # Define Asset variables
    # MANIFEST = 'https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8'
    MANIFEST = input("Enter the URL (ex: https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8):\n")
    base_url, asset_name = get_base_url_and_asset_name(MANIFEST)

    # Server request
    URL = 'http://localhost:8001/hlsmanifest/'
    HEADERS = {'Content-type': 'application/json'}
    DATA = {
        "asset_name": asset_name,
        "base_url": base_url}

    # HLS Parser request
    response = requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

    # Parse subtitles
    sub_dict = response.json().get("sub_manifest", None)
    if response.status_code == 200 and sub_dict:
        sub_url = sub_dict["subtitles"].get("sub_manifest_0", {})
        if sub_url:
            base_url, asset_name = get_base_url_and_asset_name(sub_url)
            print_url(response, base_url)

    endTime = datetime.now()
    deltaTime = endTime - startTime
    print(f"Started at: {startTime} and end at: {endTime}. Total time = {deltaTime}")
