#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer la clase `MatrizPrecios`.
Última modificación: 16/01/2026 - 15.20.40
@author: ypf
"""
import csv
import numpy as np
from arboles.especificacion import Especificacion

# Helper de módulo:
# Elimina líneas en blanco y comentarios de una línea al estilo Python, i.e. 
# elimina el carácter "#" y todo el texto a continuación hasta el final de la
# línea. El argumento csvfile debe cumplir las exigencias del argumento del 
# mismo nombre en el módulo csv. 
# Fuente: sigvaldm @ https://stackoverflow.com/a/50592259
def _decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw

class MatrizPrecios:
    """Clase para representar objetos de tipo `MatrizPrecios`.

    Se provee un tipo para representar matrices de precios. Una matriz de 
    precios es un conjunto de especificaciones que detalla todos los tipos 
    de rollo que se desean o pueden obtener simultáneamente, *i.e.* en la 
    misma operación de trozado. Se proveen métodos para manipular y 
    consultar atributos de la matriz de precios, incluyendo la 
    implementación del protocolo de secuencia. Los datos de la matriz de 
    precios que se necesitan en la simulación del trozado han sido 
    codificados como dos propiedades.    
    
    La clase ha sido concebida como una composición de objetos de la clase 
    `Especificacion` y para su instanciación se proveen dos constructores.
    
    Attributes
    ----------
    mp : ndarray, dtype=float32
        Matriz de precios propiamente dicha, *cf*. método `mp()`.
    mt : ndarray, dtype=U30
        Matriz de tipos, *cf*. método `mt()`.
    """
    def __init__(self, spfs):
        r"""Crea una instancia de `MatrizPrecios`.
        
        La matriz de precios se compone con una o más especificaciones de 
        rollo sin duplicaciones, *i.e.* cada especificación solo aparece 
        una única vez en la matriz instanciada.
        
        Parameters
        ----------
        spfs : list, tuple, set
            Una colección de instancias de `Especificacion`.
        
        Notes
        -----
        Si se crea una matriz de precios vacía, luego se puede usar el 
        método `agregar()` tantas veces como sea necesario para completar 
        una matríz de precios apropiada.
         
        Si la colección incluye ítems duplicados, el constructor solo 
        retiene el primer ítem de cada duplicación, dada la implementación 
        del operador de igualdad entre especificaciones (*cf*. método 
        `Especificacion.__eq__()`). 
        
        Si alguno de los ítems de la colección que se pasó como argumento 
        no se instanció como `Especificacion`, el constructor simplemente 
        lo ignora y pasa al siguiente.
        
        Examples
        --------
        >>> from especificacion import Especificacion
        >>> datos = [[1, 5, 25, 150], [2, 3.5, 20, 45], [3, 2.5, 7.5, 20]]
        >>> especificaciones = []
        >>> for i in range(len(datos)):
        >>>     especificaciones.append(Especificacion(*datos[i]))
        >>> print(repr(especificaciones[-1]))
        Especificacion(3, 2.5, 7.5, 20.0)
        """
        _set_spf = {spf for spf in spfs if isinstance(spf, Especificacion)}
        self._lst_spf = list(_set_spf)
        
    
    @classmethod
    def desde_csv(cls, csvfile):
        r"""Crea una instancia de `MatrizPrecios`.
        
        La matriz de precios se compone con una o más especificaciones de 
        rollo sin duplicaciones, *i.e.* cada especificación solo aparece 
        una única vez en la matriz instanciada.
        
        Este método de clase provee un constructor alternativo.
        
        Parameters
        ----------
        csvfile : Archivo en formato CSV
            El archivo que contiene las especificaciones de rollo. El 
            archivo .csv debe detallar los atributos de cada especificación 
            en una fila separada. Los atributos se deben separar entre si
            con comas y van en este orden: `tp`, `al`, `lt`, `dm` y `pc` 
            (*cf*. método `Especificacion.__init__()`). El constructor 
            ignora los *comentarios* de una línea al estilo Python, *i.e.* 
            elimina el carácter "#" y todo el texto a continuación hasta el 
            final de la línea. Así se puede trabajar cómodamente con una 
            plantilla compuesta por numerosas especificaciones que se 
            activan y desactivan con el carácter "#" a voluntad. En la 
            carpeta ``data``, creada durante la instalación, se provee una 
            plantilla con estas características.

        Notes
        -----
        Si la colección incluye ítems duplicados, el constructor solo 
        retiene el primer ítem de cada duplicación, dada la implementación 
        del operador de igualdad entre especificaciones (*cf*. método 
        `Especificacion.__eq__()`).
        
        Este constructor no permite crear una matriz de precios vacía.
        
        Si el archivo .csv contiene especificaciones que no pueden
        ser instanciadas por errores en los datos, la matriz de precios 
        tampoco resultará instanciada.

        Examples
        --------
        >>> from especificacion import Especificacion
        >>> datos = [[1, 5, 25, 150], [2, 3.5, 20, 45], [3, 2.5, 7.5, 20]]
        """
        self = cls.__new__(cls)
        tipos = [str, str, float, float, float]
        with open(csvfile, newline='') as f:
            reader = csv.reader(_decomment(f)) # helper de módulo
            header = next(reader)
            _set_spf = set()
            for row in reader:
                typed_row = [to_type(value) for to_type, value in zip(tipos, row)]
                _set_spf.add(Especificacion(*typed_row))
            self._lst_spf = list(_set_spf)
        return self
        

    def agregar(self, spf):
        r"""Agrega una especificación de rollo a la matriz de precios.
        
        Parameters
        ----------
        spf : Especificacion
            Un objeto de la clase `Especificacion` que se agregará a la 
            matriz de precios.
        
        Returns
        -------
        bool
            ``True``, si la especificación se agregó correctamente. 
            ``False``, si la especificación no se agregó porque una igual
            ya estaba incluida en la matriz de precios. 
        
        Raises
        ------
        TypeError
            Si se intenta agregar un objeto no instanciado como 
            `Especificacion`.
        
        Notes
        -----
        Si se intenta agregar una especificación igual a una que ya estaba
        incluida, el método simplemente la ignora y retorna ``False``.
        
        Examples
        --------
        >>> from arbol import Arbol
        >>> d = 21.5; h = 20
        >>> a_1 = Arbol(1, 1, d, h)
        >>> alturas = [0.2, 1.3, 10, 20]
        >>> print([a_1.df(hf) for hf in alturas])
        [24.026560358541584, 21.5, 14.369823009819264, 0.0]
        """
        if not isinstance(spf, Especificacion):
            raise TypeError(f'El tipo de {spf} debe ser Especificacion.')
        if spf not in self._lst_spf:
            self._lst_spf.append(spf)
            return True
        return False
        
    def remover(self, spf):
        r"""Remueve una especificación de rollo de la matriz de precios.
        
        Parameters
        ----------
        spf : Especificacion
            Un objeto de la clase `Especificacion` que se removerá de la 
            matriz de precios.
        
        Returns
        -------
        bool
            ``True``, si la especificación se removió correctamente. 
            ``False``, si la especificación no se removió porque no estaba 
            incluida en la matriz de precios. 
        
        Raises
        ------
        TypeError
            Si se intenta remover un objeto no instanciado como 
            `Especificacion`.
        
        Notes
        -----
        Si se intenta remover una especificación que no estaba incluida en 
        la matriz de precios, el método simplemente la ignora y retorna 
        ``False``.
        
        Examples
        --------
        >>> from arbol import Arbol
        >>> d = 21.5; h = 20
        >>> a_1 = Arbol(1, 1, d, h)
        >>> alturas = [0.2, 1.3, 10, 20]
        >>> print([a_1.df(hf) for hf in alturas])
        [24.026560358541584, 21.5, 14.369823009819264, 0.0]
        """
        if not isinstance(spf, Especificacion):
            raise TypeError(f'El tipo de {spf} debe ser Especificacion.')
        if spf in self._lst_spf:
            self._lst_spf.remove(spf)
            return True
        return False
                
    def es_multiplo(self, ls):
        r"""Evalua si las longitudes de rollo son multiplos del argumento.
        
        Idealmente, todas las longitudes de rollo incluidas en una matriz
        de precios deberían ser múltiplos de la longitud del segmento usada
        para construir la matriz del fuste; *c.f.* método `Arbol.mf()`.
        
        Parameters
        ----------
        ls : float
            Longitud del segmento para determinar los potenciales puntos
            de trozado del fuste del árbol (m).
        
        Returns
        -------
        bool
            ``True``, si todas las especificaciones de la matriz de precios
            son múltiplos del segmento del fuste.
        
        Examples
        --------
        >>> from arbol import Arbol
        >>> ...
        """
        _div = round(ls * 100)
        return all(round(spf.lt * 100) % _div == 0 for spf in self._lst_spf)
    
    def _ordenar(self):
        return sorted(self._lst_spf, reverse = True)
    
    @property
    def mp(self):
        r"""Devuelve la parte cuantitativa de la matriz de precios.
        
        Matriz de precios propiamente dicha, conformada por el subconjunto
        cuantitativo de los datos que conforman las especificaciones de 
        rollo. La estructura de los datos es apropiada para simular el 
        trozado de un fuste con diferentes algoritmos.
        
        Returns
        -------
        ndarray, dtype=float32
            La matriz se compone con una fila para cada especificación y 
            una columna para cada uno de sus tres atributos cuantitativos,
            `lt`, `dm` y `pc`, en ese orden. Las especificaciones están 
            ordenadas de mayor a menor, de acuerdo con sus operadores de 
            comparación (*c.f.* métodos `Especificacion.__gt__()` y 
            `Especificacion.__lt__()`).
        
        Notes
        -----
        El orden garantiza su *sincronización* coherente con el atributo 
        `mt`.
                
        Examples
        --------
        >>> from arbol import Arbol
        >>> ...
        """
        ordenada = self._ordenar()
        return np.array([[spf.lt, spf.dm, spf.pc] for spf in ordenada], dtype=np.float32)


    @property
    def mt(self):
        r"""Devuelve la parte descriptiva de la matriz de precios.
        
        Matriz de tipos, conformada por el subconjunto descriptivo de los 
        datos que conforman las especificaciones de rollo. La estructura de 
        los datos es apropiada para simular el trozado de un fuste con 
        diferentes algoritmos.
        
        Returns
        -------
        ndarray, dtype=U30
            La matriz se compone con una fila para cada especificación y 
            una columna para cada uno de sus dos atributos descriptivos,
            `tp` y `al`, en ese orden. Las especificaciones están 
            ordenadas de mayor a menor, de acuerdo con sus operadores de 
            comparación (*c.f.* métodos `Especificacion.__gt__()` y 
            `Especificacion.__lt__()`).
        
        Notes
        -----
        El orden garantiza su *sincronización* coherente con el atributo 
        `mp`.
                
        Examples
        --------
        >>> from arbol import Arbol
        >>> ...
        """
        ordenada = self._ordenar()
        return np.array([[spf.tp, spf.al] for spf in ordenada], dtype='U30')

#    def __str__(self):
#        return (f'{self.__class__.__name__}('
#                f'dimensión = {self.ne}, matriz de precios = {self.mp})')
#    def __repr__(self):
#        return (f'{self.__class__.__name__}('
#                f'{self.ne}, {self.mp})')

    def __len__(self):
        r"""Devuelve la dimensión de la matriz de precios.
        
        La dimensión de la matriz de precios refiere al número de 
        especificaciones de rollo diferentes que la componen.
        
        Returns
        -------
        int
            Número de especificaciones de rollo diferentes que componen la 
            matriz de precios.

        Notes
        -----
        Implementación concreta del método para proveer el protocolo de 
        secuencia.
        """
        return len(self._lst_spf)
    
    def __getitem__(self, index): #sequence protocol
        r"""Devuelve la especificación de rollo en la posición del índice.
        
        La implementación permite usar la notación de corchetes para 
        acceder a las especificaciones por sus posiciones en la matriz de 
        precios, ya sea individualmente o *en porciones*.
                        
        Parameters
        ----------
        index : int
            Índice que representa la posición en la matriz de precios.
        
        Returns
        -------
        Especificacion
            La especificación de rollo ubicada en la posición de la matriz
            de precios dada por el índice.

        Notes
        -----
        Implementación concreta del método para proveer el protocolo de 
        secuencia.
        """
        return self._lst_spf[index]

    def __eq__(self, other): #no probado
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False
