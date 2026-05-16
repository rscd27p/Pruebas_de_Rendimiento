# Perfilador de CPU y de línea para Python en Windows
# Refactorizado de Proyecto eBridge por Randy Cespedes <rscd27p - rcespedes27dds@gmail.com>
# Adaptado para versiones recientes de py-spy
# Diseñado para computadoras personales o máquinas virtuales con Windows

import sys
import csv
import subprocess
import time
from os import path, makedirs
from datetime import datetime
from time import sleep
from threading import Thread, Event

from psutil import cpu_count, cpu_percent, pid_exists


LOGS_DIR = "Logs"


def crear_directorio_logs():
    if not path.exists(LOGS_DIR):
        makedirs(LOGS_DIR)


def generar_nombre_archivo_cpu():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return path.join(LOGS_DIR, f"log_cpu_windows_{fecha}.csv")


def generar_nombre_archivo_perfilado():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return path.join(LOGS_DIR, f"Resultado_de_Perfilado_Windows_{fecha}.txt")


def cpu_analyze(csv_filename_cores, detener_evento, pid):
    """
    Monitorea el uso de CPU por núcleo mientras el proceso exista.
    """

    start_time = time.time()

    with open(csv_filename_cores, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(
            ["Time"] + [f"Core_{n}" for n in range(1, cpu_count(logical=True) + 1)]
        )

        file.flush()

        while not detener_evento.is_set():

            # Si el proceso terminó, detener monitoreo
            if not pid_exists(pid):
                print("El proceso monitoreado terminó.")
                detener_evento.set()
                break

            carga_cpu = cpu_percent(percpu=True)

            writer.writerow(
                [datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]] + carga_cpu
            )

            file.flush()

            elapsed_time = time.time() - start_time

            print(
                "Tiempo Transcurrido: "
                + str(round(elapsed_time, 2))
                + " (s)"
                + "\nCarga CPU: "
                + str(carga_cpu)
            )

            sleep(0.1)


def profiler(pid, results_file, print_info, detener_evento):
    """
    Ejecuta py-spy dump repetidamente sobre un proceso existente.

    Esta versión es más estable en Windows que py-spy top.
    """

    try:

        while not detener_evento.is_set():

            # Verificar si el proceso sigue vivo
            if not pid_exists(pid):
                print("El proceso monitoreado finalizó.")
                detener_evento.set()
                break

            cmd = [
                "py-spy",
                "dump",
                "--pid",
                str(pid),
            ]

            proceso = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            try:
                salida, _ = proceso.communicate(timeout=5)

            except subprocess.TimeoutExpired:
                proceso.kill()
                salida = "ERROR: Timeout ejecutando py-spy dump.\n"

            if salida:

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

                separador = "=" * 80

                results_file.write("\n")
                results_file.write(separador + "\n")
                results_file.write(f"Muestra tomada en: {timestamp}\n")
                results_file.write(separador + "\n")
                results_file.write(salida + "\n")

                results_file.flush()

                if print_info:
                    print(separador)
                    print(f"Muestra tomada en: {timestamp}")
                    print(separador)
                    print(salida)

            sleep(0.5)

    except FileNotFoundError:

        results_file.write(
            "ERROR: py-spy no está instalado o no está en el PATH.\n"
        )

        results_file.write(
            "Instale py-spy utilizando:\n"
        )

        results_file.write(
            "python -m pip install py-spy\n"
        )

        print("ERROR: py-spy no está instalado o no está en el PATH.")

        detener_evento.set()

    except PermissionError:

        results_file.write(
            "ERROR: Permisos insuficientes para ejecutar py-spy.\n"
        )

        print("ERROR: Ejecute CMD o PowerShell como Administrador.")

        detener_evento.set()

    except KeyboardInterrupt:

        print("Perfilado detenido por el usuario.")

        detener_evento.set()

    except Exception as error:

        results_file.write(
            f"ERROR ejecutando py-spy: {error}\n"
        )

        print(f"ERROR ejecutando py-spy: {error}")

        detener_evento.set()


def mostrar_uso():

    print("Uso:")
    print("    python Perfilador_PC.py <PID_del_programa_a_perfilar> <True|False>")
    print()

    print("Ejemplo:")
    print("    python Perfilador_PC.py 12540 True")
    print()

    print("Descripción:")
    print("    True  -> imprime resultados en consola y guarda archivos")
    print("    False -> solo guarda archivos en Logs")
    print()

    print("Nota:")
    print("    Si py-spy genera errores de permisos,")
    print("    ejecute CMD o PowerShell como Administrador.")


if __name__ == "__main__":

    crear_directorio_logs()

    # Validar cantidad de argumentos
    if len(sys.argv) < 3:
        mostrar_uso()
        sys.exit(1)

    # Validar PID
    try:
        pid = int(sys.argv[1])

    except ValueError:

        print("ERROR: El PID debe ser un número entero.")

        mostrar_uso()

        sys.exit(1)

    # Verificar si el proceso existe
    if not pid_exists(pid):

        print(f"ERROR: No existe un proceso activo con el PID {pid}.")
        print("Verifique que el programa a perfilar siga corriendo.")

        sys.exit(1)

    # Determinar si imprimir información
    print_info = sys.argv[2].lower() == "true"

    # Crear nombres de archivos
    csv_filename_cores = generar_nombre_archivo_cpu()

    filename = generar_nombre_archivo_perfilado()

    detener_evento = Event()

    print("Iniciando perfilador para Windows...")
    print(f"PID analizado: {pid}")
    print(f"Archivo CPU: {csv_filename_cores}")
    print(f"Archivo perfilado: {filename}")

    # Abrir archivo de resultados
    with open(filename, mode="w", encoding="utf-8") as results_file:

        # Crear hilos
        cores_analyzer = Thread(
            target=cpu_analyze,
            args=(csv_filename_cores, detener_evento, pid),
        )

        profiler_analyzer = Thread(
            target=profiler,
            args=(pid, results_file, print_info, detener_evento),
        )

        # Iniciar hilos
        cores_analyzer.start()

        profiler_analyzer.start()

        # Esperar a que termine profiler
        profiler_analyzer.join()

        # Detener monitoreo CPU
        detener_evento.set()

        # Esperar thread CPU
        cores_analyzer.join()

    print("Perfilado finalizado.")
    print("Revise el folder Logs para ver los resultados.")
