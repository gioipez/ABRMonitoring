# ABRMonitoring
There are a tons of HLS, Smooth streaming and DASH library to parse the information from manifest to JSON data out there, the idea of this is give the engineer a tool to validate an HTTP Stream asset configuration, check the information that manifest is returning, all the submanifest, audio/video/subtitles chunks, codecs, etc. all of these in a microservice contenirized app responding with REST API.

Then as you have all of that information, in a phase 2 of the project, the idea is to have another microservice that could use that information of the exposed server and use as input for monitoring

## Workflow

### HLS manifest parse

![ABRManifestDiagram](pictures/ABRManifest.svg)

Diagram designed with: [Sequence Diagram](https://sequencediagram.org/)

# Getting started 
The instructions to install the app in docker are comming here.

## Prerequisites
- Install Docker.
- Install Docker Compose.
- Internet access or CDN/Origin access.

## Instalation

1. Download the repository from this url [ABR Monitoring](https://github.com/GioLopez/ABRMonitoring/)
2. In the same folder as `docker-compose.yml` file, execute the following command:
```sh
docker-compose up -d --build
```

## Usage
The solution was build with an software architecture patern Microservice Deployment, Containerization, Microservice Isolation Levels, that let you use the microservices isolated, in this phase 1 only HLS manifest parser is available and is use as follow:

- HTTP Method: POST
- HTTP Headers: Content-Type:application/json
- URL: in my case: [http://localhost:8000/hlsmanifest/](http://localhost:8000/hlsmanifest/) but that depends where you deployed it
- Body: {"asset_name":"name_of_the_asset.m3u8", "base_url":"http://cdn_fqn:port/path/"}

```sh
curl -XPOST -H'Content-type:application/json' 'http://localhost:8000/hlsmanifest/' -d '{"asset_name": "playlist.m3u8","base_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/"}'
```

to print pretty formated, add ` | python -m json.tool` at the end of your request, like this:

```sh
curl -XPOST -H'Content-type:application/json' 'http://localhost:8000/hlsmanifest/' -d '{"asset_name": "playlist.m3u8","base_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/"}' | python -m json.tool
```

That's all, you have all the information parser from your HLS asset

# Sumary

The idea of this repo is create an HLS, DASH and SMOOTH streaming monitoring tool, that mean that could check HTTP status request of the manifest and chunks, analize how available they are in terms of HTTP answer and push a report in Elasticsearch.

In the future there will be a feature where all of this will be in containers, this will rock and will be easy to implement anywhere.

# License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


