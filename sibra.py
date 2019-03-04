# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:03:33 2019

@author: evand
"""
import math
import data2py
from plan import Plan


def shortest_way(plan, arretDepart, arretArrivee):
    """
    Fonction d'affichage pour le chemin le plus court en nombre de connexions, entre deux arrets
    Parametres :
        - plan (Plan) : le plan contenant les arrets et les connexions
        - arretDepart (String) : le nom de l'arret de départ
        - arretArrivee (String) : le nom de l'arret d'arrivee
    Retourne :
        Aucun retour
    """

    #Récupère l'arret de départ et l'arret d'arrivée d'après leur nom
    arr1 = plan.is_in_arrets(arretDepart)
    arr2 = plan.is_in_arrets(arretArrivee)
    #Récupère le chemin le plus court entre les deux arrets, d'après l'algorithme de Djikstra, sous forme d'une liste d'arrets (dans l'ordre de passage)
    shortestWay = plan.djikstra(arr1,arr2,"shortest")
    #Initialisation de certaines données
    trajets_par_ligne = {}
    currentLine = "0"
    trajet_ligne=[]
    #Création de dictionnaires pour chaque ligne composant le chemin (lé clé étant le numéro de la ligne, la valeur
    #étant une liste des arrets qui sont dans cette ligne. A chaque changement, une nouvelle clé est créée dans le dic)
    for i,arret in enumerate(shortestWay):
        #si l'arret traité n'est pas l'arret d'arrivée
        if arret != arr2:
            #Récupération de la connexion entre un arret et l'arret qui le suit, pour connaitre la ligne qui les lie
            connexion = plan.get_connexion(arret, shortestWay[i+1])
            #création d'une clé dans le dictionnaire à chaque changement de ligne dans le chemin
            if currentLine != connexion.get_ligne():
                if currentLine != "0":
                    oldConnexion = plan.get_connexion(shortestWay[i-1], arret)
                    trajet_ligne.append(arret)
                    trajets_par_ligne[currentLine] = [trajet_ligne,oldConnexion.get_rightDirection(shortestWay[i-1],arret)]
                currentLine = connexion.get_ligne()
                trajet_ligne=[]
            trajet_ligne.append(arret)
        #si l'arret traité est l'arret d'arrivée, on ajoute la dernière clé dans le dictionnaire (= la dernière ligne de bus trouvée)
        else:
            connexion = plan.get_connexion(shortestWay[i-1],arret)
            trajet_ligne.append(arret)
            trajets_par_ligne[currentLine] = [trajet_ligne,connexion.get_rightDirection(shortestWay[i-1],arret)]
            currentLine = connexion.get_ligne()

    #Affichage des différents arrets composant le chemin, et des éventuels changements présents.
    for numeroLigne, listeArrets in trajets_par_ligne.items():
        print("Monter dans le bus",numeroLigne,"à l'arrêt",listeArrets[0][0].get_nom(),"en direction de",listeArrets[1])
        # Si un ou plusieurs arrets sont présents entre le premier arret de la ligne et le dernier, alors on le(s) liste
        if (len(listeArrets[0]) - 2 > 0):
            print(len(listeArrets[0])-2,"arrêts :")
        for i,arret in enumerate(listeArrets[0]):
            if 0 < i < len(listeArrets[0])-1:
                print("|",arret.get_nom())
        print("Descendre à l'arrêt",listeArrets[0][-1].get_nom())
    print("Nombre total d'arrets :",len(shortestWay))
        
def fastest_way(plan, arretDepart, arretArrivee, wayType, dateDepart):
    """
    Fonction d'affichage pour les chemins "fastest" et "foremost"
        -Fastest : passe le moins de temps possible dans les bus (trajet le plus court)
        -Foremost : arrive au plus tot à destination
    Parametres :
        - plan (Plan) : le plan contenant les arrets et les connexions
        - arretDepart (String) : le nom de l'arret de départ
        - arretArrivee (String) : le nom de l'arret d'arrivee
        - wayType(String) : le type de chemin ("fastest" ou "foremost")
        - dateDepart([String,String]) : liste contenant le jour de départ sous forme d'une string (ex "12/01/2019") et l'heure
            sous forme de string également (ex "12:03")
    Retourne :
        Peut retourner None lorsqu'aucun chemin n'a été trouvé entre les deux arrets à l'heure demandée, mais sinon
        ne retourne rien.
    """
    #Récupère l'arret de départ et l'arret d'arrivée d'après leur nom
    arr1 = plan.is_in_arrets(arretDepart)
    arr2 = plan.is_in_arrets(arretArrivee)
    tempsDebut = dateDepart[1]
    #Récupère le chemin le plus court entre les deux arrets, d'après l'algorithme de Djikstra, sous forme d'une liste d'arrets (dans l'ordre de passage)
    fastestWay = plan.djikstra(arr1, arr2, wayType,dateDepart)

    #Dans le cas où aucun trajet n'a été trouvé entre les deux arrets à l'heure en paramètre, on affiche un message d'erreur :
    if fastestWay is None:
        print("Aucun bus ne permet de se rendre de", arretDepart, "à", arretArrivee," à cette date.")
        return None

    #Setting des temps de trajets total, dans le bus, l'heure de fin
    tempsFin = fastestWay[-1].get_heurePassage()[0]
    tempsTotal = data2py.getTimeDelta(tempsFin,tempsDebut)
    tempsBus = arr2.get_shortestWayToSelf()[0]
    print("TEMPS TOTAL :",tempsTotal,"MINUTES")
    if wayType == "fastest":
        print("TEMPS DANS LES BUS :",tempsBus,"MINUTES")
        print("TEMPS D'ATTENTE TOTAL :",tempsTotal-tempsBus,"MINUTES")
    trajets_par_ligne = {}
    currentLine = "0"
    trajet_ligne = []
    for i, arret in enumerate(fastestWay):
        # si l'arret traité n'est pas l'arret d'arrivée
        if arret != arr2:
            # Récupération de la connexion entre un arret et l'arret qui le suit, pour connaitre la ligne qui les lie
            connexion = plan.get_connexion(arret, fastestWay[i + 1])
            # création d'une clé dans le dictionnaire à chaque changement de ligne dans le chemin
            if currentLine != connexion.get_ligne():
                if currentLine != "0":
                    oldConnexion = plan.get_connexion(fastestWay[i - 1], arret)
                    trajet_ligne.append(arret)
                    trajets_par_ligne[currentLine] = [trajet_ligne,
                                                      oldConnexion.get_rightDirection(fastestWay[i - 1], arret)]
                currentLine = connexion.get_ligne()
                trajet_ligne = []
            trajet_ligne.append(arret)
        # si l'arret traité est l'arret d'arrivée
        else:
            connexion = plan.get_connexion(fastestWay[i - 1], arret)
            trajet_ligne.append(arret)
            trajets_par_ligne[currentLine] = [trajet_ligne, connexion.get_rightDirection(fastestWay[i - 1], arret)]
            currentLine = connexion.get_ligne()
    # Affichage des différents arrets composant le chemin, avec des détails sur les heures de passages, les changements,
    # ainsi que les temps d'attente éventuels.
    # La boucle for permet de parcourir chaque clé du dictionnaire, correspondant aux arrets d'une ligne
    for numeroLigne, listeArrets in trajets_par_ligne.items():
        heureArrivee = listeArrets[0][0].get_heurePassage()[0]
        heureDepart = listeArrets[0][0].get_heurePassage()[1][listeArrets[0][1].get_nom()]
        #Temps d'attente initial au premier arret de la ligne
        if heureArrivee != heureDepart:
            tempsAttente = data2py.getTimeDelta(heureDepart, heureArrivee)
            print("- Attendre", tempsAttente, "minutes à l'arrêt", listeArrets[0][0].get_nom())
        print("- Monter dans le bus", numeroLigne, "à l'arrêt", listeArrets[0][0].get_nom(), "en direction de",
              listeArrets[1], \
              "à", listeArrets[0][0].get_heurePassage()[1][listeArrets[0][1].get_nom()])
        # Si un ou plusieurs arrets sont présents entre le premier arret de la ligne et le dernier, alors on le(s) liste
        if (len(listeArrets[0]) - 2 > 0):
            print("- Rester dans le bus pendant les arrêts suivants :")
        for i, arret in enumerate(listeArrets[0]):
            if 0 < i < len(listeArrets[0]) - 1:
                heureArrivee = arret.get_heurePassage()[0]
                heureDepart = arret.get_heurePassage()[1][listeArrets[0][i + 1].get_nom()]
                #Affichage de texte dans le cas où l'on attend à un arret pour prendre le même bus mais plus tard, afin d'atteindre
                #des arrets qui sont "rarement accessibles". L'exemple de LYCEE-DE-POISY est assez parlant.
                if heureArrivee != heureDepart:
                    print("- Descendre à l'arrêt", listeArrets[0][i].get_nom(), "à",
                          listeArrets[0][i].get_heurePassage()[0])
                    tempsAttente = data2py.getTimeDelta(heureDepart,heureArrivee)
                    print("- Attendre",tempsAttente,"minutes à l'arrêt", listeArrets[0][i].get_nom())
                    print("- Monter dans le bus", numeroLigne, "à l'arrêt", listeArrets[0][i].get_nom(),
                          "en direction de", listeArrets[1], "à", listeArrets[0][i].get_heurePassage()[1]
                          [listeArrets[0][i+1].get_nom()])
                #Affichage simple des arrets parcourus par une ligne si aucune attente n'est nécessaire
                else:
                    print("|", arret.get_nom(), "(", heureArrivee, ")")
        print("- Descendre à l'arrêt", listeArrets[0][-1].get_nom(), "à", listeArrets[0][-1].get_heurePassage()[0])
    
                
            
            

#------------------------------- ZONE DE TEST ------------------------------------

#Création du plan et remplissage de ce dernier avec les différentes lignes à disposition
planTest = Plan()
planTest.build_connexions("data/2_Piscine-Patinoire_Campus.txt","2")
planTest.build_connexions("data/1_Poisy-ParcDesGlaisins.txt","1")

#Exemples d'utilisation de shortest_way et fastest_way
#shortest_way(planTest,"Chorus","CAMPUS")
#fastest_way(planTest,"GARE","LYCEE-DE-POISY","fastest",["22/03/19","6:00"])


#Bon exemple de compréhension entre la différence entre fastest et foremost
fastest_way(planTest,"CAMPUS","GARE","foremost",["04/03/19","16:24"])
fastest_way(planTest,"GARE","VIGNIERES","foremost",["23/03/19","9:26"])
