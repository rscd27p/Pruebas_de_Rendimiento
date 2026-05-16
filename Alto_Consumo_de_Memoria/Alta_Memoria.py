# Este código forma parte de la actividad de la semana 3 del curso de TSEV-008 Validación de Sistemas Embebidos
# En este se verá el efecto de guardar múltiples números aleatorios en memoria.

import random
from typing import List
import sys


# La siguiente función tiene el objetivo de crear un arreglo de datos de números aleatorios utilizando
# la biblioteca de random de Python

def guardar_numeros_random(cantidad: int = 1, num_random: List[float] = None):

    if num_random is None:
        num_random = []

    for i in range(cantidad):
        num_random.append(random.random())

    return num_random


def obtener_cantidad_desde_argumentos(argumentos):
    """
    Busca el primer argumento entero positivo.
    Esto permite compatibilidad con Scalene.
    """

    for argumento in argumentos:

        try:
            valor = int(argumento)

            if valor > 0:
                return valor

        except ValueError:
            continue

    return None


if __name__ == "__main__":

    print("------------ Bienvenido al programa para probar consumo de memoria ------------")

    args = sys.argv[1:]

    cantidad_random = obtener_cantidad_desde_argumentos(args)

    if cantidad_random is None:
        print("El sistema debe tener por lo menos 1 argumento válido:")
        print("         1 - El número de elementos aleatorios a guardar en memoria.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()

    print("     El sistema va a generar %d números aleatorios y guardarlos en un arreglo" % cantidad_random)

    guardar_numeros_random(cantidad_random)

    print("Termina")
