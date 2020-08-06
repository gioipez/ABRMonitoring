"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Module for test the HLSManifest class
"""
import unittest
from hls_manifest import HLSManifest


class TestHLSManifest(unittest.TestCase):
    """
    This will test HLSManifest class
    """

    def setUp(self):
        tmp = "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
        self.hls = HLSManifest(tmp)

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

    def test_manifest_text_with_failing_url(self):
        """
        method tested: get_manifest_text
        This is what will be done when the URL is wrong, that mean
        HTTP_404_NOT_FOUND
        """
        expected = (None, False)
        self.hls.asset_url = "http://184.72.239.149/vod/smil:BigBuckBunny.smil/playlist.m3u8"
        result = self.hls.get_manifest_text()
        self.assertEqual(
            expected,
            result,
            msg="The URL should fail, but does not")

if __name__ == '__main__':
    unittest.main()
