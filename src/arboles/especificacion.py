#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer la clase `Especificación`.
Última modificación: 11/10/2025 - 21.55.55
@author: ypf
"""
import arboles.validador as validar

class Especificacion:
    """Clase para representar objetos de tipo `Especificación`.
    
    Se provee un tipo para representar una especificación de rollo. Además
    de los atributos que describen la especificación, se implementan los 
    métodos especiales (*dunders*) que se pueden invocar para comparar 
    instancias de la clase.

    La clase ha sido concebida para que sus instancias puedan ser usadas 
    en la composición de la clase `MatrizPrecios`.

    Attributes
    ----------
    tp : str
        Tipo, *cf*. método `__init__()`.
    al : str
        Alias, *cf*. método `__init__()`.
    lt : float
        Longitud, *cf*. método `__init__()`.
    dm : float
        Diámetro mínimo de la sección menor, *cf*. método `__init__()`.
    pc : float
        Precio, *cf*. método `__init__()`.
    
    """
    tp = validar.CadenaCondicionada(r'^(?!\s)[0-9A-Za-zÀ-ÿ\s\(\)_-]{1,30}$')
    al = validar.CadenaCondicionada(r'^(?!\s)[0-9A-Za-zÀ-ÿ_-]{1,6}$')
    lt = validar.RealAcotado(minimo=0)
    dm = validar.RealAcotado(minimo=0)
    pc = validar.RealAcotado(minimo=0)
    
    def __init__(self, tp, al, lt, dm, pc):
        r"""Crea una instancia de `Especificación`.
        
        Parameters
        ----------
        tp : str
            Tipo de rollo. Identificador del grupo de procesamiento o
            destino comercial o industrial del rollo especificado. Debe
            contener entre 1 y 30 caracteres y no puede empezar con un
            espacio en blanco; luego, los caracteres válidos son los de
            números y letras (incluyendo mayúsculas, minúsculas, acentuadas
            y con diéresis), además de los de guión, espacio en blanco,
            ambos paréntesis y subrayado.
        al : str
            Alias del tipo de rollo. Identificador de un alias para el
            grupo de procesamiento o destino comercial o industrial del
            rollo especificado. Debe contener entre 1 y 6 caracteres y no
            puede empezar con un espacio en blanco; luego, los caracteres
            válidos son los de números y letras (incluyendo mayúsculas,
            minúsculas, acentuadas y con diéresis), además de los de guión
            y subrayado.
        lt : float
            Longitud del tipo de rollo (m). El valor es el definido para
            este tipo de rollo, *i.e.* no es un valor mínimo admisible. El
            valor debe ser estrictamente positivo.
        dm : float
            Diámetro mínimo de la sección menor del tipo de rollo (cm),
            también conocido como diámetro en punta fina. El valor debe ser
            estrictamente positivo.
        pc : float
            Precio del tipo de rollo ($/m\ :sup:`3`\ ). La definición 
            específica depende del usuario (*e.g.* puede ser un valor neto
            del costo de elaboración o también puede ser el precio de 
            mercado). El valor debe ser estrictamente positivo.
        
        --------
        >>> from especificacion import Especificacion
        >>> spf_1 = Especificacion('Exportación', 'Exp_01', 12.1, 20, 1.00)
        >>> print(spf_1) # doctest: +ELLIPSIS
        Especificacion(tipo de rollo = Exportación, ..., precio = 1.00)
        >>> eval(repr(spf_1))==spf_1
        True
        >>> spf_2 = Especificacion('Aserrado', 'Ase_01', 12.1, 20, 1.00)
        >>> spf_3 = Especificacion('Exportación', 'Exp_02', 12.0, 20.1, 1.)
        >>> print(spf_1 == spf_2, spf_1 < spf_2, spf_1 > spf_2)
        True False False
        >>> print(spf_2 == spf_3, spf_2 < spf_3, spf_1 > spf_2)
        False True False
        >>> set_spf = {spf_1, spf_2, spf_3}
        >>> for spf in set_spf:
        ...     print(repr(spf))
        Especificacion('Exportación', 'Exp_02', 12.0, 20.1, 1.0)
        Especificacion('Exportación', 'Exp_01', 12.1, 20, 1.0)
        """
        self.tp = tp
        self.al = al
        self.lt = lt
        self.dm = dm
        self.pc = pc

    def __str__(self):
        return (f'{self.__class__.__name__}('
                f'tipo de rollo = {self.tp}, alias = {self.al}, '
                f'longitud = {self.lt:.2f}, diámetro mínimo de la sección '
                f'menor = {self.dm:.1f}, precio = {self.pc:.2f})')

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.tp!r}, {self.al!r}, {self.lt!r}, {self.dm!r}, '
                f'{self.pc!r})')
        
    def __eq__(self, other):
        r"""Devuelve verdadero si dos especificaciones son iguales.
        
        Se implementa la comparación entre instancias de la clase frente 
        al operador `==` de igualdad. En la comparación no se tiene en 
        cuenta el tipo de rollo (`tp`) ni el alias (`al`). En otras 
        palabras, dos especificaciones con idéntica combinación de precio 
        (`pc`), longitud (`lt`) y diámetro mínimo (`dm`) serán considerados
        iguales aunque se hayan codificado en tipos y/o alias diferentes. 
        Este método se usará al componer la clase matriz de precios 
        (`MatrizPrecios`), que solo trabaja con especificaciones únicas 
        para optimizar el trozado.
        """
        if isinstance(other, Especificacion):
            return (self.pc, self.lt, self.dm) == (
                other.pc, other.lt, other.dm)
        return NotImplemented
    
    def __ne__(self, other):
        r"""Devuelve verdadero si dos especificaciones son diferentes.
        
        La implementación devuelve la negación del método `__eq__()`.
        """    
        iguales = self.__eq__(other)
        return iguales if iguales is NotImplemented else not iguales
    
    def __gt__(self, other):
        r"""Devuelve verdadero si una especificación es mayor que otra.
        
        Se implementa la comparación entre instancias de la clase frente 
        al operador mayor que (`>`). Como en el método `__eq__`, en la 
        comparación tampoco se tiene en cuenta el tipo de rollo (`tp`) ni 
        el alias (`al`). Se implementa una comparación lexicográfica: 
        primero se comparan los valores comerciales de las especificaciones 
        de rollo; luego, y solamente si los valores comerciales son 
        iguales, se comparan las longitudes (`lt`); finalmente, y solamente 
        si también las longitudes son iguales, entonces se comparan los 
        diámetros mínimos (`dm`). El valor comercial es el producto del 
        precio (`pc`) por una expresión simplificada del volumen del rollo 
        especificado (`lt` * `dm` * `dm`). Este método se usará para 
        ordenar las especificaciones que compongan una instancia de la 
        clase `MatrizPrecios`.
        """
        if isinstance(other, Especificacion):
            return (
                self.pc * self.lt * self.dm * self.dm, self.lt, self.dm) > (
                other.pc * other.lt * other.dm * other.dm, other.lt, other.dm)            
        else:
            return NotImplemented

    def __lt__(self, other):
        r"""Devuelve verdadero si una especificación es menor que otra.
        
        La implementación es coherente con la que se usó en el método 
        `__gt__()`.
        """
        if isinstance(other, Especificacion):
            return (
                self.pc * self.lt * self.dm * self.dm, self.lt, self.dm) < (
                other.pc * other.lt * other.dm * other.dm, other.lt, other.dm)            
        else:
            return NotImplemented
    
    def __hash__(self):
        r"""Devuelve el *hash value* de un objeto de la clase.
        
        La implementación es estándar.
        """
        return hash((self.pc, self.lt, self.dm))
