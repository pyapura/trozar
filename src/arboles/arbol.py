#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer la clase `Arbol`.
Última modificación: 12/02/2026 - 14.45.20
@author: ypf
"""
from abc import ABC, abstractmethod
import math
import numpy as np
import arboles.validador as validar

class Arbol(ABC):
    """Clase para representar objetos de tipo `Arbol`.

    Se provee un tipo para representar árboles individuales
    independientemente de la especie y que se describen por otros atributos
    elementales. Los atributos de instanciación han sido codificados con un
    mecanismo de validación y también se proveen otros atributos calculados
    como el área basal y el volumen total del árbol. También se proveen 
    otros métodos que permiten calcular el volumen de un segmento del fuste
    o crear la matriz que describe la forma de un fuste en formato 
    apropiado para su trozado.
    
    La clase ha sido concebida para ser heredada, fundamentalmente para
    representar la especie del árbol y los atributos o métodos que dependen
    de ella, de modo que algunos atributos o métodos están codificados como
    abstractos y la implementación concreta debe hacerse en las subclases.
    
    Attributes
    ----------
    i : int
        Identificador, *cf*. método `__init__()`.
    d : float
        Diámetro a la altura del pecho, *cf*. método `__init__()`.
    h : float
        Altura total, *cf*. método `__init__()`.    
    """
    i = validar.EnteroAcotado(minimo=0)
    d = validar.RealAcotado(minimo=0)
    h = validar.RealAcotado(minimo=0)

    #_SP : string
    #   Nombre científico de la especie, constante de clase.    
    _SP = 'Indefinida'

    def __init__(self, i, d, h):
        r"""Crea una instancia de `Arbol`.
        
        Parameters
        ----------
        i : int
            Identificador del árbol. Un número entero que identifique al 
            árbol. El valor no puede ser negativo.
        d : float
            Diámetro a la altura del pecho (cm) del árbol, con corteza. El
            valor no puede ser negativo.
        h : float
            Altura total del árbol (m). El valor no puede ser negativo.
        """
        self.i = i
        self.d = d
        self.h = h

    @property
    def g(self):
        r"""Calcula el área basal del árbol.
        
        Returns
        -------
        float
            Área basal del árbol (m\ :sup:`2`\ /ha), con corteza.
        """
        return math.pi/40000*self.d*self.d

    #@property
    @abstractmethod
    def v(self):
        r"""Calcula el volumen total del árbol.
        
        El método está codificado como abstracto, de modo que debe ser
        redefinido (*overridden*) en las subclases.
        
        Returns
        -------
        float
            Volumen total del árbol (m\ :sup:`3`\ /ha), con corteza.
        
        Notes
        -----
        El volumen total retornado debería incluir el volumen del tocón.
        """
        pass

    @abstractmethod
    def df(self, hf):
        r"""Calcula el diámetro del fuste del árbol a la altura del 
        fuste especificada.
        
        El método está codificado como abstracto, de modo que debe ser
        redefinido (*overridden*) en las subclases.
        
        Parameters
        ----------
        hf : float
            Altura del fuste del árbol (m) para la cual se requiere la
            determinación del diámetro del fuste.
        
        Returns
        -------
        float
            Diámetro del fuste del árbol (cm), con corteza, a la altura del
            fuste especificada.
        """
        pass

    @abstractmethod
    def hf(self, df):
        r"""Calcula la altura del fuste del árbol a la que se presenta
        el diámetro del fuste especificado.
        
        El método está codificado como abstracto, de modo que debe ser
        redefinido (*overridden*) en las subclases.
        
        Parameters
        ----------
        df : float
            Diámetro del fuste del árbol (cm), con corteza, para el cual se
            requiere la determinación de la altura del fuste.
        
        Returns
        -------
        float
            Altura del fuste del árbol (m) a la que se presenta el diámetro
            del fuste especificado.
        """
        pass

    @abstractmethod
    def w(self, hp, hd):
        r"""Calcula el volumen de un segmento del fuste del árbol, entre
        una altura proximal y otra distal, ambas con respecto a la base del
        fuste.
        
        El método está codificado como abstracto, de modo que debe ser
        redefinido (*overridden*) en las subclases.
        
        Parameters
        ----------
        hp : float
            Altura proximal (m) con respecto a la base del fuste.
        hd : float
            Altura distal (m) con respecto a la base del fuste.
        
        Returns
        -------
        float
            Volumen del segmento de fuste entre las dos alturas del árbol
            especificadas (m\ :sup:`3`\ ).
        """
        pass

    def mf(self, ht, ls):
        r"""Construye la matriz del fuste del árbol en un formato apropiado
        para su trozado.
        
        En general, la estructura de la matriz se apega a la empleada en 
        la implementación del algoritmo de trozado de un fuste que se 
        describe en [1]_.    
        
        Parameters
        ----------
        ht : float
            Altura del corte de apeo del árbol o altura del tocón (m).
        ls : float
            Longitud del segmento para determinar los potenciales puntos
            de trozado del fuste del árbol (m).
        
        Returns
        -------
        ndarray, dtype=float32
            Las filas de la matriz se corresponden con potenciales puntos
            de trozado del fuste, empezando a la altura del tocón (`ht`) y
            luego a intervalos fijos dados por la longitud del segmento
            (`ls`). Cada fila contiene el diámetro con corteza (cm) a la 
            altura del fuste especificada, la propia altura del fuste 
            especificada (m) y el volumen acumulado desde el tocón hasta la
            altura del fuste especificada (m\ :sup:`3`\ ), cada uno en su 
            respectiva columna y en el orden indicado.
        
        Notes
        -----
        Para la construcción de la matriz, este método invoca los métodos
        `df()` y `w()`. Esto implica que la matriz resultará *apropiada* 
        para simular el trozado del fuste si dichos métodos se han 
        codificado con funciones que cumplen criterios de buen
        comportamiento como los que se detallaron en [2]_.
        
        References
        ----------
        .. [1] Simosol. (2016). "SIMO: Adaptable Simulation & 
           Optimization". SIMO Documentation. Release 1.0.0. Simosol Oy,
           Finlandia.
        .. [2] Goulding, C. & Murray, J. (1976). "Polynomial taper 
           equations that are compatible with tree volume equations". New
           Zealand Journal of Forestry Science 5 (3): 313-322.
        """
        n = int(((self.h-ht)/ls) + 1)
        _alts = [_n * ls + ht for _n in range(n)]
        _dmts = [self.df(hf) for hf in _alts]
        _vlms = [0.] + [self.w(_alts[i], _alts[i+1]) 
                        for i in range(len(_alts)-1)]
        _vols = np.cumsum(_vlms)
        
        return np.stack((_dmts, _alts, _vols), axis=-1, dtype=np.float32)
    
    def __eq__(self, other):
        r"""Devuelve verdadero si dos árboles son iguales.
        
        Se implementa la comparación entre instancias de la clase frente 
        al operador `==` de igualdad. La comparación tiene en cuenta la 
        especie del árbol y los siguientes atributos numéricos: 
        identificador (`i`), diámetro a la altura del pecho (`d`) y altura
        total de árbol (`h`). En otras palabras, para que dos árboles sean 
        considerados iguales, deben ser de la misma especie e instanciarse 
        con idéntica combinación de los tres atributos numéricos. Este 
        método se usará al componer la clase árboles (`Arboles`).
        """
        # No se necesita implementar __ne__ (no se retorna NotImplemented) 
        if type(self) is type(other):
            return (self.i, self.d, self.h) == (
                other.i, other.d, other.h)
        return False
    
    def __hash__(self):
        r"""Devuelve el *hash value* de un objeto de la clase.
        
        La implementación incluye el nombre científico de la especie, para
        evitar la igualdad entre árboles de diferentes especies (i.e., 
        subclases) cuando tienen la misma combinación de atributos 
        numéricos.
        """
        return hash((self._SP, self.i, self.d, self.h))