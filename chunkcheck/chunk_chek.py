"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Build a class to get Manifest, sub-manifest, video and
audio chunks
"""
import re
import os
import platform
import threading
from random import randint
from basic import (
    # head_request,
    get_request,
    post_request,
    load_streamnames_from_file
)


# Check random profile or disable and define
# the profile to check
# OPTIONS = (V_PROFILE, NUM_CHUNKS_TOB_CHECK, RANDOM_PROFILES, ASSET_LIST)
if platform.system() != 'Linux':
    OPTIONS = (5, 10, False, "asset_list.yaml")
    # ABR Server IP
    ABR_MANIFEST_SERVER_IP = "localhost"
    ABR_MANIFEST_SERVER_PORT = 8000
else:
    V_PROFILE = int(os.getenv("V_PROFILE"))
    NUM_CHUNKS_TOB_CHECK = int(os.getenv("NUM_CHUNKS_TOB_CHECK"))
    RANDOM_PROFILES = bool(os.getenv("RANDOM_PROFILES"))
    ASSET_LIST = os.getenv("ASSET_LIST")
    OPTIONS = (V_PROFILE, NUM_CHUNKS_TOB_CHECK, RANDOM_PROFILES, ASSET_LIST)
    ABR_MANIFEST_SERVER_IP = os.getenv("ABR_MANIFEST_SERVER_IP")
    ABR_MANIFEST_SERVER_PORT = os.getenv("ABR_MANIFEST_SERVER_PORT")

# Load asset URLs
URLS = load_streamnames_from_file(OPTIONS[3])
ABR_HLS_PARSER = f"http://{ABR_MANIFEST_SERVER_IP}:{ABR_MANIFEST_SERVER_PORT}/hlsmanifest/"


class Chunk:
    """Chunk to be check

    This object has a basic HTTP caracteristic
    of an HTTP Chunk, could be video, audio or
    subtitle
    """

    def __init__(self, chunk_url):
        self.chunk_url = chunk_url

    def get_http_chunk_info(self):
        """To avoid traffic overload on the
        network, a simple head validation will
        be execute
        """
        return get_request(self.chunk_url)


def get_parsed_manifest(manifest_url):
    """
    Get data from hlsparser, developed by Gio
    """
    manifest_data = {"manifest_url": manifest_url}

    return post_request(ABR_HLS_PARSER, body=manifest_data)


def channel_check(manifest_url):
    """
    Manifest parser request
    """
    parsed_manifest = get_parsed_manifest(manifest_url)

    if parsed_manifest:
        json_manifest = parsed_manifest.json()
        sub_manifests = json_manifest["sub_manifest"]
        vid_prof_num = len(sub_manifests["video"])
        # au_prof_num = len(sub_manifests["audio"])
        # sub_prof_num = len(sub_manifests["subtitles"])
        if OPTIONS[0] >= vid_prof_num:
            v_prof = vid_prof_num - 1
        else:
            v_prof = OPTIONS[0]

        if OPTIONS[2]:
            v_prof = randint(0, vid_prof_num)
        if f"sub_manifest_{v_prof}" in sub_manifests["video"].keys():
            selected_profile = sub_manifests["video"][f"sub_manifest_{v_prof}"]
            chunk_base_url = list(
                filter(None, re.split(r"/\w*.m3u8(.*?)", selected_profile)))
            chunks = json_manifest["asset_chunks"]
            if len(chunks["video"]) > OPTIONS[1]:
                for item in range(
                        len(chunks["video"]) - 2,
                        (len(chunks["video"]) - 2 - int(OPTIONS[1])), - 1):
                    chunk = Chunk(f'{chunk_base_url[0]}/{chunks["video"][str(item)]}')
                    chunk.get_http_chunk_info()
                    # if chunk_headers:
                    #     print(chunk_headers.headers)


def recursion_channel_check(manifest_urls):
    """
    Given a list of URLs, do a thread execution by URL, amazing fast
    """

    if len(manifest_urls) == 1:
        my_thread = threading.Thread(target=channel_check, args=(manifest_urls[0],))
        my_thread.start()
    else:
        mid1 = manifest_urls[:len(manifest_urls)//2]
        mid2 = manifest_urls[len(manifest_urls)//2:]
        recursion_channel_check(mid1)
        recursion_channel_check(mid2)


def main():
    """
    Main executing function
    """
    recursion_channel_check(URLS)


if __name__ == '__main__':

    main()
