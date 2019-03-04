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
        self.horaires = {}
        self.shortestWayToSelf = []
        self.heurePassage = [None,{}]
        self.heurePassageDepart = None
        
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
        if horaire.get_is_semaine():
            periode = "S"
        else:
            periode = "V"
        nom_horaire = self.nom+"_"+str(horaire.get_ligne())+"_"+periode+"_"+str(horaire.get_direction())
        self.horaires[nom_horaire]=horaire








        