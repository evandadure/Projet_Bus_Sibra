# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 10:01:18 2019

@author: evand
"""


class Connexion:

    def __init__(self, arrets,ligne, direction_0_1,direction_1_0):
        self.arrets = arrets 
        self.ligne = ligne
        self.direction_0_1 = direction_0_1
        self.direction_1_0 = direction_1_0
        
    def get_arrets(self):
        return self.arrets
        
    def get_ligne(self):
        return self.ligne
    
    def get_direction_0_1(self):
        return self.direction_0_1
    
    def get_direction_1_0(self):
        return self.direction_1_0
    
        
    def get_rightDirection(self,arret1,arret2):
        if arret1 == self.arrets[0] and arret2 == self.arrets[1]:
            return self.direction_0_1
        elif arret2 == self.arrets[0] and arret1 == self.arrets[1]:
            return self.direction_1_0
        else:
            return None
            
        