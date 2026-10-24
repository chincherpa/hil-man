import getpass
import socket
import time

def wait_and_get_username(seconds=10):
    time.sleep(seconds)
    return f'{getpass.getuser()} - {socket.gethostname()}', ''

if __name__ == "__main__":
    username, _ = wait_and_get_username(1)
    print(username)
