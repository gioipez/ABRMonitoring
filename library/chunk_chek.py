"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Build a class to get Manifest, submanifest, video and
audio chunks
"""
import re
from random import randint
from basic import head_request, post_request


class Chunk():
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
        url = self.chunk_url
        response = head_request(url)
        print(response.headers)


if __name__ == '__main__':
    # Check random profile or disable and define
    # the profile to check
    RANDOM_PROFILES = False
    V_PROF = 0
    NUM_CHUN_TOB_CHECK = 10

    # Build Manifest
    ASSET_NAME = "playlist.m3u8?algo=0"
    BASE_URL = "https://bitdash-a.akamaihd.net/content/sintel/hls/"
    manifest_url = f"{BASE_URL}{ASSET_NAME}"
    manifest_data = {"asset_name": ASSET_NAME, "base_url": BASE_URL}

    # ABR Server IP
    ABR_MANIFEST_SERVER_IP = "localhost"
    ABR_MANIFEST_SERVER_PORT = 8001
    abr_hls_parser = f"http://{ABR_MANIFEST_SERVER_IP}:{ABR_MANIFEST_SERVER_PORT}/hlsmanifest/"

    # Manifest parser request
    parsed_manifest = post_request(abr_hls_parser, body=manifest_data)

    if parsed_manifest:
        json_manifest = parsed_manifest.json()
        sub_manifests = json_manifest["sub_manifest"]
        vid_prof_num = len(sub_manifests["video"])
        au_prof_num = len(sub_manifests["audio"])
        sub_prof_num = len(sub_manifests["subtitles"])
        if RANDOM_PROFILES:
            V_PROF = randint(0, vid_prof_num)
        selected_profile = sub_manifests["video"][f"sub_manifest_{V_PROF}"]
        chunk_base_url = list(
            filter(None, re.split(r"/\w*.m3u8(.*?)", selected_profile)))
        print(chunk_base_url[0])
        print(V_PROF)
        chunks = json_manifest["asset_chunks"]
        for item in range(
                len(chunks["video"]) - 2,
                (len(chunks["video"]) - 2 - NUM_CHUN_TOB_CHECK), -1):
            chunk = Chunk(f'{chunk_base_url[0]}/{chunks["video"][str(item)]}')
            chunk.get_http_chunk_info()
    else:
        print('Error trying to get manifest')
