# Bienvenido a trozar

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/trozar.svg)](https://pypi.org/project/trozar/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/trozar.svg)](https://pypi.org/project/trozar/)  |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

El paquete **trozar** simula el trozado óptimo de fustes de árboles individuales. El programa funciona de manera autónoma y puede procesar un árbol a la vez o una lista de árboles de la misma especie. En esta versión se han codificado las rutinas para tres de las especies más cultivadas en Misiones y Corrientes, República Argentina. Pero el enfoque adoptado para la programación hace que se puedan incorporar otras especies con facilidad, al igual que otros algoritmos de trozado. En esta versión también se ha incluido un segundo algoritmo, el que no necesariamente encuentra patrones de trozado óptimos.

## Instalación y uso

El paquete se puede instalar en un cualquier ambiente activado de Python mediante pip:

```bash
$ pip install trozar
```

Para invocar la interfaz de línea de comandos (*cli*) en la consola:

```bash
>>> trozar --help
```

Finalmente, para usar el paquete como una librería:

```python
>>> from arboles.arbol_pita import ArbolPita
>>> arb_11 = ArbolPita(i=11, d=35., h=27.5)
>>> print(arb_11)
```

## Copyright

- Copyright © 2026 Pablo Yapura.
- Free software distributed under the [GNU General Public License](./LICENSE).
