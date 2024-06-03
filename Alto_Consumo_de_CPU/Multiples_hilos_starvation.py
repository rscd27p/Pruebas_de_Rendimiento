# Este código forma parte de la actividad de la semana 3 del curso de TSEV-008 Validación de Sistemas Embebidos 
# En este se vera el efecto de tener múltiples hilos de ejecución en el uso de CPU 

import threading
import random
from typing import List
import sys


# La siguiente función tiene el objetivo de crear un arreglo de datos de números aleatorios utilizando
# la biblioteca de random de Python
def guardar_numeros_random(cantidad : int = 1, mum_random : List[float] = []):
    for i in range(cantidad):
        mum_random.append(random.random())

def crear_numeros_random(cantidad : int = 1):
    for i in range(cantidad):
        x = random.random()*random.random()


if __name__ == "__main__":
    print("------------ Bienvido al programa para probar consumo de CPU ------------")
    args= sys.argv[1:] # Lista de argumentos de la función main

    if len(args) < 2:
        print("El sistema debe de tener por lo menos 2 argumentos: ")
        print("         1 - El número de hilos a crear.")
        print("         2 - El número de elementos aleatorios a crear.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()
    
    else: 
        args[0] = int(args[0])
        args[1] = int(args[1])

    if (not isinstance(args[0], int) or not args[0] > 0):
        print("El argumento de número de hilos debe ser de tipo entero y mayor que 0")
        sys.exit()
    if (not isinstance(args[1], int) or not args[1] > 0):
        print("El argumento de número de números aleatorios debe ser de tipo entero y mayor que 0")
        sys.exit()

    num_hilos = args[0]
    cantidad_random = args[1]

    hilos = []

    print("     El Sistema va a crear %d hilos." % args[0])
    print("     Cada hilo va a generar %d números aleatorios" % args[1])
    for i in range(0, num_hilos):
        hilo = threading.Thread(target=crear_numeros_random(cantidad_random), args=(i,))
        hilos.append(hilo)

    for t in hilos:
        t.start()
    
    for t in hilos:
        t.join()
        
    print("Termina")
        
