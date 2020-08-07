# ABRMonitoring

## Prerequisites
- Install Docker.
- Install Docker Compose.
- Machine where will be deploy needs access to internet.

## Workflow

### HLS manifest parse


```
sequenceDiagram
	participant User_Machine
	participant HLS_Parser
	participant CDN/Origin
	User_Machine->>HLS_Parser:POSTrequestwithassetinformation
	HLS_Parser-->HLS_Parser:BuildgetrequesttogettheManifest
	HLS_Parser->>CDN/Origin:GETrequesttogetthemanifest
	CDN/Origin->>HLS_Parser:GETresponsewiththemanifest
	HLS_Parser-->HLS_Parser:Parsetheinformationfrommanifest
	HLS_Parser-->HLS_Parser:BuildgetrequesttogetthesubManifestsURL
	HLS_Parser->>CDN/Origin:GETrequesttogetvideosubmanifest
	CDN/Origin->>HLS_Parser:GETresponsewithvideosubmanifes
	HLS_Parser->>CDN/Origin:GETrequesttogetaudiosubmanifest
	CDN/Origin->>HLS_Parser:GETresponsewithaudiosubmanifest
	HLS_Parser->>CDN/Origin:GETrequesttogetsubtitlessubmanifest
	CDN/Origin->>HLS_Parser:GETresponsewithsubtitlessubmanifest
	HLS_Parser->>User_Machine:POSTresponsewithassetinformationinJSONformat
	Note right of HLS_Parser: This is phase 1 of the<br> project, the idea <br> is to add more feature.
```


# Sumary

The idea of this repo is create an HLS, DASH and SMOOTH streaming monitoring tool, that mean that could check HTTP status request of the manifest and chunks, analize how available they are in terms of HTTP answer and push a report in Elasticsearch.

In the future there will be a feature where all of this will be in containers, this will rock and will be easy to implement anywhere.

# License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


