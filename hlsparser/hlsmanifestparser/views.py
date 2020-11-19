import re
from random import randint
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from hlsmanifestparser.library.hls_manifest import HLSManifest
from hlsmanifestparser.serializers import HLSPManifestParserSerializer


def get_base_url_and_asset_name(url):
    pattern = r'\w*\.m3u8(\?.*)?'
    match = re.search(pattern, url)
    base_url = url.split(match.group())[0]
    return base_url, match.group()


# Create your views here.
@api_view(http_method_names=['POST'])
def hls_manifest_parser(request):
    serializer = HLSPManifestParserSerializer(data=request.data)
    if request.method == 'POST':
        if serializer.is_valid():
            manifest = serializer.data['manifest_url']
            base_url, file_name = get_base_url_and_asset_name(manifest)

            # HLS Object creation
            hls_object = HLSManifest(manifest)
            hls_object.get_manifest_text()
            hls_object.parse_manifest()

            # Video Submaniefst build
            for profiles in range(len(hls_object.video_info_list)):
                hls_object.build_submanifest_url(base_url, profiles)

            # Audio Submaniefst build
            for profiles in range(len(hls_object.audio_info_list)):
                hls_object.build_submanifest_url(base_url, profiles, c_type="audio")

            # Subtitles Submaniefst build
            for profiles in range(len(hls_object.subtitles_info_list)):
                hls_object.build_submanifest_url(base_url, profiles, c_type="subtitles")

            # Extract video from a submanifest_url
            if 'sub_manifest_0' in hls_object.sub_manifest_url["video"].keys():
                hls_object.extract_files_from_submanifest(
                    hls_object.sub_manifest_url["video"]["sub_manifest_0"])
            if 'sub_manifest_0' in hls_object.sub_manifest_url["audio"].keys():
                hls_object.extract_files_from_submanifest(
                    hls_object.sub_manifest_url["audio"]["sub_manifest_0"], c_type="audio")
            if 'sub_manifest_0' in hls_object.sub_manifest_url["subtitles"].keys():
                hls_object.extract_files_from_submanifest(
                    hls_object.sub_manifest_url["subtitles"]["sub_manifest_0"], c_type="subtitles")

            response = {
                    "asset_info": hls_object.asset_json,
                    "asset_chunks": hls_object.asset_files,
                    "sub_manifest": hls_object.sub_manifest_url} 

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'body': 'error'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'ERROR': "Method not allow"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
