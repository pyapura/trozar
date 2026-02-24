#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer la Estrategia.
Última modificación: 13/08/2024 - 19.50.20
@author: ypf
"""
from abc import ABC, abstractmethod
import numpy as np

class Algoritmo(ABC): # La estrategia
    @abstractmethod
    def trozar(self, arbol,  matriz_precios):
        pass

class Laroze(Algoritmo): # Una estrategia concreta
    def __init__(self, ht=0.20):
        self.ht = ht
    def trozar(self, arbol, matriz_precios):
        h1 = self.ht
        P = matriz_precios
        m, _ = P.shape # número de especificaciones de rollo
        patron = []
        d1 = arbol.df(h1)
        for j in range(m): # j código para vincular con el tipo de rollo
            h2 = h1 + P[j][0]
            d2 = arbol.df(h2)
            while d2 >= P[j][1]:
                v = arbol.w(h1, h2)
                u = v * P[j][2]
                patron.append([j, d1, h1, d2, h2, P[j][0], v, u])
                h1 = h2
                h2 = h1 + P[j][0]
                d1 = d2
                d2 = arbol.df(h2)
        return patron


class Nasberg(Algoritmo): # Una estrategia concreta
    def __init__(self, ht=0.20, ls=0.10):
        self.ht = ht
        self.ls = ls
    def trozar(self, arbol, matriz_precios):
        T = arbol.mf(self.ht, self.ls)
        P = matriz_precios
        n, _ = T.shape # Número de nodos
        m, _ = P.shape # Número de especificaciones de rollo
        patron = []
        #Vectores "sincronizados" y variables locales del método
        VC = np.zeros((n, 2))
        AL = np.zeros((n, 2), dtype = int)
        t = 0; d_top = 0.0; d_min = 0.0 
        v = 0.0; c = 0.0; v_tot = 0.0; c_tot = 0.0
        for i in range(n):
            for j in range(m):
                t = i + int(round(P[j][0] / self.ls))
                if t < n:
                    d_top = T[t][0]
                    d_min = P[j][1]
                    if d_top >= d_min:
                        v = T[t][2] - T[i][2]
                        c = v * P[j][2]
                        v_tot = v + VC[i][0]
                        c_tot = c + VC[i][1]
                        if c_tot > VC[t][1]:
                            VC[t][0] = v_tot
                            VC[t][1] = c_tot
                            AL[t][0] = j #P[j][0]
                            AL[t][1] = i
        #Extraer los índices para construir el patrón óptimo
        _, max_i = np.argmax(VC, axis=0)
        li = [max_i]
        while max_i > 0:
            li.append(AL[max_i,1])
            max_i = AL[max_i,1]
        ind = np.array(li[::-1])
        #Construir el patrón óptimo
        p_1 = AL[ind[1:],0] # tipos
        p_2 = T[ind[:-1],:-1]; p_3 = T[ind[1:],:-1] # d1 y h1; d2 y h2
        p_4 = np.diff(ind)*self.ls  # longitud
        p_5 = np.diff(VC[ind,0]); p_6 = np.diff(VC[ind,1]) # volumen; valor
        patron = np.column_stack((p_1, p_2, p_3, p_4, p_5, p_6)).tolist()
        return [[int(rollo[0])] + rollo[1:] for rollo in patron]


class Trozador: # El Contexto
    def __init__(self, arbol, matriz_precios, algoritmo):
        self.arbol = arbol
        self.matriz_precios = matriz_precios
        self._algoritmo = algoritmo
    @property
    def algoritmo(self):
        return self._algoritmo
    @algoritmo.setter
    def algoritmo(self, algoritmo):
        self._algoritmo = algoritmo
    def trozar(self):
        return self._algoritmo.trozar(self.arbol, self.matriz_precios)
 
 
 
 
 
