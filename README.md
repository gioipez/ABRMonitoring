# ABRMonitoring

## Prerequisites
- Install Docker.
- Install Docker Compose.
- Machine where will be deploy needs access to internet.

## Workflow

### HLS manifest parse

```mermaid
sequenceDiagram
User_Machine ->> HLS_Parser: POST request with asset information
HLS_Parser --> HLS_Parser: Build get request to get the Manifest
HLS_Parser ->> CDN/Origin: GET request to get the manifest
CDN/Origin ->> HLS_Parser: GET response with the manifest
HLS_Parser --> HLS_Parser: Parse the information from manifest
HLS_Parser --> HLS_Parser: Build get request to get the sub Manifests URL
HLS_Parser ->> CDN/Origin: GET request to get video submanifest
CDN/Origin ->> HLS_Parser: GET response with video submanifes
HLS_Parser ->> CDN/Origin: GET request to get audio submanifest
CDN/Origin ->> HLS_Parser: GET response with audio submanifest
HLS_Parser ->> CDN/Origin: GET request to get subtitles submanifest
CDN/Origin ->> HLS_Parser: GET response with subtitles submanifest
HLS_Parser ->> User_Machine: POST response with asset information in JSON format
Note right of HLS_Parser: This is phase 1 of the<br> project, the idea <br> is to add more feature.
```


# Sumary

The idea of this repo is create an HLS, DASH and SMOOTH streaming monitoring tool, that mean that could check HTTP status request of the manifest and chunks, analize how available they are in terms of HTTP answer and push a report in Elasticsearch.

In the future there will be a feature where all of this will be in containers, this will rock and will be easy to implement anywhere.

# License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


