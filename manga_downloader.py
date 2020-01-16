import sys
import os
from urllib.request import Request, urlopen


def syntax_chapitre_valide(chapitres):
    for chapitre in chapitres:
        if chapitre.isnumeric() == False:
            return False
    return True



def creer_liste_chapitre(chapitre_param):

    if '-' in chapitre_param:
        list_chapitre = chapitre_param.split('-', maxsplit=1)
        if is_valid_chapter_syntax(list_chapitre):
            return range(int(list_chapitre[0]),int(list_chapitre[1]))
        else:
            print("Use a valid syntax for chapter list")
            sys.exit()
    elif ',' in chapitre_param:
        list_chapitre = chapitre_param.split(',')
        if is_valid_chapter_syntax(list_chapitre):
            return list_chapitre
        else:
            print("Use a valid syntax for chapter list")
            sys.exit()
    else:
        if is_valid_chapter_syntax(chapitre_param):
            return [chapitre_param]
        else:
            print("Use a valid syntax for chapter list")
            sys.exit()



def check_chapitre_exist(chapitre_url):
    o = 'notexist'
    try:
        chapitre_url.index(" is marked as completed. Possibly there will be no new chapter for this manga.")
    except ValueError:
        o = 'exist'

    if chapitre_url == "b''" and o == 'notexist':
        return False
    else:
        return True
