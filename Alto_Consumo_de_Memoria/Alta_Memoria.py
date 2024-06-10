# Este código forma parte de la actividad de la semana 3 del curso de TSEV-008 Validación de Sistemas Embebidos 
# En este se vera el efecto de tener múltiples hilos de ejecución en el uso de CPU 

import random
from typing import List
import sys


# La siguiente función tiene el objetivo de crear un arreglo de datos de números aleatorios utilizando
# la biblioteca de random de Python
def guardar_numeros_random(cantidad : int = 1, mum_random : List[float] = []):
    for i in range(cantidad):
        mum_random.append(random.random())

if __name__ == "__main__":
    print("------------ Bienvido al programa para probar consumo de CPU ------------")
    args= sys.argv[1:] # Lista de argumentos de la función main

    if len(args) < 1:
        print("El sistema debe de tener por lo menos 1 argumento: ")
        print("         1 - El número de elementos aleatorios a guardar en memoria.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()
    
    else: 
        args[0] = int(args[0])

    if (not isinstance(args[0], int) or not args[0] > 0):
        print("El argumento de número de números aleatorios debe ser de tipo entero y mayor que 0")
        sys.exit()

    cantidad_random = args[0]
    
    print("     El sistema va a generar %d números aleatorios y guardarlos en un arreglo" % args[0])
    guardar_numeros_random(cantidad_random)

    print("Termina")
        
