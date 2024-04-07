import os, re
from pathlib import Path
from termcolor import colored

def get_pardir():
    cwd = os.path.abspath(os.getcwd())
    end = re.search(r'prife-balance', cwd).end()

    if type(end) == type(None):
        print("Make sure to change directory to prife directory")
        return False
    
    root_dir = cwd[:end]

    return root_dir

def get_user():
    user = os.path.expanduser('~').split('/')[-1]
    return user

def message(type):
    if type=='SUCCESS':
        return f'{colored("DONE", color="green")} ✅'
    return f'{colored("FAILED", color="red")} ❌'

pardir = get_pardir()