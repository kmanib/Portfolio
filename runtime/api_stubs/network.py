import urllib.request
import socket

class NetworkBridge:
    @staticmethod
    def is_connected():
        try:
            # Simple check
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    @staticmethod
    def simple_get(url):
        try:
            response = urllib.request.urlopen(url)
            return response.read()
        except Exception as e:
            return str(e)
