# Perfilador de CPU y de línea para Python en Raspberry PI / Linux
# Refactorizado de Proyecto eBridge por Randy Cespedes <rscd27p - rcespedes27dds@gmail.com>
# Adaptado para versiones recientes de py-spy
# Mantiene py-spy top para Raspberry PI y detiene automáticamente cuando finaliza el proceso monitoreado.

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
    return path.join(LOGS_DIR, f"log_cpu_rpi_{fecha}.csv")


def generar_nombre_archivo_perfilado():
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return path.join(LOGS_DIR, f"Resultado_de_Perfilado_RPI_{fecha}.txt")


def cpu_analyze(csv_filename_cores, detener_evento, pid):
    start_time = time.time()

    with open(csv_filename_cores, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["Time"] + [f"Core_{n}" for n in range(1, cpu_count(logical=True) + 1)]
        )

        file.flush()

        while not detener_evento.is_set():

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
    Ejecuta py-spy top sobre un proceso existente.

    En Raspberry PI / Linux, py-spy top normalmente funciona mejor que en Windows.
    Si aparece error de permisos, ejecute este script con sudo.
    """

    cmd = [
        "py-spy",
        "top",
        "--pid",
        str(pid),
        "--subprocesses",
    ]

    proceso = None

    try:
        proceso = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        while not detener_evento.is_set():

            if proceso.poll() is not None:
                break

            if not pid_exists(pid):
                print("El proceso monitoreado finalizó.")
                detener_evento.set()
                break

            line = proceso.stdout.readline()

            if line:
                line = line.rstrip()

                if line:
                    results_file.write(line + "\n")
                    results_file.flush()

                    if print_info:
                        print(line)

            else:
                sleep(0.1)

        detener_evento.set()

    except FileNotFoundError:
        results_file.write("ERROR: py-spy no está instalado o no está en el PATH.\n")
        results_file.write("Instale py-spy con:\n")
        results_file.write("python -m pip install py-spy\n")
        print("ERROR: py-spy no está instalado o no está en el PATH.")
        detener_evento.set()

    except PermissionError:
        results_file.write("ERROR: Permisos insuficientes para ejecutar py-spy.\n")
        results_file.write("En Raspberry PI / Linux intente ejecutar:\n")
        results_file.write("sudo python Perfilador.py <PID> True\n")
        print("ERROR: Permisos insuficientes para ejecutar py-spy.")
        print("Intente ejecutar el comando con sudo.")
        detener_evento.set()

    except KeyboardInterrupt:
        print("Perfilado detenido por el usuario.")
        detener_evento.set()

    except Exception as error:
        results_file.write(f"ERROR ejecutando py-spy: {error}\n")
        print(f"ERROR ejecutando py-spy: {error}")
        detener_evento.set()

    finally:
        if proceso is not None and proceso.poll() is None:
            try:
                proceso.terminate()
                proceso.wait(timeout=3)
            except Exception:
                try:
                    proceso.kill()
                except Exception:
                    pass


def mostrar_uso():
    print("Uso:")
    print("    python Perfilador.py <PID_del_programa_a_perfilar> <True|False>")
    print()
    print("Ejemplo:")
    print("    python Perfilador.py 5251 True")
    print()
    print("Descripción:")
    print("    True  -> imprime resultados en consola y guarda archivos")
    print("    False -> solo guarda archivos en Logs")
    print()
    print("En Raspberry PI, si hay error de permisos, use:")
    print("    sudo python Perfilador.py 5251 True")


if __name__ == "__main__":

    crear_directorio_logs()

    if len(sys.argv) < 3:
        mostrar_uso()
        sys.exit(1)

    try:
        pid = int(sys.argv[1])

    except ValueError:
        print("ERROR: El PID debe ser un número entero.")
        mostrar_uso()
        sys.exit(1)

    if not pid_exists(pid):
        print(f"ERROR: No existe un proceso activo con el PID {pid}.")
        print("Verifique que el programa a perfilar siga corriendo.")
        sys.exit(1)

    print_info = sys.argv[2].lower() == "true"

    csv_filename_cores = generar_nombre_archivo_cpu()
    filename = generar_nombre_archivo_perfilado()

    detener_evento = Event()

    print("Iniciando perfilador para Raspberry PI / Linux...")
    print(f"PID analizado: {pid}")
    print(f"Archivo CPU: {csv_filename_cores}")
    print(f"Archivo perfilado: {filename}")

    with open(filename, mode="w", encoding="utf-8") as results_file:

        cores_analyzer = Thread(
            target=cpu_analyze,
            args=(csv_filename_cores, detener_evento, pid),
        )

        profiler_analyzer = Thread(
            target=profiler,
            args=(pid, results_file, print_info, detener_evento),
        )

        cores_analyzer.start()
        profiler_analyzer.start()

        profiler_analyzer.join()

        detener_evento.set()

        cores_analyzer.join()

    print("Perfilado finalizado.")
    print("Revise el folder Logs para ver los resultados.")
