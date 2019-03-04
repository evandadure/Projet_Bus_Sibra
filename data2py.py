#!/usr/bin/python3
#-*-coding:utf-8-*-
from datetime import datetime,timedelta


def get_content(data_file_name):
    """
    Fonction qui récupère le texte d'un fichier txt
    Parametres :
        -data_file_name(String) : le chemin du fichier à récupérer
    Retourne :
        content : le contenu du fichier
        (peut aussi afficher un message d'erreur si le fichier n'est pas trouvé)
    """
    try:
        with open(data_file_name, 'r') as f:
            content = f.read()
        return content
    except OSError:
        # 'File not found' error message.
        print("File not found")

def dates2dic(dates):
    """
    Fonction qui retourne les horaires d'un arret sous la forme d'un dictionnaire
    Parametres :
        -dates(List) : une liste d'arrets (chacun étant suivi de ses horaires, séparés par des espaces)
    Retourne :
        dic : un dictionnaire dons les clés sont les arrets, et les valeurs de chaque clé sont des listes d'horaires
    """
    dic = {}
    splitted_dates = dates.split("\n")
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic

def line_infos(content):
    """
    Fonction qui retourne un dictionnaire contenant les différentes informations extraites d'un fichier de ligne de bus
    Parametres :
        -content : le contenu du fichier d'une ligne de bus
    Retourne :
        infos_dic : un dictionnaire contenant les différentes informations de la ligne de bus (horaires "aller" et "retour" en semaine et en weekend/vacances,
        ainsi que la liste des arrets qui composent cette ligne)
    """
    slited_content = content.split("\n\n")
    infos_dic={}
    infos_dic["regular_path"] = slited_content[0]
    infos_dic["regular_date_go"] = dates2dic(slited_content[1])
    infos_dic["regular_date_back"] = dates2dic(slited_content[2])
    infos_dic["we_holidays_path"] = slited_content[3]
    infos_dic["we_holidays_date_go"] = dates2dic(slited_content[4])
    infos_dic["we_holidays_date_back"] = dates2dic(slited_content[5])
    return infos_dic

def setDateTime(date,heure):
    """
    Fonction qui crée un datetime à partir d'une string de date (exemple "21/08/18"), et d'une string d'heure (exemple "13:37")
    Parametres :
        - date : String de la date
        - heure : String de l'heure
    Retourne :
        d : la date (et son heure) dans le type datetime
    """
    d = datetime.strptime(date,"%d/%m/%y")
    h = heure[:heure.find(":")]
    m = heure[heure.find(":")+1:]
    d = d.replace(hour=int(h),minute=int(m))
    return d

def getTimeDelta(heure1,heure2):
    """
    Fonction qui retourne la différence, en minutes, entre deux heures données
    Parametres :
        - heure1 : String contenant une heure
        - heure2 : String contenant une heure
    Retourne :
        - Int des minutes entre les deux heures (pouvant être négatif si l'heure1 est inférieure à l'heure2)
    """
    delta = setDateTime("01/01/70",heure1)-setDateTime("01/01/70",heure2)
    return int(delta.total_seconds()/60)

def getHeure(date):
    """
    Fonction qui retourne l'heure (sous le type String) d'un datetime
    Parametres :
        - date : datetime
    Retourne :
        - heure (exemple "13:37") extraite depuis le datetime
    """
    return str(date.time())[0:5]

def addMinuteToTime(time,minutes):
    """
    [ANCIENNEMENT UTILISEE]
    Fonction qui retourne une heure après lui avoir ajouté un certain nombre de minutes
    Parametres :
        - time (string): heure (ex : "13:37")
        - minutes (int): minutes à ajouter
    Retourne :
        - string : nouvelle heure après avoir ajouté les minutes
    """
    date = setDateTime("01/01/70",time)
    date+=timedelta(minutes=minutes)
    return getHeure(date)
    
def isSemaine(date):
    """
    Fonction qui repère si une date définie est un samedi ou pas
    Parametres :
        - date (datetime) : une date
    Retourne :
        - string : "V" si c'est un samedi (V pour "vacances"), "S" si ce n'est pas un samedi (S pour "semaine")
    """
    if(date.isoweekday() == 6):
        return "V"
    else:
        return "S"




    


