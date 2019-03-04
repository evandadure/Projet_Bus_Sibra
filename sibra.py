# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:03:33 2019

@author: evand
"""
import math
import data2py
from plan import Plan


def shortest_way(plan, arretDepart, arretArrivee):
    arr1 = planTest.is_in_arrets(arretDepart)
    arr2 = planTest.is_in_arrets(arretArrivee)
    shortestWay = planTest.djikstra(arr1,arr2,"shortest")
    trajets_par_ligne = {}
    currentLine = "0"
    trajet_ligne=[]
    for i,arret in enumerate(shortestWay):
        #si l'arret traité n'est pas l'arret d'arrivée
        if arret != arr2:
            connexion = plan.get_connexion(arret, shortestWay[i+1])
            if currentLine != connexion.get_ligne():
                if currentLine != "0":
                    oldConnexion = plan.get_connexion(shortestWay[i-1], arret)
                    trajet_ligne.append(arret)
                    trajets_par_ligne[currentLine] = [trajet_ligne,oldConnexion.get_rightDirection(shortestWay[i-1],arret)]
                currentLine = connexion.get_ligne()
                trajet_ligne=[]
            trajet_ligne.append(arret)
        #si l'arret traité est l'arret d'arrivée
        else:
            connexion = plan.get_connexion(shortestWay[i-1],arret)
            trajet_ligne.append(arret)
            trajets_par_ligne[currentLine] = [trajet_ligne,connexion.get_rightDirection(shortestWay[i-1],arret)]
            currentLine = connexion.get_ligne()
                 
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
        
def fastest_way(plan, arretDepart, arretArrivee, wayType, dateDepart=None,):
    arr1 = planTest.is_in_arrets(arretDepart)
    arr2 = planTest.is_in_arrets(arretArrivee)
    tempsDebut = dateDepart[1]
    fastestWay = planTest.djikstra(arr1, arr2, wayType,dateDepart)

    #Dans le cas où aucun trajet n'a été trouvé entre les deux arrets à l'heure en paramètre, on affiche un message d'erreur :
    if fastestWay is None:
        print("Aucun bus ne permet de se rendre de", arretDepart, "à", arretArrivee," à cette date.")
        return None


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
            connexion = plan.get_connexion(arret, fastestWay[i + 1])
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

    for numeroLigne, listeArrets in trajets_par_ligne.items():
        heureArrivee = listeArrets[0][0].get_heurePassage()[0]
        heureDepart = listeArrets[0][0].get_heurePassage()[1][listeArrets[0][1].get_nom()]
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
                if heureArrivee != heureDepart:
                    print("- Descendre à l'arrêt", listeArrets[0][i].get_nom(), "à",
                          listeArrets[0][i].get_heurePassage()[0])
                    tempsAttente = data2py.getTimeDelta(heureDepart,heureArrivee)
                    print("- Attendre",tempsAttente,"minutes à l'arrêt", listeArrets[0][i].get_nom())
                    print("- Monter dans le bus", numeroLigne, "à l'arrêt", listeArrets[0][i].get_nom(),
                          "en direction de", listeArrets[1], "à", listeArrets[0][i].get_heurePassage()[1]
                          [listeArrets[0][i+1].get_nom()])
                else:

                    print("|", arret.get_nom(), "(", heureArrivee, ")")
        print("- Descendre à l'arrêt", listeArrets[0][-1].get_nom(), "à", listeArrets[0][-1].get_heurePassage()[0])
    
                
            
            
            
            
    
    



         
        
        
planTest = Plan()
planTest.build_connexions("data/2_Piscine-Patinoire_Campus.txt","2")
planTest.build_connexions("data/1_Poisy-ParcDesGlaisins.txt","1")


#shortest_way(planTest,"Arcadium","Ponchy")

shortest_way(planTest,"GARE","LYCEE-DE-POISY")
#fastest_way(planTest,"GARE","LYCEE-DE-POISY","fastest",["22/03/19","6:00"])
fastest_way(planTest,"GARE","LYCEE-DE-POISY","fastest",["23/03/19","6:58"])


# arr1 = planTest.is_in_arrets("CAMPUS")
# arr2 = planTest.is_in_arrets("France-Barattes")
# for arret in planTest.djikstra(arr1,arr2,"fastest",["22/03/19","14:20"]):
#     print(arret.get_nom(),arret.get_heurePassage())

#EXEMPLE QUI DIFFERENCIE FOREMOST ET FORECAST : fastest_way(planTest,"GARE","VIGNIERES","fastest",["23/03/19","9:26"])


#
