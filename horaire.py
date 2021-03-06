# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 17:00:28 2019

@author: evand
"""
import data2py
import math

class Horaire:
    
    def __init__(self, ligne, direction, is_semaine, horaires):
        self.ligne = ligne 
        self.direction = direction 
        self.is_semaine = is_semaine 
        self.horaires = horaires

    # --------- GETTERS --------------
    def get_ligne(self):
        return self.ligne
        
    def get_direction(self):
        return self.direction
        
    def get_is_semaine(self):
        return self.is_semaine
        
    def get_horaires(self):
        return self.horaires
    
    def get_next_bus(self, heureDepart):
        """
        Méthode qui récupère l'heure de passage du prochain bus d'après une heure de départ passée en paramètre
        Parametres :
            -heureDepart(String) : l'heure de départ
        Retourne :
            Une liste contenant la prochaine heure de passage et son index dans la liste des horaires de cet arret
        """

        tempsMinimum = math.inf
        nextBus = None
        index = None
        for i,horaire in enumerate(self.horaires):
            if horaire != "-":
                timeDiff = data2py.getTimeDelta(horaire,heureDepart)
                if timeDiff >= 0 and timeDiff < tempsMinimum:
                    tempsMinimum = timeDiff
                    nextBus = horaire
                    index = i
        return [nextBus,index]
    