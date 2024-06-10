# Este código forma parte de la actividad de la semana 3 del curso de TSEV-008 Validación de Sistemas Embebidos 
# En este se vera el efecto se realizaran generación de números aleatorios y de operaciones matemáticas dentro de un ciclo for

import random
from typing import List
import sys
from os import getpid


# La siguiente función tiene el objetivo de crear un arreglo de datos de números aleatorios utilizando
# la biblioteca de random de Python

def crear_numeros_random(cantidad : int = 1):
    for i in range(cantidad):
        x = random.random()*random.random()+cantidad


if __name__ == "__main__":
    print("------------ Bienvido al programa para probar consumo de CPU ------------")
    args= sys.argv[1:] # Lista de argumentos de la función main

    pid = getpid()
    print("El PID del proceso es: %d - Este puede ser usado por el perfilador"%pid)
    input("Presione enter para continuar")

    if len(args) < 1:
        print("El sistema debe de tener por lo menos 1 argumento: ")
        print("         1 - El número de elementos aleatorios a crear.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()
    
    else: 
        args[0] = int(args[0])

    if (not isinstance(args[0], int) or not args[0] > 0):
        print("El argumento de número de números aleatorios debe ser de tipo entero y mayor que 0")
        sys.exit()

    cantidad_random = args[0]

    hilos = []

    print("     El sistema va a generar %d números aleatorios" % args[0])
    crear_numeros_random(cantidad_random)

    print("El programa esta terminando...")
        
