# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 10:01:12 2019

@author: evand
"""

from horaire import Horaire

class Arret:
    
    def __init__(self, nom):
        self.nom = nom
        self.lignes = []
        #horaires est un dictionnaire dont les clés sont des strings contenant l'information sur le nom de l'arret, la ligne, le type d'horaire (semaine/vacances)et le terminus
        #exemple : Chorus_1_S_PARC-DES-GLAISINS pour le bus 1 à l'arret Chorus, en semaine et en direction de PARC-DES-GLAISINS
        self.horaires = {}
        #shortestWayToSelf est une liste contenant le poids pour arriver à cet arret, et l'arret précédent cet arret
        self.shortestWayToSelf = []
        #heurePassage est une liste contenant l'heure de passage à cet arret, et un dictionnaire contenant des clés correpondant aux arrets voisins, dont les valeurs sont
        #les prochains passages à ces arrets)
        self.heurePassage = [None,{}]
        #heurePassageDepart est utilisé uniquement par les voisins de l'arret de départ, il est utilisé dans l'algorithme de djikstra
        #pour stocker l'heure de passage au premier arret, qui dépend du deuxieme arret (= de la direction et du bus)
        self.heurePassageDepart = None

    # --------- GETTERS --------------
    def get_nom(self):
        return self.nom
    def get_lignes(self):
        return self.lignes
    def get_horaires(self):
        return self.horaires
    def get_shortestWayToSelf(self):
        return self.shortestWayToSelf
    def get_heurePassage(self):
        return self.heurePassage
    def get_heurePassageDepart(self):
        return self.heurePassageDepart
    
    def add_ligne(self,ligne):
        self.lignes.append(ligne)
        
    def set_shortestWayToSelf(self,lastArret):
        self.shortestWayToSelf = lastArret

    def set_heurePassage0(self, heure):
        self.heurePassage[0] = heure

    def set_heurePassage1(self, arret, heure):
        self.heurePassage[1][arret.get_nom()] = heure

    def set_heurePassageDepart(self, heure):
        self.heurePassageDepart = heure
    
    def add_horaire(self, horaire):
        """
        Méthode qui ajoute une liste d'horaires à la liste des listes d'horaires de l'arret
        Parametres :
            -horaire(Horaire) : une liste d'horaires à ajouter
        Retourne :
            Aucun retour
        """
        if horaire.get_is_semaine():
            periode = "S"
        else:
            periode = "V"
        nom_horaire = self.nom+"_"+str(horaire.get_ligne())+"_"+periode+"_"+str(horaire.get_direction())
        self.horaires[nom_horaire]=horaire








        