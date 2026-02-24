#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo para proveer Data Descriptors.
Última modificación: 11/10/2023 - 11.18.20
@author: ypf
Fuentes: LineItem Take #5: A New Descriptor Type (Ramalho, 2022, p. 889) y
https://docs.python.org/3/howto/descriptor.html#complete-practical-example
"""
from abc import ABC, abstractmethod
import re

class Validador(ABC):
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, instance, value):
        valor = self.validar(self.name, value)
        instance.__dict__[self.name] = valor
    
    @abstractmethod
    def validar(self, name, value): #name se usa para informar qué atributo es
        r"""Devolver el valor validado o generar un Error apropiado"""
        pass

class Categoria(Validador):
    def __init__(self, *options):
        self.opciones = set(options)

    def validar(self, name, value):
        if value not in self.opciones:
            raise ValueError(f'El valor de {name} debe ser uno de {self.opciones}.')
        return value

class RealAcotado(Validador):
    def __init__(self, minimo=None, maximo=None):
        self.minimo = minimo
        self.maximo = maximo

    def validar(self, name, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'El tipo de {name} debe ser int o float.')
        if self.minimo is not None and value < self.minimo:
            raise ValueError(f'El valor de {name} debe ser mayor o igual que {self.minimo}.')
        if self.maximo is not None and value > self.maximo:
            raise ValueError(f'El valor de {name} debe ser menor o igual que {self.maximo}.')
        return value

class EnteroAcotado(Validador):
    def __init__(self, minimo=None, maximo=None):
        self.minimo = minimo
        self.maximo = maximo

    def validar(self, name, value):
        if not isinstance(value, int):
            raise TypeError(f'El tipo de {name} debe ser int.')
        if self.minimo is not None and value < self.minimo:
            raise ValueError(f'El valor de {name} debe ser mayor o igual que {self.minimo}.')
        if self.maximo is not None and value > self.maximo:
            raise ValueError(f'El valor de {name} debe ser menor o igual que {self.maximo}.')
        return value

class CadenaCondicionada(Validador):
    def __init__(self, regex=None):
        self.regex = regex

    def validar(self, name, value):
        if not isinstance(value, str):
            raise TypeError(f'El tipo de {name} debe ser str.')
        if self.regex is not None and not re.match(self.regex, value):
            raise ValueError(f'El valor de {name} no es válido.')
        return value
