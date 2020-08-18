"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Module for test the HLSManifest class
"""
import unittest
from hls_manifest import HLSManifest

# Indicate if wants the asset with Subtitles and Audio
WITH_ALL = True
if WITH_ALL:
    ASSET_URL = "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
    BASE_URL = "https://bitdash-a.akamaihd.net/content/sintel/hls/"
    HAS_SUB = True
    HAS_AUDIO = True
else:
    ASSET_URL = "https://mnmedias.api.telequebec.tv/m3u8/29880.m3u8"
    BASE_URL = "https://mnmedias.api.telequebec.tv/m3u8/"
    HAS_SUB = False
    HAS_AUDIO = False

FAIL_URL = "http://184.72.239.149/vod/smil:BigBuckBunny.smil/playlist.m3u8"


class TestHLSManifest(unittest.TestCase):
    """
    This will test HLSManifest class
    """

    def setUp(self):
        tmp = ASSET_URL
        self.hls = HLSManifest(tmp)
        self.base_url = BASE_URL

    def test_manifest_text_with_failing_url(self):
        """
        method tested: get_manifest_text
        This is what will be done when the URL is wrong, that could mean
        HTTP_404_NOT_FOUND
        """
        expected = (None, False)
        self.hls.asset_url = FAIL_URL
        result = self.hls.get_manifest_text()
        self.assertEqual(
            expected,
            result,
            msg="The URL should fail, but does not")

    def test_manifest_text_with_good_url(self):
        """
        method tested: get_manifest_text
        With a given URL, validate that manifest
        text of the variable HLSManifest.manifest_text
        """
        expected = (200, True)
        result = self.hls.get_manifest_text()
        self.assertEqual(expected, result, msg="Should be (200, True)")
        self.assertNotEqual(
            "",
            self.hls.manifest_text,
            msg="manifest_text should not be empty")

    def test_get_audio_information(self):
        """
        Check if the audio info could be got from Manifest
        """
        self.test_manifest_text_with_good_url()
        self.assertNotEqual(
            self.hls.manifest_text,
            "",
            msg="could not be empty the manifest")
        self.assertTrue(
            self.hls.get_audio_information(),
            msg="Audio was not extracted from Manifest")

    def test_parse_audio_to_json(self):
        """
        Check if the list is parse to Json with audio information
        """
        self.test_get_audio_information()
        if HAS_AUDIO:
            self.assertNotEqual(
                self.hls.audio_info_list,
                [],
                msg="Audio parameters list could not be empty")
            self.assertTrue(
                self.hls.parse_audio_to_json(),
                msg="Audio information could not be parse to JSON")
        else:
            self.assertEqual(
                self.hls.audio_info_list,
                [],
                msg="Audio parameters list could not be empty")
            self.assertFalse(
                self.hls.parse_audio_to_json(),
                msg="Audio information could not be parse to JSON")

    def test_get_video_information(self):
        """
        Check if the video info could be got from Manifest
        """
        self.test_manifest_text_with_good_url()
        self.assertNotEqual(
            self.hls.manifest_text,
            "",
            msg="could not be empty the manifest")
        self.assertTrue(
            self.hls.get_video_information(),
            msg="Video was not extracted from Manifest")

    def test_parse_video_to_json(self):
        """
        Check if the list is parse to Json with video information
        """
        self.test_get_video_information()
        self.assertNotEqual(
            self.hls.video_info_list,
            [],
            msg="Video parameters list could not be empty")
        self.assertTrue(
            self.hls.parse_video_to_json(),
            msg="Video information could not be parse to JSON")

    def test_get_subtitle_information(self):
        """
        Check if the subtitle info could be got from Manifest
        """
        self.test_manifest_text_with_good_url()
        self.assertNotEqual(
            self.hls.manifest_text,
            "",
            msg="could not be empty the manifest")
        self.assertTrue(
            self.hls.get_subtitles_information(),
            msg="Subtitle was not extracted from Manifest")

    def test_parse_subtitles_to_json(self):
        """
        Check if the list is parse to Json with subtitle information
        NOTE: Indicate as Global variable if ASSET URL
        has or not Subtitles
        """
        self.test_get_subtitle_information()
        if not HAS_SUB:
            self.assertEqual(
                self.hls.subtitles_info_list,
                [],
                msg="Subtitle parameters list could not be empty")
            self.assertFalse(
                self.hls.parse_subtitles_to_json(),
                msg="Subtitle information could not be parse to JSON")
        else:
            self.assertNotEqual(
                self.hls.subtitles_info_list,
                [],
                msg="Subtitle parameters list could not be empty")
            self.assertTrue(
                self.hls.parse_subtitles_to_json(),
                msg="Subtitle information could not be parse to JSON")

    def test_build_video_submanifest_url(self):
        """
        Validate that Video submanifest URL could be build
        """
        self.test_parse_video_to_json()
        self.assertTrue(
            self.hls.build_submanifest_url(BASE_URL, 0, "video"),
            msg="Video does not have JSON information")

    def test_build_audio_submanifest_url(self):
        """
        Validate that Audio submanifest URL could be build
        """
        self.test_parse_audio_to_json()
        if HAS_AUDIO:
            self.assertTrue(
                self.hls.build_submanifest_url(BASE_URL, 0, "audio"),
                msg="Audio does not have JSON information")
        else:
            self.assertFalse(
                self.hls.build_submanifest_url(BASE_URL, 0, "audio"),
                msg="Audio does have JSON information")

    def test_build_subtitles_submanifest_url(self):
        """
        Validate that Subtitle submanifest URL could be build
        """
        self.test_parse_subtitles_to_json()
        if HAS_SUB:
            self.assertTrue(
                self.hls.build_submanifest_url(BASE_URL, 0, "subtitles"),
                msg="Subtitle does not have JSON information")
        else:
            self.assertFalse(
                self.hls.build_submanifest_url(BASE_URL, 0, "subtitles"),
                msg="Subtitle does not have JSON information")

    def test_extract_video_files_from_submnifest(self):
        """
        Get all video files from Video submanifest
        """
        self.test_build_video_submanifest_url()
        result = self.hls.extract_files_from_submanifest(
            self.hls.sub_manifest_url["video"]["sub_manifest_0"])
        self.assertTrue(
            result,
            msg="Chunks could not be extracted from submanifest")

    def test_extract_audio_files_from_submnifest(self):
        """
        Get all audio files from Video submanifest
        """
        self.test_build_audio_submanifest_url()
        if HAS_AUDIO:
            result = self.hls.extract_files_from_submanifest(
                self.hls.sub_manifest_url["audio"]["sub_manifest_0"])
            self.assertTrue(
                result,
                msg="Chunks could not be extracted from submanifest")
        else:
            self.assertEqual(
                self.hls.sub_manifest_url["audio"],
                {})

    def test_extract_subtitles_files_from_submnifest(self):
        """
        Get all subtitles files from Video submanifest
        """
        self.test_build_subtitles_submanifest_url()
        if HAS_SUB:
            result = self.hls.extract_files_from_submanifest(
                self.hls.sub_manifest_url["subtitles"]["sub_manifest_0"])
            self.assertTrue(
                result,
                msg="Chunks could not be extracted from submanifest")
        else:
            self.assertEqual(self.hls.sub_manifest_url["subtitles"], {})


if __name__ == '__main__':
    unittest.main()
