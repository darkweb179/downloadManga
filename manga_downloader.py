import sys
import os
from urllib.request import Request, urlopen


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


try:
    manga_name = sys.argv[1]
    chapter = sys.argv[2]
except IndexError :
    print("Missing manga name or/and manga chapter")
    sys.exit()
       
mainFolder = False
chapterList = create_chapter_list(chapter)

for chap in chapterList:
    print(manga_name.upper())
    url = create_url(manga_name, chap)
    urlContent = read_url(url)

    if is_exist_chapter(urlContent):
        pageNum = get_nbof_page_manga(urlContent)
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

        urlimage = get_info_of_page_manga(urlContent)
        fileName = "./"+manga_name+"/"+chapterFolder+"/" + manga_name + "-" + chap + '-1.jpg'
        print(fileName)
        download_page_manga(urlimage, fileName)
        
        for k in range(2, pageNum + 1):
            urlname = url + "/" + str(k)
            urlContent = read_url(urlname)
            urlimage = get_info_of_page_manga(urlContent)
            fileName = "./"+manga_name+"/"+chapterFolder+"/"+ manga_name + "-" + chap + "-" + str(k) + ".jpg"
            print(fileName)
            download_page_manga(urlimage, fileName)
    else:
        print("Chapter {} does not exist".format(chap))