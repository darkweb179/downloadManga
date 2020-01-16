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
        if syntax_chapitre_valide(chapitre_param):
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


try:
    manga_name = sys.argv[1]
    chapter = sys.argv[2]
except IndexError :
    print("Missing manga name or/and manga chapter")
    sys.exit()
       
mainFolder = False
chapterList = creer_liste_chapitre(chapter)

for chap in chapterList:
    print(manga_name.upper())
    url = creer_url(manga_name, chap)
    urlContent = lecture_lien(url)

    if check_chapitre_exist(urlContent):
        pageNum = retoure_nombre_episode(urlContent)
        print("Chapter - {}".format(chap))
        chapterFolder = 'chapitre'+chap
        if mainFolder == False:
            try:
                os.mkdir("./"+manga_name)
            except FileExistsError:
                pass
            finally:
                mainFolder = True

        try:
            os.mkdir("./"+manga_name+"/"+chapterFolder)
        except FileExistsError:
            pass

        urlimage = recuperer_lien_image(urlContent)
        fileName = "./"+manga_name+"/"+chapterFolder+"/" + manga_name + "-" + chap + '-1.jpg'
        print(fileName)
        telecharger_image_manga(urlimage, fileName)
        
        for k in range(2, pageNum + 1):
            urlname = url + "/" + str(k)
            urlContent = lecture_lien(urlname)
            urlimage = recuperer_lien_image(urlContent)
            fileName = "./"+manga_name+"/"+chapterFolder+"/"+ manga_name + "-" + chap + "-" + str(k) + ".jpg"
            print(fileName)
            telecharger_image_manga(urlimage, fileName)
    else:
        print("Chapter {} does not exist".format(chap)) 