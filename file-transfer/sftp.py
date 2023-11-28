import pysftp
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class fileTransfer:
    def __init__(self, host='', username='', private_key='', private_key_pass='', ignore_host_key=False):
        self.host = os.getenv('HOST', host)
        self.username = os.getenv('USERNAME', username)
        self.private_key = os.getenv('PRIVATE_KEY', private_key)
        self.private_key_pass = os.getenv('PRIVATE_KEY_PASS', private_key_pass)
        self.port = 22
        self.serverconn = self.connect(ignore_host_key)

    def connect(self, ignore_host_key):
        """Connects to the sftp server and returns the sftp connection object"""
        try:
            cnopts = None

            if ignore_host_key:
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys = None

            # Get the sftp connection object
            serverconn = pysftp.Connection(
                host=os.getenv('HOST'),
                username=os.getenv('USERNAME'),
                private_key=os.getenv('PRIVATE_KEY'),
                private_key_pass=os.getenv('PRIVATE_KEY_PASS'),
                port=self.port,
                cnopts=cnopts
            )
            if serverconn:
                print("Connected to host...")
        except Exception as err:
            print(err)
            raise Exception(err)

        finally:
            return serverconn

    def transfer(self, src, target):
        """Recursively places files in the target dir, copies everything inside of src dir"""
        try:
            print(f"Transferring files to {self.host} ...")
            self.serverconn.put_r(str(src), str(target))
            print("Files Successfully Transferred!")
            print(
                f"Src files placed in Dir: {self.serverconn.listdir(target)}")

        except Exception as err:
            raise Exception(err)

def main():
    svrcon = fileTransfer()
    src = sys.argv[1]
    target = sys.argv[2]
    svrcon.transfer(str(src), (target))

if __name__ == '__main__':
    main()
