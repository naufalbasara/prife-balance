import os

from pathlib import Path

def get_pardir():
    return Path(os.getcwd()).parent.absolute()

def get_user():
    user = os.path.expanduser('~').split('/')[-1]
    return user