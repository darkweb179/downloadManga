import sys
import os
from urllib.request import Request, urlopen

def is_exist_chapter(r):
    o = 'notexist'
    try:
        r.index(" is marked as completed. Possibly there will be no new chapter for this manga.")
    except ValueError:
        o = 'exist'

    if r == "b''" and o == 'notexist':
        return False
    else:
        return True
