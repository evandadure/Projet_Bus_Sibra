# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 10:01:18 2019

@author: evand
"""


class Connexion:
    """
    Une connexion représente le lien entre deux arrets de bus, cette dernière est donc composée de :
        -arrets(liste) : liste des deux arrets qui composent la connexion
        -ligne(string) : la ligne de bus qui passe entre les deux arrets
        -direction_0_1(string) : la direction (= le terminus de la ligne) dans le sens "premier arret de la liste 'arrets' -> deuxieme arret de la liste 'arrets'"
        -direction_0_1(string) : la direction (= le terminus de la ligne) dans le sens "deuxieme arret de la liste 'arrets' -> premier arret de la liste 'arrets'"
    """

    def __init__(self, arrets,ligne, direction_0_1,direction_1_0):
        self.arrets = arrets 
        self.ligne = ligne
        self.direction_0_1 = direction_0_1
        self.direction_1_0 = direction_1_0


    #--------- GETTERS --------------
    def get_arrets(self):
        return self.arrets
        
    def get_ligne(self):
        return self.ligne
    
    def get_direction_0_1(self):
        return self.direction_0_1
    
    def get_direction_1_0(self):
        return self.direction_1_0
    
        
    def get_rightDirection(self,arret1,arret2):
        """
        Méthode qui renvoie la direction du bus qui passe entre les deux arrets de la connexion, d'après l'ordre des paramètres
        Parametres :
            -arret1(Arret) : premier arret du trajet
            -arret2(Arret) : deuxieme arret du trajet
        Retourne :
            - la direction(string) (= le terminus de la ligne) correspondante
        """
        if arret1 == self.arrets[0] and arret2 == self.arrets[1]:
            return self.direction_0_1
        elif arret2 == self.arrets[0] and arret1 == self.arrets[1]:
            return self.direction_1_0
        else:
            return None
            
        