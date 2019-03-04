# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 16:26:33 2019

@author: evand
"""

from arret import Arret
from horaire import Horaire
from connexion import Connexion
import data2py
import math
import datetime as dt

class Plan:
    """
    Un plan est un graphe composé d'arrets et de connexions entre eux, ainsi que de différents méthodes de calculs et de l'algorithme de Djikstra.
    """

    def __init__(self):
        #Liste de toutes les connexions du plan
        self.connexions = []
        #Liste de tous les arrets du plan
        self.arrets = []

    # --------- GETTERS --------------
    def get_connexions(self):
        return self.connexions
        
    def get_arrets(self):
        return self.arrets
    
    def add_connexion(self,connexion):
        """
        Méthode qui ajoute une connexion à la liste des connexions du plan
        Parametres :
            -connexion(Connexion) : une connexion à ajouter
        Retourne :
            Aucun retour
        """
        self.connexions.append(connexion)
    
    def add_arret(self,arret):
        """
        Méthode qui ajoute un arret à la liste des arrets du plan
        Parametres :
            -arret(Arret) : un arret à ajouter
        Retourne :
            Aucun retour
        """
        self.arrets.append(arret)
        
    def is_in_arrets(self,nomArret):
        """
        Méthode qui renvoie un arret d'après son nom passé en paramètre, sinon renvoie False
        Parametres :
            -nomArret(String) : le nom de l'arret
        Retourne :
            - Arret : l'arret dont le nom est passé en paramètre
            - False : si aucun arret dont le nom est passé en paramètre n'a été trouvé
        """
        for arret in self.arrets:
            if arret.get_nom() == nomArret:
                return arret
        return False
    
    def get_connexion(self, arret1, arret2):
        """
        Méthode qui renvoie la connexion qui lie deux arrets
        Parametres :
            -arret1(Arret) : un premier arret
            -arret2(Arret) : un deuxieme arret
        Retourne :
            - Connexion : la connexion qui lie les deux arrets
        """
        for connexion in self.connexions:
            #Comme on ne connait pas l'ordre dans lequel sont présents les deux arrets dans la connexion, on teste les "deux ordres" possibles (arret1-arret2 et arret2-arret1)
            if connexion.get_arrets()[0] == arret1:
                if connexion.get_arrets()[1] == arret2:
                    return connexion
            if connexion.get_arrets()[0] == arret2:
                if connexion.get_arrets()[1] == arret1:
                    return connexion
    
    def get_arrets_voisins(self,arret):
        """
        Méthode qui renvoie les arrets voisins d'un arret passé en paramètre. Pour cela, on parcourt toutes les connexions
        de notre plan et on cherche celles qui contiennent l'arret en paramètre
        Parametres :
            -arret(Arret) : un arret
        Retourne :
            - voisins(liste d'Arrets) : les arrets voisins à l'arret passé en paramètre
        """
        voisins=[]
        for connexion in self.connexions:
            if connexion.get_arrets()[0] == arret:
                voisins.append(connexion.get_arrets()[1])
            if connexion.get_arrets()[1] == arret:
                voisins.append(connexion.get_arrets()[0])
        return voisins
                
                
        
    def build_connexions(self,file_path,line):
        """
        Méthode qui crée tous les arrêts et toutes les connexions présentes dans un fichier de ligne de bus, en utilisant
        les différentes fonctions de traitements de data2py.py et les méthodes des classes Plan, Arret, Horaire et Connexion.
        Parametres :
            -file_path(String) : le chemin vers le fichier de la ligne
            -line(string) : la ligne de bus dont on veut ajouter les connexions et les arrets
        Retourne :
            - voisins(liste d'Arrets) : les arrets voisins à l'arret passé en paramètre
        """
        #Récupération de toutes les informations sur les différents horaires
        lineInfos = data2py.line_infos(data2py.get_content(file_path))
        listeNomsArrets = lineInfos["regular_path"].split(' N ')
        direction_aller = listeNomsArrets[-1]
        direction_retour= listeNomsArrets[0]
        #Création et ajout des différents arrets de bus présents dans la ligne de bus en paramètre
        for i,nomArret in enumerate(listeNomsArrets):
            #Création des différents horaires pour cet arret pour cette ligne (semaine ou vacances, aller ou retour)
            horaires_semaine_aller = Horaire(line, direction_aller, True, lineInfos["regular_date_go"][nomArret])
            horaires_semaine_retour = Horaire(line, direction_retour, True, lineInfos["regular_date_back"][nomArret])
            horaires_vacances_aller = Horaire(line, direction_aller, False, lineInfos["we_holidays_date_go"][nomArret])
            horaires_vacances_retour = Horaire(line, direction_retour, False, lineInfos["we_holidays_date_back"][nomArret])
            #Si l'arret en cours de traitement n'est pas déjà dans la liste des arrets du plan
            if self.is_in_arrets(nomArret) == False:
                #Création de l'arret en cours 
                currentArret = Arret(nomArret)
            #Sinon, le currentArret correpond à l'arret dans la liste des arrets du plan
            else:
                currentArret = self.is_in_arrets(nomArret)
            #Ajout des différents horaires qui lui sont liés, et de la ligne en cours
            currentArret.add_ligne(line)
            currentArret.add_horaire(horaires_semaine_aller)
            currentArret.add_horaire(horaires_semaine_retour)
            currentArret.add_horaire(horaires_vacances_aller)
            currentArret.add_horaire(horaires_vacances_retour)
            #Ajout de la connexion entre l'arret en cours et le dernier arret ajouté (si l'arret en cours n'est pas le premier arret)
                #POISY-COLLEGE et LYCEE-DE-POISY se suivent dans la liste mais ne sont pas liés entre eux
            if i != 0 and nomArret != "POISY-COLLEGE":
                currentConnexion = Connexion([self.is_in_arrets(listeNomsArrets[i-1]),currentArret],line, direction_aller, direction_retour)
                self.add_connexion(currentConnexion)
                #Cas particulier des arrets "LYCEE-DE-POISY" et "POISY-COLLEGE", qui sont deux terminus distincs de la ligne 1
                    #non reliés entre eux (Vernod, l'arret suivant, est donc relié aux deux, et les bus s'arretent soit à l'un,
                    #soit à l'autre
                if nomArret == "Vernod":
                    connexionLycee = Connexion([self.is_in_arrets(listeNomsArrets[i-2]),currentArret],line, direction_aller, direction_retour)
                    self.add_connexion(connexionLycee)
            if self.is_in_arrets(nomArret) == False:
                #Ajout de l'arret s'il n'existe pas déjà
                self.add_arret(currentArret)
    

    def chemin(self,arretDepart,arretArrivee, shortestWay):
        """
        Méthode récursive qui reconstruit le chemin entre un arret de départ et d'arrivée, en utilisant l'attribut "get_shortestWayToSelf" des arrets.
        Cet attribut d'un arret A contient l'arret B qui précède l'arret A, donc en repartant du dernier arret on peut revenir jusqu'au premier.
        Parametres :
            -arretDepart(Arret) : l'arret de depart
            -arretArrivee(Arret) : l'arret d'arrivee
            -shortestWay : la liste des arrets qui est modifiée dans le traitement récursif
        Retourne :
            - le chemin entre un arretDepart et un arretArrivee, sous la forme d'une liste d'arrets, dans l'ordre
        """
        if arretArrivee.get_shortestWayToSelf()[1] == arretDepart:
            return [arretDepart, arretArrivee] + shortestWay
        else:
            return self.chemin(arretDepart,arretArrivee.get_shortestWayToSelf()[1], [arretArrivee] + shortestWay)

    def djikstra(self,arretDepart,arretArrivee,typeChemin,dateDepart=["01/01/70","00:00"]):
        """
        Algorithme qui calcule le chemin le chemin le plus court entre deux arrets
        Parametres :
            -arretDepart(Arret) : l'arret de depart
            -arretArrivee(Arret) : l'arret d'arrivee
            -typeChemin(String) : le type de chemin (shortest/fastest/foremost)
            -dateDepart(liste d'une date et d'une heure) : la date à laquelle l'utilisateur veut se déplacer
        Retourne :
            - le chemin entre un arretDepart et un arretArrivee, sous la forme d'une liste d'arrets, dans l'ordre (en utilisant la méthode précédente)
        """
        etape = 0
        arretsVisites = []
        search = True
        while(search):
            #Au départ, on considère que les distances de chaque sommet au sommet
            #de départ sont infinies, sauf pour le sommet de départ pour lequel la distance est nulle.
            if(etape == 0):
                for arret in self.arrets:
                    arret.set_shortestWayToSelf([math.inf, None])
                arretDepart.set_shortestWayToSelf([0, None])
                etape+=1

            else:
                #Boucle qui repère le noeud qui a le poids le plus faible pour pouvoir le traiter, parmis les noeuds non visités
                distanceMin = math.inf
                for arretTestDistance in self.arrets:
                    if (arretTestDistance not in arretsVisites) and (arretTestDistance.get_shortestWayToSelf()[0] < distanceMin):
                        arretEnCours = arretTestDistance
                        distanceMin = arretTestDistance.get_shortestWayToSelf()[0]

                #Sortie de l'algorithme lorsque l'arret en cours de traitement est l'arret d'arrivée (on n'a pas besoin d'aller plus loin)
                if arretEnCours == arretArrivee:
                    search = False
                else:
                    for arretVoisin in self.get_arrets_voisins(arretEnCours):
                        if (arretVoisin not in arretsVisites):
                            if (typeChemin == "shortest"):
                                #Dans le cas du type de chemin "shortest", on ne prend pas en compte les horaires donc les poids sont tous les 1 entre les arrets.
                                dureeDeuxArrets = 1
                                heurePassageNext = None
                                heureDepartArret1 = None
                            if (typeChemin == "fastest"):
                                #Pour le premier arret, l'heure de départ est celle passée en parametre
                                if arretEnCours == arretDepart:
                                    #tempsEntreArrets contient la durée de trajet entre l'arrêt en cours et l'arrêt voisin
                                        #ainsi que l'heure de passage du bus aux deux arrêts
                                    tempsEntreArrets = self.getTempsEntreArrets(arretEnCours,arretVoisin,dateDepart)
                                    if tempsEntreArrets is None:
                                        return None
                                    #On set l'attribut "heurePassageDepart" des arrets voisins à l'arret de depart, car cette heure
                                    #dépend de l'arret suivant.
                                    arretVoisin.set_heurePassageDepart(tempsEntreArrets[1])

                                #Pour les arrets suivants, l'heure de départ est l'heure à laquelle le bus est
                                    #arrivé à "l'arret en cours"
                                else:
                                    #On définie une nouvelle date de départ dépendant de l'heure de passage du bus à l'arret courant
                                    if arretDepart in self.get_arrets_voisins(arretEnCours) and \
                                            data2py.getTimeDelta(arretEnCours.get_heurePassageDepart(),arretEnCours.get_heurePassage()[0]) >=0:
                                        dateDepart[1] = arretEnCours.get_heurePassageDepart()
                                    else:
                                        dateDepart[1] = arretEnCours.get_heurePassage()[0]
                                    tempsEntreArrets = self.getTempsEntreArrets(arretEnCours,arretVoisin,dateDepart)
                                    if tempsEntreArrets is None:
                                        return None
                                heurePassageNext = tempsEntreArrets[2]
                                heureDepartArret1 = tempsEntreArrets[3]
                                dureeDeuxArrets = data2py.getTimeDelta(heurePassageNext,heureDepartArret1)
                            if (typeChemin == "foremost"):
                                #Pour le premier arret, l'heure de départ est celle passée en parametre
                                if arretEnCours == arretDepart:
                                    #tempsEntreArrets contient la durée de trajet entre l'arrêt en cours et l'arrêt voisin
                                        #ainsi que l'heure de passage du bus aux deux arrêts
                                    tempsEntreArrets = self.getTempsEntreArrets(arretEnCours,arretVoisin,dateDepart)
                                    if tempsEntreArrets is None:
                                        return None
                                    #On set l'attribut "heurePassageDepart" des arrets voisins à l'arret de depart, car cette heure
                                    #dépend de l'arret suivant.
                                    arretVoisin.set_heurePassageDepart(tempsEntreArrets[1])

                                #Pour les arrets suivants, l'heure de départ est l'heure à laquelle le bus est
                                    #arrivé à "l'arret en cours"
                                else:
                                    #On définie une nouvelle date de départ dépendant de l'heure de passage du bus à l'arret courant
                                    if arretDepart in self.get_arrets_voisins(arretEnCours) and \
                                            data2py.getTimeDelta(arretEnCours.get_heurePassageDepart(),
                                                                 arretEnCours.get_heurePassage()[0]) >= 0:
                                        dateDepart[1] = arretEnCours.get_heurePassageDepart()
                                    else:
                                        dateDepart[1] = arretEnCours.get_heurePassage()[0]
                                    tempsEntreArrets = self.getTempsEntreArrets(arretEnCours, arretVoisin, dateDepart)
                                    if tempsEntreArrets is None:
                                        return None

                                heurePassageNext = tempsEntreArrets[2]
                                heureDepartArret1 = tempsEntreArrets[3]
                                dureeDeuxArrets = (data2py.getTimeDelta(heurePassageNext,dateDepart[1]))


                            #si l'arret n'a pas encore de chemin le plus court OU que son chemin le plus court est plus long que ce nouveau chemin
                            if (arretVoisin.get_shortestWayToSelf()[1] is None) or (dureeDeuxArrets < arretVoisin.get_shortestWayToSelf()[0]):
                                arretVoisin.set_shortestWayToSelf([distanceMin+dureeDeuxArrets, arretEnCours])
                                #ajout de l'heure de passage (si le bus passe bien à l'arret voisin)
                                arretEnCours.set_heurePassage1(arretVoisin,heureDepartArret1)
                                arretVoisin.set_heurePassage0(heurePassageNext)
                                if arretEnCours == arretDepart:
                                    arretEnCours.set_heurePassage0(dateDepart[1])
                    arretsVisites.append(arretEnCours)
        #utilise la méthode récursive chemin(arretDepart,arretArrivee, shortestWay) pour construire
        #la liste qui contient tous les arrets entre arretDepart et arretArrivee.
        chemin = self.chemin(arretDepart,arretArrivee,[])
        #On set ici l'heure de passage du bus au premier arret, après avoir défini la direction à prendre depuis cet arret (= après le traitement
        #de djikstra)
        chemin[0].set_heurePassage1(chemin[1],chemin[1].get_heurePassageDepart())
        return chemin
                
    def getTempsEntreArrets(self, arret1, arret2, dateDepart=None):
        """
        Méthode qui retourne le temps entre deux arrets selon une heure précise
        Parametres :
            -arret1(Arret) : l'arret de depart
            -arret2(Arret) : l'arret d'arrivee
            -dateDepart(liste d'une date et d'une heure) : la date à laquelle l'utilisateur veut se déplacer
        Retourne :
            - [duree pour aller de l'arret1 au 2, heure arrivée arret1, heure arrivée arret 2, heure départ arret 1 (qui est
                différente de l'heure d'arrivée arret1 si l'on doit attendre à l'arret1 pour prendre un bus qui va a l'arret2]
        """
        connex = self.get_connexion(arret1, arret2)
        direction = connex.get_rightDirection(arret1, arret2)
        if(dateDepart is None):
            depart = dt.datetime.now()
        else:
            depart = data2py.setDateTime(dateDepart[0],dateDepart[1])
        type_jour = data2py.isSemaine(depart)
        labelHoraireArret1 = arret1.get_nom() + "_" + connex.get_ligne() + "_" + type_jour + "_" + direction
        labelHoraireArret2 = arret2.get_nom() + "_" + connex.get_ligne() + "_" + type_jour + "_" + direction
        depart = data2py.getHeure(depart)

        
        nextBus1 = arret1.horaires[labelHoraireArret1].get_next_bus(depart) #Contient [heure arrivée prochain bus, index de l'heure dans le tableau]
        #si nextBus1 vaut [None,None], cela veut dire qu'aucun horaire n'a été trouvé pour l'heure de départ spécifiée (il est trop tard)
        if nextBus1 == [None,None]:
            return None
        indexBus1 =  nextBus1[1]
        horairesArret1 = arret1.horaires[labelHoraireArret1].get_horaires()
        horairesArret2 = arret2.horaires[labelHoraireArret2].get_horaires()
        nextBus2 = horairesArret2[indexBus1]
        while nextBus2 == "-":
            indexBus1+=1
            #dans les rares cas où on veut tester le temps entre des arrets qui ne sont pas connectés après l'heure passée en paramètre
            if indexBus1 == len(horairesArret2):
                return None
            nextBus2 = horairesArret2[indexBus1]
        #Dans certains cas où on attend à l'arret 1 avant d'aller à l'arret2, l'heure de départ à ce premier arret est différente de l'heure d'arrivée,
        #on redéfinie donc l'heure de départ de ce premier arret d'après l'indice de l'heure de passage au deuxieme arret
        vraiDepartBus1 = horairesArret1[indexBus1]
        return ([data2py.getTimeDelta(nextBus2,nextBus1[0]),nextBus1[0], nextBus2, vraiDepartBus1])

        
    

   
            
            
              





# =============================================================================
# arr = Arret("Campus")
# arr.add_ligne("1")
# arr.add_ligne("2")
# hor = ["14:30","14:55","15:03","15:41"]
# arr.add_horaire(1,True,"PARC_DES_GLAISINS",hor)
# =============================================================================