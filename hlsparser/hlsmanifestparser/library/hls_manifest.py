"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Build a class to get Manifest, submanifest, video and
audio chunks
"""
import re
from hlsmanifestparser.library import basic


class HLSManifest():
    """HLS Asset objects

    Attributes:
        * asset_url
        * manifest_text
        * submanifest_text_url
        * submanifest_text
        * subtitles_info_list
        * audio_info_list
        * video_info_list
        * asset_json
        * sub_manifest_url
        * asset_files

    Init parameter(s):
        - asset_url
    Returns:
        - HLSManifest object of the given URL and
          the rest of the attibutes empty
    """
    asset_url = ""
    manifest_text = ""
    submanifests_url = ""
    submanifests_text = ""
    subtitles_info_list = []
    audio_info_list = []
    video_info_list = []
    asset_json = {"audio": {}, "video": {}, "subtitles": {}}
    sub_manifest_url = {"audio": {}, "video": {}, "subtitles": {}}
    asset_files = {"audio": {}, "video": {}, "subtitles": {}}

    def __init__(self, asset_url):
        super(HLSManifest, self).__init__()
        self.asset_url = asset_url
        self.clear_variables()

    def clear_variables(self):
        """
        Clear variables for new request
        """
        self.manifest_text = ""
        self.submanifests_url = ""
        self.submanifests_text = ""
        self.subtitles_info_list = []
        self.audio_info_list = []
        self.video_info_list = []
        self.asset_json = {"audio": {}, "video": {}, "subtitles": {}}
        self.sub_manifest_url = {"audio": {}, "video": {}, "subtitles": {}}
        self.asset_files = {"audio": {}, "video": {}, "subtitles": {}}

    def get_manifest_text(self):
        """
        Get manifest response base on given URL

        Output:
        if works:
         - self.manifest_text = [str] HLS manifest information
         - tuple with ([200|304], True)
        if does not work:
         - tuple with (None, False)

        NOTE: self.asset_url should not be empty
        """
        manifest_text = basic.get_request(self.asset_url)
        if manifest_text:
            if manifest_text.status_code == 200 or manifest_text.status_code == 304:
                self.manifest_text = manifest_text.text
                return (manifest_text.status_code, True)
        return (None, False)

    def parse_manifest(self):
        """
        Parse Manifest to JSON, including video and audio info
        """
        self.parse_audio()
        self.parse_video()
        self.parse_subtitles()

    # Build submanifest URL ########################

    def build_submanifest_url(self, base_url, p_num, c_type="video"):
        """
        Build the submanifest URL of the given asset
        Parameters:
            - base_url: [str] is the CDN/Origin URL that will helps
                to create the URL
            - p_num: [int] video/audio/subtitle profile to be retrieve
        Output:
            - self.submanifest_url [dict] filled with submanifest urls
        NOTE: self.manifest_text should not be empty
        """
        if f"{c_type}_{p_num}" in self.asset_json[f"{c_type}"].keys():
            submani_url = self.asset_json[f"{c_type}"][f"{c_type}_{p_num}"]["URI"]
            temp_va = f"{base_url}{submani_url}"
            self.sub_manifest_url[f"{c_type}"][f"sub_manifest_{p_num}"] = temp_va
            return True

    def extract_files_from_submanifest(self, sub_manifest_url, c_type="video"):
        """
        Given the selected sub_manifest URL, it extract files
        Parameters:
            - sub_manifest_url [str] selected sub manifest url
        Output:
            - self.asset_files [dict] of all videos in the submanifest
        """
        submanifest_text = basic.get_request(sub_manifest_url)
        counter = 0
        if submanifest_text:
            if submanifest_text.text != "":
                for item in submanifest_text.text.split("\n"):
                    if "#EXT" not in item and item != "":
                        self.asset_files[f"{c_type}"][f"{counter}"] = item.replace("\r", "")
                        counter += 1
                return True

    # Build sub-manifest URL END ####################

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
        Get asset's video(s) paramaters from manifest as list
        Output:
            - self.video_info_list [list] with all video profile info
            Return True

        NOTE: self.manifest_text should have manifest information
        If self.manifest_text is empty, it returns False
        """
        video_profiles = []
        if self.manifest_text != "":
            self.video_info_list = [
                    (profile, self.manifest_text.split()[index + 1])\
                            for index, profile in enumerate(self.manifest_text.split())\
                            if "RESOLUTION" in profile and "#EXT-X-I-FRAME" not in profile]
            return True

    def parse_video_to_json(self):
        """
        Parse information from list to json
        Output:
            - self.asset_json["video"] [dict] with all video information
              returns True

        NOTE: self.video_info_list should have information
        if self.video_info_list is empty, it returns False
        """
        vid_num = 0
        video_json = {}
        pattern = ",([A-Z]*)="
        if len(self.video_info_list) > 0:
            for items in self.video_info_list:
                video_json[f"video_{vid_num}"] = {}
                separated_item = list(
                    filter(None, re.split(pattern, items[0])))
                for video_i in enumerate(separated_item):
                    if video_i[0] % 2 != 0:
                        v_key = separated_item[video_i[0]]
                        v_value = separated_item[video_i[0] + 1]
                        video_json[f"video_{vid_num}"][v_key] = v_value.replace(
                            "\"", "").replace("\r", "")
                video_json[f"video_{vid_num}"]["URI"] = items[1].replace(
                    "\"", "").replace("\r", "")
                vid_num += 1
            self.asset_json["video"] = video_json
            return True

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
        Get asset's audio(s) paramaters from manifest as list
        Output:
            - self.audio_info_list [list] with all audio profile info
            Return True

        NOTE: self.manifest_text should have manifest information
        If self.manifest_text is empty, it returns False
        """
        audio_list = []
        if self.manifest_text != "":
            self.audio_info_list = [
                    audio for audio in self.manifest_text.split() if "TYPE=AUDIO" in audio]
            return True

    def parse_audio_to_json(self):
        """
        Parse information from list to json
        Output:
            - self.asset_json["audio"] [dict] with all audio information
            return True

        NOTE: self.audio_info_list should have information
        if self.audio_info_list is empty, it returns False
        """
        audio_json = {}
        audio_num = 0
        pattern = ",([A-Z]*)="
        if len(self.audio_info_list) > 0:
            for audio in self.audio_info_list:
                audio_json[f"audio_{audio_num}"] = {}
                list_sub = list(filter(None, re.split(pattern, audio)))
                for item in enumerate(list_sub):
                    if item[1].isupper() and 'YES' not in item[1]:
                        audio_json[f"audio_{audio_num}"][item[1]] = list_sub[item[0]+1].replace(
                            "\"", ""
                        ).replace("\r", "")
                audio_num += 1
            self.asset_json["audio"] = audio_json
            return True

    # Audio parse section END ######################

    # Subtitles parse section ##########################

    def parse_subtitles(self):
        """
        Parse all subtitles info, calling methods:
            - get_subtitles_information
            - parse_subtitles_to_json
        As a result this will handle all the information that manifest
        have about subtitles
        """
        self.get_subtitles_information()
        self.parse_subtitles_to_json()

    def get_subtitles_information(self):
        """
        Get asset's subtitle(s) paramaters from manifest as list
        Output:
            - self.subtitle_info_list [list] with all subtitle profile info
            Return True

        NOTE: self.manifest_text should have manifest information
        If self.manifest_text is empty, it returns False
        """
        subtitles_list = []
        if self.manifest_text != "":
            self.subtitles_info_list = [sub for sub in self.manifest_text.split() if "TYPE=SUBTITLES" in sub]
            return True

    def parse_subtitles_to_json(self):
        """
        Parse information from list to json
        Output:
            - self.asset_json["subtitles"] [dict] with all subtitles information
        NOTE: self.subtitles_info_list should have information
        """
        subtitles_json = {}
        sub_num = 0
        pattern = ",([A-Z]*)="
        if len(self.subtitles_info_list) > 0: 
            for subtitles in self.subtitles_info_list:
                subtitles_json[f"subtitles_{sub_num}"] = {}
                list_sub = list(filter(None, re.split(pattern, subtitles)))
                for item in enumerate(list_sub):
                    if item[1].isupper() and 'YES' not in item[1]:
                        subtitles_json[f"subtitles_{sub_num}"][item[1]] = list_sub[item[0]+1].replace(
                            "\"", ""
                        )
                sub_num += 1
            self.asset_json["subtitles"] = subtitles_json
            return True

    # Subtitles parse section END ######################

