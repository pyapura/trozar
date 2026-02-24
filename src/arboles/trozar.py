#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Script para proveer la cli.
Última modificación: 18/02/2026 - 20.05.43
@author: ypf
"""
import argparse
import sys
import importlib
from importlib.resources import files
from string import Template 
from arboles.matriz_precios import MatrizPrecios  # Absolute import
import arboles.estrategias

def informar_resultados_arbol(arbol, matriz_precios, nombre_archivo_mp, algoritmo, patron):
    alias = matriz_precios.mt[:, 1].tolist()
    tabla = ''
    for orden, rollo in enumerate(patron):
        rollo[0] = alias[rollo[0]]
        tabla += f'{orden+1:>5} {rollo[0]:>7} {rollo[7]:>8.2f} {rollo[1]:>5.1f} {rollo[3]:>5.1f} {rollo[5]:>8.2f} {rollo[2]:>8.2f} {rollo[4]:>8.2f} {rollo[6]:>7.4f} \n'
    arbol_vu = sum(lista_interior[6] for lista_interior in patron)
    arbol_vl = sum(lista_interior[7] for lista_interior in patron)
    datos = {'arbol_i': arbol.i, 'arbol_sp': arbol._SP, 'arbol_d': f'{arbol.d:.1f}', 'arbol_h': f'{arbol.h:.2f}', 'arbol_v': f'{arbol.v:.4f}', 'arbol_vu': f'{arbol_vu:.4f}', 'arbol_vl': f'{arbol_vl:.3f}', 'algoritmo': algoritmo, 'matriz_precios': nombre_archivo_mp, 'tabla': tabla}
    # hay que usar importlib para recuperar el archivo de la plantilla
    plt = files("arboles").joinpath("plantilla_resultados_arbol_individual.txt")
    with plt.open('r') as t:
        plantilla = Template(t.read())
    return plantilla.substitute(datos) # salida_final

def informar_resultados_lista(trozadores, nombre_archivo_liar, matriz_precios, nombre_archivo_mp, algoritmo):
    alias = matriz_precios.mt[:, 1].tolist()
    tabla = ''
    for trozador in trozadores:
        patron = trozador.trozar()
        arbol_id = [[trozador.arbol.i, orden + 1] for orden in range(len(patron))]
        patron = [blq_1 + blq_2 for blq_1, blq_2 in zip(arbol_id, patron)]
        for rollo in patron:
            rollo[2] = alias[rollo[2]]
            tabla += f'{rollo[0]:>5} {rollo[1]:>5} {rollo[2]:>7} {rollo[9]:>8.2f} {rollo[3]:>5.1f} {rollo[5]:>5.1f} {rollo[7]:>8.2f} {rollo[4]:>8.2f} {rollo[6]:>8.2f} {rollo[8]:>7.4f} \n'
    datos = {'lista_arb': nombre_archivo_liar, 'arbol_sp': trozador.arbol._SP, 'algoritmo': algoritmo, 'matriz_precios': nombre_archivo_mp, 'tabla': tabla}
    # hay que usar importlib para recuperar el archivo de la plantilla
    plt = files("arboles").joinpath("plantilla_resultados_lista_arboles.txt")
    with plt.open('r') as t:
        plantilla = Template(t.read())
    return plantilla.substitute(datos) # salida_final

descripcion = '''
Simula el trozado del fuste de un árbol individual, o de una lista de árboles de 
la misma especie, con diferentes algoritmos.'''

epilogo = '''
Ejemplos:
  Trozar el árbol 7 de Pinus taeda, de 32.1 cm de dap y 28.35 m de altura 
  total, usando el algoritmo de Laroze con 0.15 m de altura del tocón y con la
  matriz de precios especificada en mmpp.csv. Mostrar los resultados en 
  pantalla:

  trozar -e Pita -i 11 -d 35 -a 27.5 -t 0.2 -g Laroze -m mmpp.csv
  
  Trozar todos los árboles de la parcela registrados en p_08.csv, conformada
  únicamente por Pinus híbrido F2, usando el algoritmo de Näsberg, con la altura 
  del tocón y la longitud del segmento en sus valores por defecto y usando la 
  matriz de precios especificada en mmpp.csv. Guardar los resultados en 
  p_08.txt:
      
  trozar -e Pihi -l p_08.csv -g Nasberg -m mmpp.csv -r p_08.txt 
    
trozar, Copyright (C) 2026, Pablo Yapura.

This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you
are welcome to redistribute it under certain conditions. For details look for 
the appropriate parts of the GNU General Public License.'''

def main():
    # instanciar el parser
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = descripcion,
        epilog = epilogo,
        add_help = False)
        #usage='%(prog)s [opciones] MP.csv', #personalizar la línea `usage`
        
    # agregar los argumentos
    parser.add_argument(
        '-h', '--help', action='help', default=argparse.SUPPRESS,
        help='Muestra este mensaje de ayuda y vuelve a la línea de comandos. Para una mejor legibilidad se recomienda configurar una ventana de al menos 80 columnas para la terminal de comandos o consola.')
    
    spp_codificadas = {'Pita': 'Pinus taeda', 'Pihi': 'Pino híbrido F2',
                       'Eugr': 'Eucalyptus grandis'}
    parser.add_argument(
        '-e', '--especie', choices=[keys for keys in spp_codificadas],
        required=True,
        help='El código que especifica la especie del árbol individual o de la lista de árboles cuyo trozado se simulará. Consultar la nómina de especies codificadas y sus códigos en la documentación.')
        
    parser.add_argument(
        '-l', '--lista_arboles', type=argparse.FileType('r', encoding='utf-8'), 
        metavar='lista_arboles.csv',
        help='Un archivo en formato CSV con los datos de todos los árboles de la misma especie cuyo trozado se simulará. El archivo debe existir y residir en la carpeta o directorio actual de trabajo. Consultar la estructura de datos que debe tener este archivo en la documentación. Si no se especifica una lista, se debe suministrar toda la información necesaria para trozar un árbol individual, i.e., los argumentos opcionales --id_arbol, --dap y --altura.')

    parser.add_argument(
        '-i', '--id_arbol', type=int, metavar='n',
        help='El número entero n que identifica al árbol individual cuyo trozado se simulará. Requerido para cualquier simulación del trozado.')
        
    parser.add_argument(
        '-d', '--dap', type=float, metavar='n',
        help='El número real n que cuantifica el diámetro a la altura del pecho (en cm) del árbol individual cuyo trozado se simulará. Requerido para cualquier simulación del trozado.')
        
    parser.add_argument(
        '-a', '--altura', type=float, metavar='n',
        help='El número real n que cuantifica la altura total (en m) del árbol individual cuyo trozado se simulará. Requerido para cualquier simulación del trozado.')

    algs_codificados = {'Nasberg': 'Näsberg', 'Laroze': 'Laroze'}
    parser.add_argument(
        '-g', '--algoritmo', choices=[keys for keys in algs_codificados],
        required=True,
        help='El código que especifica el algoritmo de trozado que se empleará en la simulación. Consultar los detalles de los algoritmos codificados en la documentación. Requerido para cualquier simulación del trozado.')

    parser.add_argument(
        '-m', '--matriz_precios', type=argparse.FileType('r', encoding='utf-8'), 
        required=True, metavar='matriz_precios.csv',
        help='El archivo en formato CSV con la matriz de precios que se usará para simular el trozado. El archivo debe existir y residir en la carpeta o directorio actual de trabajo. Consultar la estructura de datos que debe tener este archivo en la documentación. Requerido para cualquier simulación del trozado.')
    
    parser.add_argument(
        '-t', '--tocon', type=float, metavar='n', default=0.2,
        help='El número real n que cuantifica la altura de corte del tocón (en m) para la simulación del trozado del árbol. Si no se especifica una altura, se usará --tocon=0.2 como valor predeterminado en cualquier simulación del trozado.')

    parser.add_argument(
        '-s', '--segmento', type=float, metavar='n', default=0.1,
        help='El número real n que cuantifica la longitud del segmento (en m) que se usa en algunos algoritmos para la simulación del trozado del árbol (e.g. Näsberg). El valor especificado debe ser múltiplo de todas las longitudes de rollo que se hayan especificado en la matriz de precios. Si no se especifica una longitud, se usará --segmento=0.1 como valor predeterminado solamente con los algoritmos de trozado que lo requieran.')

    parser.add_argument(
        '-r', '--resultados', type=argparse.FileType('w', encoding='utf-8'),
        default=sys.stdout, metavar='resultados.txt',
        help='El archivo en formato TXT con los resultados del trozado obtenido. El informe de resultados será diferente según se haya procesado un árbol individual o una lista de árboles. El archivo será grabado en la carpeta o directorio actual de trabajo. Si la opción no se especifica, los resultados se imprimirán en la salida estándar (normalmente en la pantalla).')

   # procesar la línea de comando 
    args = parser.parse_args()
    esp = args.especie
    alg = args.algoritmo
    amp = args.matriz_precios #archivo matriz precios
    toc = args.tocon
    seg = args.segmento
    
    try:
        nom_arch_mp = amp.name
        mmpp = MatrizPrecios.desde_csv(nom_arch_mp)
    except Exception as e:
        print(f'Error al procesar el archivo con la matriz de precios: {e}.')
    
    # Necesario tanto para árboles individuales como para la lista
    Estrategia = getattr(arboles.estrategias, alg)
    match alg:
        case 'Nasberg':
            algoritmo = Estrategia(toc, seg)
        case 'Laroze':
            algoritmo = Estrategia(toc)
        case _:
            pass

    if args.lista_arboles:
        try:
            nom_arch_liar = args.lista_arboles.name
            from arboles.arboles import Arboles 
            liar = Arboles.desde_csv(esp, nom_arch_liar)
            trozadores = [arboles.estrategias.Trozador(arbol, mmpp.mp, algoritmo) for arbol in liar]
            salida_final = informar_resultados_lista(trozadores, nom_arch_liar, mmpp, nom_arch_mp, alg)
        except Exception as e:
            print(f'No fue posible simular el trozado de la lista de árboles: {e}.')
    elif args.id_arbol and args.dap and args.altura:
        try:
            arbol_gesp = importlib.import_module(f'arboles.arbol_{esp.lower()}')
            ArbolGesp = getattr(arbol_gesp, f'Arbol{esp}')
            arbol = ArbolGesp(args.id_arbol, args.dap, args.altura)
            trozador = arboles.estrategias.Trozador(arbol, mmpp.mp, algoritmo)
            patron = trozador.trozar()
            salida_final = informar_resultados_arbol(arbol, mmpp, nom_arch_mp, alg, patron)
        except Exception as e:
            print(f'No fue posible simular el trozado del árbol: {e}.')
    else:
        print(f'Se esperaba una lista de árboles o la información necesaria para trozar un árbol')
        print(f'individual.')
        return None

    if args.resultados is not sys.stdout:
        with args.resultados as archivo:
            archivo.write(salida_final)
            print("Se grabó el archivo con los resultados.")
    else:
        print(salida_final)

if __name__ == '__main__':
    main()
