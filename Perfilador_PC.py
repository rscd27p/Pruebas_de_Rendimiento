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

from psutil import cpu_count, cpu_percent, pid_exists, Process


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


def formato_tiempo(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    seg = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{seg:06.3f}"


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

            if not pid_exists(pid):
                print("El proceso monitoreado terminó.")
                detener_evento.set()
                break

            carga_cpu = cpu_percent(percpu=True)

            elapsed_time = time.time() - start_time
            elapsed_time_formateado = formato_tiempo(elapsed_time)

            writer.writerow(
                [elapsed_time_formateado] + carga_cpu
            )

            file.flush()

            print(
                "Tiempo Transcurrido: "
                + elapsed_time_formateado
                + "\nCarga CPU: "
                + str(carga_cpu)
            )

            sleep(0.1)


def profiler(pid, results_file, print_info, detener_evento):
    """
    Ejecuta py-spy top repetidamente sobre un proceso existente.

    Esta versión permite mostrar las funciones donde el programa
    pasa más tiempo durante la ejecución.
    """

    try:

        proceso_psutil = Process(pid)

        # Inicializar medición de CPU del proceso
        proceso_psutil.cpu_percent(interval=None)

        while not detener_evento.is_set():

            if not pid_exists(pid):
                print("El proceso monitoreado finalizó.")
                detener_evento.set()
                break

            cpu_proceso = proceso_psutil.cpu_percent(interval=None)
            cpu_total = cpu_percent(interval=None)
            cpu_nucleos = cpu_percent(interval=None, percpu=True)

            cmd = [
                "py-spy",
                "top",
                "--pid",
                str(pid),
                "--rate",
                "10",
            ]

            proceso = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            try:
                sleep(2)
                proceso.terminate()
                salida, _ = proceso.communicate(timeout=5)

            except subprocess.TimeoutExpired:
                proceso.kill()
                salida = "ERROR: Timeout ejecutando py-spy top.\n"

            if salida:

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]

                separador = "=" * 80

                results_file.write("\n")
                results_file.write(separador + "\n")
                results_file.write(f"Muestra tomada en: {timestamp}\n")
                results_file.write(f"CPU del proceso PID {pid}: {cpu_proceso:.2f}%\n")
                results_file.write(f"CPU total del sistema: {cpu_total:.2f}%\n")
                results_file.write(f"CPU por núcleo: {cpu_nucleos}\n")
                results_file.write(separador + "\n")
                results_file.write(salida + "\n")

                results_file.flush()

                if print_info:
                    print(separador)
                    print(f"Muestra tomada en: {timestamp}")
                    print(f"CPU del proceso PID {pid}: {cpu_proceso:.2f}%")
                    print(f"CPU total del sistema: {cpu_total:.2f}%")
                    print(f"CPU por núcleo: {cpu_nucleos}")
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

    print("Iniciando perfilador para Windows...")
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
