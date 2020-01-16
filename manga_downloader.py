import sys
import os
from urllib.request import Request, urlopen

def telecharger_image_manga(url, fichier):
    a = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    b = urlopen(a)
    c = open(fichier, 'wb')
    block_sz = 8192
    while True:
        buffer = b.read(block_sz)
        if not buffer:
            break
        c.write(buffer)

    c.close()


def recuperer_lien_image(html):
    begin = html.index('src="https://i')
    end = html.index('.jpg"', begin+14)
    link = html[begin+5:end+4]
    # fname = link.split('/')[-1]
    # ret = {'link':link, 'fname':fname}
    # return ret
    return link


def lecture_lien(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    reqopen = urlopen(req)
    return str(reqopen.read())

def retoure_nombre_episode(html):
    begin = html.index('</select> of ')
    end = html.index('</div>', begin+13)
    return int(html[begin+13 : end])


def creer_url(nomManga, chapitre):
    chapitre = str(chapitre)
    return "https://www.mangapanda.com/" + nomManga + "/" + chapitre




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
