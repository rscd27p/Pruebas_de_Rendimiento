# Perfilador de CPU y de línea para Python
# Refactorizado de Proyecto eBridge por Randy Cespedes <rscd27p - rcespedes27dds@gmail.com>

# Importar Bibliotecas
import sys
import csv
import subprocess
from psutil import cpu_count, cpu_percent
from os import getpid, path
from datetime import datetime
from time import sleep
from threading import Thread
import time

# Nombre de archivo
csv_filename_cores = "Logs/log_cpu_" + datetime.now().strftime("%Y-%m-%d_%H-%M") + ".csv"

# Función para analizar CPU
def cpu_analyze():
    start_time = time.time()
    with open(csv_filename_cores, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time"]+[str(n) for n in list(range(1, cpu_count(logical=True)+1))])
        file.flush()
        while(ANALIZAR):
            y = cpu_percent(percpu=True)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]]+y)
            file.flush()
            elapsedtime = time.time() - start_time
            print("Tiempo Transcurrido: " + str(elapsedtime) + " (s)" + "\nCarga CPU: " + str(y))
            sleep(0.1)

def profiler():
    while ANALIZAR:
        cmd = ["py-spy", "dump", "--pid", sys.argv[1]]

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        output, _ = p.communicate()

        cpu_total = cpu_percent(interval=0.1)
        cpu_cores = cpu_percent(percpu=True)

        results_file.write(f"Fecha: {datetime.now()}\n")
        results_file.write(f"CPU Total: {cpu_total}%\n")
        results_file.write(f"CPU por núcleo: {cpu_cores}\n\n")
        results_file.write(output)
        results_file.write("\n" + "=" * 80 + "\n")
        results_file.flush()

        if PRINT_INFO:
            print(f"CPU Total: {cpu_total}%")
            print(f"CPU por núcleo: {cpu_cores}")
            print(output)

        sleep(1)

if __name__ == "__main__":
    
    ANALIZAR = True
    PRINT_INFO = True if (sys.argv[2] == "True") else False
	# Nombre de archivo de perfilado de línea
    filename = "Logs/Resultado_de_Perfilado" + datetime.now().strftime("%Y-%m-%d_%H-%M")  + ".txt"
    results_file = open(filename, mode="w", encoding="utf-8")

    cores_analyzer = Thread(target=cpu_analyze)
    profiler_analyzer = Thread(target=profiler)

    cores_analyzer.start()
    profiler_analyzer.start()
    profiler_analyzer.join()
    results_file.close()
    ANALIZAR = False