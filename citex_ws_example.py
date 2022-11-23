import ssl
import certifi
import websocket
import time
import gzip
import zlib
import json
import io
import base64

class test_ws_client:
    def __init__(self, base_url):
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        self.url = base_url
        # ssl.SSLCertVerificationError
        # On Mac OS X, the problem is resolved by clicking on the "Install Certificates.command" file located in the Python directory of the Applications folder.
        # To run the command, open a new Finder window. Click on "Applications". Then click on the directory where Python is installed. For example, "Python 3.8". Finally, kick on the "Install Certificates.command file.
        # All of this can be accomplished by executing the following command in the Terminal application:
        # open "/Applications/Python 3.7/Install Certificates.command"
        # NOTE: You need to be logged into the account that downloaded and installed Python 3.7.
        self.ws = websocket.create_connection(self.url, ssl=ssl_context)

    def recv(self):

        topic1 = '42["subscribe",{"args":[{"topic":"snapshot","params":{"contractId":1,"depth":30}}]}]'#订阅深度
        # topic2 = '42["subscribe",{"args":[{"topic":"tick","params":{"contractId":1}}]}]'#订阅tick
        self.ws.send(topic1)
        while True:
            try:
                compress_data = self.ws.recv()
                if type(compress_data) == bytes:

                    msg = json.loads(zlib.decompress(compress_data[1:], zlib.MAX_WBITS|32))

                    print(msg)
            except Exception as e:
                print(e)


if __name__ == '__main__':

    base_url = "wss://socket.citex.info/socket.io/?EIO=3&transport=websocket"

    test_ws_client(base_url).recv()
