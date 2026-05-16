# Este código forma parte de la actividad de la semana 3 del curso de TSEV-008 Validación de Sistemas Embebidos
# En este se verá el efecto de realizar generación de números aleatorios y operaciones matemáticas dentro de un ciclo for.

import random
import sys
from os import getpid


def crear_numeros_random(cantidad: int = 1):
    for i in range(cantidad):
        x = random.random() * random.random() + cantidad


def obtener_cantidad_desde_argumentos(argumentos):
    """
    Esta función busca el primer argumento numérico positivo recibido por consola.

    Se hace de esta forma para que el programa funcione tanto cuando se ejecuta
    directamente con Python como cuando se ejecuta usando Scalene, ya que Scalene
    puede agregar argumentos adicionales internamente.
    """

    for argumento in argumentos:
        try:
            cantidad = int(argumento)

            if cantidad > 0:
                return cantidad

        except ValueError:
            continue

    return None


if __name__ == "__main__":
    print("------------ Bienvenido al programa para probar consumo de CPU ------------")

    args = sys.argv[1:]

    pid = getpid()
    print("El PID del proceso es: %d - Este puede ser usado por el perfilador" % pid)
    input("Presione enter para continuar")

    cantidad_random = obtener_cantidad_desde_argumentos(args)

    if cantidad_random is None:
        print("El sistema debe tener por lo menos 1 argumento válido:")
        print("         1 - El número de elementos aleatorios a crear.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()

    print("     El sistema va a generar %d números aleatorios" % cantidad_random)

    crear_numeros_random(cantidad_random)

    print("El programa está terminando...")
