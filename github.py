import threading
import urllib.request
import json

class GitHub:

    @staticmethod
    def _request(url, then=None, error=None):
        try:
            response = urllib.request.urlopen(url)
            if (then):
                body = response.read().decode('utf-8')
                then(json.loads(body))
            return response
        except Exception as e:
            if (error):
                error(e)
            else:
                raise e

    @staticmethod
    def _request_thread(url, then, error):
        thread = threading.Thread(target=GitHub._request, args=[url, then, error])
        thread.start()

    @staticmethod
    def _download(url, filepath, then, error):
        try:
            urllib.request.urlretrieve(url, filepath)
            then()
        except Exception as e:
            error(e)

    
    @staticmethod
    def get_releases(then, error):
        url = 'https://api.github.com/repos/open-stage/blender-dmx/releases'
        return GitHub._request_thread(url, then, error)
    
    @staticmethod
    def get_branches(then, error):
        url = 'https://api.github.com/repos/open-stage/blender-dmx/branches'
        return GitHub._request_thread(url, then, error)

    @staticmethod
    def download(url, filepath, then, error):
        thread = threading.Thread(target=GitHub._download, args=[url, filepath, then, error])
        thread.start()
