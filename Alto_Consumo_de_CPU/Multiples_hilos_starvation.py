import threading
import random
import sys


def crear_numeros_random(cantidad: int = 1):
    for i in range(cantidad):
        x = random.random() * random.random()


def obtener_enteros_desde_argumentos(argumentos):
    enteros = []

    for argumento in argumentos:
        try:
            valor = int(argumento)

            if valor > 0:
                enteros.append(valor)

        except ValueError:
            continue

    return enteros


if __name__ == "__main__":
    print("------------ Bienvenido al programa para probar consumo de CPU ------------")

    args = sys.argv[1:]
    enteros = obtener_enteros_desde_argumentos(args)

    if len(enteros) < 2:
        print("El sistema debe tener por lo menos 2 argumentos válidos:")
        print("         1 - El número de hilos a crear.")
        print("         2 - El número de elementos aleatorios a crear.")
        print(" Nota: Ver manual de instrucciones para valores sugeridos y diferentes elementos.")
        sys.exit()

    num_hilos = enteros[0]
    cantidad_random = enteros[1]

    hilos = []

    print("     El sistema va a crear %d hilos." % num_hilos)
    print("     Cada hilo va a generar %d números aleatorios" % cantidad_random)

    for i in range(num_hilos):
        hilo = threading.Thread(target=crear_numeros_random, args=(cantidad_random,))
        hilos.append(hilo)

    for t in hilos:
        t.start()

    for t in hilos:
        t.join()

    print("Termina")
