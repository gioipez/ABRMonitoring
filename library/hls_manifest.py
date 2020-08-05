"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Build a class to get Manifest, submanifest, video and
audio chunks
"""
import re
import json
import basic


class HLSManifest():
    """HLS Asset objects

    Attributes:
        * asset_url
        * manifest_text
        * submanifest_text_url
        * submanifest_text

    Parameters:
        - asset_url
    Returns:
        - HLSManifest object of the given URL
    """
    asset_url = ""
    manifest_text = ""
    submanifests_url = ""
    submanifests_text = ""
    audio_info_list = ""
    audio_json = {}
    video_info_list = []
    video_json = {}
    sub_manifest_url = {}
    video_files = {}

    def __init__(self, asset_url):
        super(HLSManifest, self).__init__()
        self.asset_url = asset_url

    def get_manifest_text(self):
        """
        Get manifest response base on given URL
        Output:
            - self.manifest_text = [str] HLS manifest information
        NOTE: self.asset_url should not be empty
        """
        manifest_text = basic.get_request(self.asset_url)
        if manifest_text:
            self.manifest_text = manifest_text.text

    def parse_manifest(self):
        """
        Parse Manifest to JSON, including video and audio info
        """
        self.parse_audio()
        self.parse_video()

    # Build submanifest URL ########################

    def build_submanifest_url(self, base_url, profile_number):
        """
        Build the submanifest URL of the given asset
        Parameters:
            - base_url: [str] is the CDN/Origin URL that will helps
                to create the URL
            - profile_number: [int] video profile that will be retrieve
        Output:
            - self.submanifest_url [dict] filled with submanifest urls
        NOTE: self.manifest_text should not be empty
        """
        video_url = self.video_json[f"video_{profile_number}"]["URI"]
        temp_va = f"{base_url}{video_url}"
        self.sub_manifest_url[f"sub_manifest_{profile_number}"] = temp_va

    def extract_video_files_from_submanifest(self, sub_manifest_url):
        """
        Given the selected sub_manifest URL, it extract
        Parameters:
            - sub_manifest_url [str] selected sub manifest url
        Output:
            - self.video_files [dict] of all videos in the submanifest
        """
        submanifest_text = basic.get_request(sub_manifest_url)
        video_chunk = 0
        if submanifest_text:
            for item in submanifest_text.text.split("\n"):
                if "#EXT" not in item and item != "":
                    self.video_files[f"{video_chunk}"] = item
                    video_chunk += 1

    # Build submanifest URL END ####################

    # Video parse section ##########################

    def parse_video(self):
        """
        Parse all video info, callin methods:
            - get_video_information
            - parse_video_to_json
        As a result this will handle all the information that manifest
        have about video
        """
        self.get_video_information()
        self.parse_video_to_json()

    def get_video_information(self):
        """
        Get video(s) URL from manifest as list
        Output:
            - self.video_info_list [list] with all video profile info
        NOTE: self.manifest_text should have manifest information
        """
        video_profiles = []
        for items in enumerate(self.manifest_text.split("\n")):
            info = items[1]
            if "RESOLUTION" in info and "#EXT-X-I-FRAME" not in info:
                video_profiles.append((
                    info,
                    self.manifest_text.split("\n")[items[0] + 1]))
        self.video_info_list = video_profiles

    def parse_video_to_json(self):
        """
        Parse information from list to json
        Output:
            - self.video_json [dict] with all video information
        NOTE: self.video_info_list should have information
        """
        vid_num = 0
        video_json = {}
        for items in self.video_info_list:
            video_json[f"video_{vid_num}"] = {}
            separated_item = list(
                filter(None, re.split(",([A-Z]*)=", items[0])))
            for video_i in enumerate(separated_item):
                if video_i[0] % 2 != 0:
                    v_key = separated_item[video_i[0]]
                    v_value = separated_item[video_i[0] + 1]
                    video_json[f"video_{vid_num}"][v_key] = v_value.replace(
                        "\"", "").replace("\r", "")
            video_json[f"video_{vid_num}"]["URI"] = items[1].replace(
                "\"", "").replace("\r", "")
            vid_num += 1
        self.video_json = video_json

    # Video parse section END ######################

    # Audio parse section ##########################

    def parse_audio(self):
        """
        Parse all audio info, calling methods:
            - get_audio_information
            - parse_audio_to_json
        As a result this will handle all the information that manifest
        have about audio
        """
        self.get_audio_information()
        self.parse_audio_to_json()

    def get_audio_information(self):
        """
        Get audio(s) URL from manifest as list
        Output:
            - self.audio_info_list [list] with all audio profile info
        NOTE: self.manifest_text should have manifest information
        """
        audio_list = []
        for items in self.manifest_text.split("\n"):
            if "TYPE=AUDIO" in items:
                audio_list.append(items)
        self.audio_info_list = audio_list

    def parse_audio_to_json(self):
        """
        Parse information from list to json
        Output:
            - self.audio_json [dict] with all audio information
        NOTE: self.audio_info_list should have information
        """
        audio_json = {}
        au_t = []
        audio_num = 0
        for audio in self.audio_info_list:
            audio_json[f"audio_{audio_num}"] = {}
            for au_parameter in audio.split(","):
                au_t = au_parameter.split("=")
                audio_json[f"audio_{audio_num}"][au_t[0]] = au_t[1].replace(
                    "\"", ""
                )
            audio_num += 1
        self.audio_json = audio_json

    # Audio parse section END ######################

if __name__ == "__main__":
    # HLS URL
    DOMAIN = "bitdash-a.akamaihd.net"
    FILE_NAME = "f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8"
    BASE_URL = f"https://{DOMAIN}/content/MI201109210084_1/m3u8s/"
    SAMPLE_URL = f"{BASE_URL}{FILE_NAME}"

    # HLS Object creation
    hls_object = HLSManifest(SAMPLE_URL)
    hls_object.get_manifest_text()
    hls_object.parse_manifest()

    # Submaniefst build
    for profiles in range(5):
        hls_object.build_submanifest_url(BASE_URL, profiles)

    # Build video URL
    hls_object.extract_video_files_from_submanifest(
        hls_object.sub_manifest_url["sub_manifest_0"])

    print(json.dumps({
        "audio": hls_object.audio_json,
        "video": hls_object.video_json,
        "video_chunks": hls_object.video_files,
        "sub_manifest": hls_object.sub_manifest_url}))