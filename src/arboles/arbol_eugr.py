#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer la clase `ArbolEugr`.
Última modificación: 19/02/2026 - 15.23.30
@author: ypf
"""
import math
#import numpy as np
from arboles.arbol import Arbol

class ArbolEugr(Arbol):
    """Clase para representar objetos de tipo `ArbolEugr`.
    Una subclase que hereda de 'Arbol' y provee un tipo para representar
    árboles individuales de *Eucalyptus grandis*. A los atributos de la 
    superclase se agrega uno nuevo para describir la especie y también es 
    tratado como una propiedad. El resto de los atributos o métodos 
    codifican la implementación concreta de los marcados como abstractos en
    la superclase.
        
    Attributes
    ----------
    i : int
        Identificador, heredado de `Arbol`.
    d : float
        Diámetro a la altura del pecho, heredado de `Arbol`.
    h : float
        Altura total, heredado de `Arbol`.
    """
    #_SP : string
    #    Nombre científico de la especie, constante de la subclase.
    _SP = 'Eucalyptus grandis'
    #_GAMMA : float
    #    Constante necesaria para varias funciones de la clase.
    _GAMMA = 2.1209
    
    def __init__(self, i, d, h):
        r"""Crea una instancia de `ArbolEugr`.
        
        Parameters
        ----------
        i : int
            Identificador, heredado de `Arbol`.
        d : float
            Diámetro a la altura del pecho, heredado de `Arbol`.
        h : float
            Altura total, heredado de `Arbol`.
        """
        super().__init__(i, d, h)
    
    @property
    def v(self):
        r"""Calcula el volumen total del árbol.

        Codificación concreta del método abstracto de la superclase. Se usó
        la función de [1]_.

        Returns
        -------
        float
            Volumen total del árbol (m\ :sup:`3`\ /ha), con corteza.
        
        Notes
        -----
        El volumen total retornado incluye el volumen del tocón. El volumen
        total sin tocón se puede obtener detrayendo el volumen del tocón
        calculado con el método `w()`.
        
        References
        ----------
        .. [1] Yapura, P.; Fassola, H.; Crechi, E.; Keller, A.; Sañudo, G.; 
        Caraballo, H.; Gonzalez, C. & Altamirano, R. (2014). Optimización 
        del trozado de fustes de *Pinus taeda*, pino híbrido (*Pinus 
        elliottii* × *Pinus caribaea* F2) y *Eucalyptus grandis* en las 
        provincias de Misiones y noreste de Corrientes. Proyecto PIA 10107: 
        Informe final. Inédito. 49 pp.
        """
        gamma = self._GAMMA
        return (math.pi/40000*math.pow(1.3, gamma-2)*self.d*self.d*
                math.pow(self.h, 4-gamma))/\
                ((3-gamma)*(4-gamma)*(self.h-1.3))

    def df(self, hf):
        r"""Calcula el diámetro del fuste del árbol a la altura del 
        fuste especificada.
        
        Codificación concreta del método abstracto de la superclase. Se usó
        la función de [1]_.
        
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
        
        References
        ----------
        .. [1] Yapura, P.; Fassola, H.; Crechi, E.; Keller, A.; Sañudo, G.; 
        Caraballo, H.; Gonzalez, C. & Altamirano, R. (2014). Optimización 
        del trozado de fustes de *Pinus taeda*, pino híbrido (*Pinus 
        elliottii* × *Pinus caribaea* F2) y *Eucalyptus grandis* en las 
        provincias de Misiones y noreste de Corrientes. Proyecto PIA 10107: 
        Informe final. Inédito. 49 pp.
        """
        gamma = self._GAMMA
        return math.sqrt(self.d*self.d*math.pow(hf/1.3, 2-gamma)
                         *(self.h-hf)/(self.h-1.3))

    # Devuelve la derivada de la función de forma -i.e. del método df()- en hf,
    # dados d y h, los argumentos de la función de forma. La derivada da error 
    # en hf=0 porque la función de forma está indeterminada en h=0. También da 
    # error en hf=h, donde la función de forma se comporta correctamente porque 
    # retorna df=0. Se deben evitar estos valores al invocarla.
    def _derivada(self, d, h, hf):
        c = 2-self._GAMMA
        xsa = hf / 1.3
        xsaec = math.pow(xsa, c)
        hma = h - 1.3
        hmx = h - hf
        numerador = d * xsaec * ((c+1)*hf-c*h)
        denominador = 2 * hma * hf * math.sqrt(hmx*xsaec/hma)
        return - (numerador / denominador)
    
    # Devuelve el valor de hf dado un df especificado usando el método de 
    # Newton-Raphson, dado que la función de forma no es soluble para hf. El df
    # especificado es el argumento obj y el argumento ini es una estimación 
    # inicial del valor buscado, i.e. es una altura del fuste. Siendo x una 
    # altura del fuste, la fun() que se pasa como argumento debe ser el método 
    # df(x)-obj, y der(x), que también se pasa como argumento, es la derivada de
    # la función de forma en x. La tolerancia tol es coherente con una precisión
    # de 1 cm para una altura del fuste.
    def _newton_raphson(self, obj, fun, der, ini, tol=1e-3):
        fin = ini - fun(ini, obj) / der(ini)
        while not abs(fin - ini) < tol:
            ini = fin
            fin = ini - fun(ini, obj) / der(ini)
        return fin

    def hf(self, df):
        r"""Calcula la altura del fuste del árbol a la que se presenta
        el diámetro del fuste especificado.
        
        Codificación concreta del método abstracto de la superclase. Se usó
        el método de Newton-Raphson, una técnica numérica, puesto que la 
        función de forma adoptada es insoluble para `hf`.
                
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
        
        Raises
        ------
        ValueError
            La función solo retorna valores para 0,01 < `hf` <= `h`.
        """
        if df == 0:
            return self.h
        elif 0 < df < self.df(0.01):
            def _fun(x, df):
                return self.df(x) - df
            def _der(x):
                return self._derivada(self.d, self.h, x)
            return self._newton_raphson(df, _fun, _der, self.h/2)
        else:
            raise ValueError(
                f'Argumento inválido: Este fuste no presenta un df={df} '
                f'en ninguna de sus hf.')

    def w(self, hp, hd):
        r"""Calcula el volumen de un segmento del fuste del árbol, entre
        una altura proximal y otra distal, ambas con respecto a la base del
        fuste.
        
        Codificación concreta del método abstracto de la superclase. Se usó
        la función de [1]_.
        
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
        
        References
        ----------
        .. [1] Yapura, P.; Fassola, H.; Crechi, E.; Keller, A.; Sañudo, G.; 
        Caraballo, H.; Gonzalez, C. & Altamirano, R. (2014). Optimización 
        del trozado de fustes de *Pinus taeda*, pino híbrido (*Pinus 
        elliottii* × *Pinus caribaea* F2) y *Eucalyptus grandis* en las 
        provincias de Misiones y noreste de Corrientes. Proyecto PIA 10107: 
        Informe final. Inédito. 49 pp.
        """
        gamma = self._GAMMA
        a = (gamma - 4)*self.h
        b = 3 - gamma
        c = gamma*gamma - 7*gamma + 12
    
        return math.pi/40000*self.d*self.d*math.pow(1.3, gamma-2)/(self.h-1.3) * ((a*math.pow(hp, 3) + b*math.pow(hp, 4)) / (c*math.pow(hp, gamma)) - (a*math.pow(hd, 3) + b*math.pow(hd, 4)) / (c*math.pow(hd, gamma)))

    def __str__(self):
        return (f'{self.__class__.__name__}('
                f'especie={self._SP}, '
                f'identificador={self.i}, '
                f'dap={self.d}, '
                f'altura total={self.h})')

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.i}, {self.d}, {self.h})')
