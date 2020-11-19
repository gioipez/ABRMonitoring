"""
Maintainer: Giovanni Lopez
Mail: giovannt_92@hotmail.com / gioipez92@gmail.com
Maintain an standar libraries for HTTP communication with
try, timeouts and headers
"""
import yaml
import requests
from requests.auth import HTTPBasicAuth


def load_streamnames_from_file(path):
    '''
    Load YAML files to python
    '''
    return yaml.load(open(path), Loader=yaml.FullLoader)

def put_request(url, **kwargs):
    '''
    Generic PUT method with basic auth
    Input:
    - url
    - kwargs:
            - user
            - password
            - body
            - headers
            - timeout
    '''
    if "timeout" not in kwargs.keys():
        kwargs["timeout"] = 60.0
    if "headers" not in kwargs.keys():
        kwargs["headers"] = {'content-type': 'application/json'}
    try:
        if "user" in kwargs.keys():
            response = requests.put(
                url,
                timeout=kwargs["timeout"],
                auth=HTTPBasicAuth(
                    kwargs["user"],
                    kwargs["password"]
                ),
                json=kwargs["body"],
                headers=kwargs["headers"])
        else:
            response = requests.put(
                url,
                timeout=kwargs["timeout"],
                json=kwargs["body"],
                headers=kwargs["headers"])
    except Exception as http_error:
        print(f"Request error: {http_error}")
        return None
    else:
        return response

def post_request(url, **kwargs):
    '''
    Generic POST method with basic auth
    Input:
    - url
    - kwargs:
            - user
            - password
            - body
            - headers
            - timeout
    '''
    if "timeout" not in kwargs:
        kwargs["timeout"] = 60.0
    if "headers" not in kwargs:
        kwargs["headers"] = {'content-type': 'application/json'}
    try:
        if "user" in kwargs.keys():
            response = requests.post(
                url,
                timeout=kwargs["timeout"],
                auth=HTTPBasicAuth(
                    kwargs["user"],
                    kwargs["password"]),
                json=kwargs["body"],
                headers=kwargs["headers"])
        else:
            response = requests.post(
                url,
                timeout=kwargs["timeout"],
                json=kwargs["body"],
                headers=kwargs["headers"])
    except Exception as http_error:
        print(f"Request error: {http_error}")
        return None
    else:
        return response

def get_request(url, **kwargs):
    '''
    Input:
    - url
    - kwargs:
            - user
            - password
            - body
            - headers
            - timeout
    '''
    if "timeout" not in kwargs.keys():
        kwargs["timeout"] = 60.0
    if "headers" not in kwargs.keys():
        kwargs["headers"] = {"Content-Type": "application/json"}
    try:
        if "user" in kwargs.keys():
            response = requests.get(
                url,
                headers=kwargs["headers"],
                timeout=kwargs["timeout"],
                auth=HTTPBasicAuth(
                    kwargs["user"],
                    kwargs["password"]),
            )
        else:
            response = requests.get(
                url,
                headers=kwargs["headers"],
                timeout=kwargs["timeout"],
            )
    except Exception as http_error:
        #print(f"Request error: {http_error}")
        return None
    else:
        return response

def head_request(url, **kwargs):
    '''
    Input:
    - url
    - kwargs:
            - user
            - password
            - body
            - headers
            - timeout
    '''
    if "timeout" not in kwargs.keys():
        kwargs["timeout"] = 60.0
    if "headers" not in kwargs.keys():
        kwargs["headers"] = {"Content-Type": "application/json"}
    try:
        if "user" in kwargs.keys():
            response = requests.head(
                url,
                headers=kwargs["headers"],
                timeout=kwargs["timeout"],
                auth=HTTPBasicAuth(
                    kwargs["user"],
                    kwargs["password"]),
            )
        else:
            response = requests.head(
                url,
                headers=kwargs["headers"],
                timeout=kwargs["timeout"],
            )
    except Exception as http_error:
        #print(f"Request error: {http_error}")
        return None
    else:
        return response
