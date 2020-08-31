'''
# curl -XPOST -H'Content-type:application/json' 'http://localhost:8001/hlsmanifest/' -d '{"asset_name": "playlist.m3u8","base_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/"}' | python -m json.tool
https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8
'''
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


def print_url(respinse, streamname):
    if response.status_code == 200:
        subtitles = response.json()["asset_chunks"]["subtitles"]
        subtitles = list(subtitles.values())
        sub_temp = f"https://bitdash-a.akamaihd.net/content/sintel/hls/"
        recursion_requested_manifest(sub_temp, subtitles)
        # iterated_requested_manifest(sub_temp, subtitles)


if __name__ == "__main__":
    startTime = datetime.now()

    channel = "hbo2hdchi"
    URL = 'http://localhost:8001/hlsmanifest/'
    HEADERS = {'Content-type': 'application/json'}
    DATA = {
        "asset_name": "playlist.m3u8",
        "base_url": f"https://bitdash-a.akamaihd.net/content/sintel/hls/"}
    response = requests.post(URL, data=json.dumps(DATA), headers=HEADERS)

    print_url(response, channel)
    endTime = datetime.now()
    deltaTime = endTime - startTime
    print(f"Started at: {startTime} and end at: {endTime}. Total time = {deltaTime}")
