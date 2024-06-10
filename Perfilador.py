# Perfilador de CPU y de línea para Python
# Refactorizado de Proyecto eBridge por Randy Cespedes <rscd27p - rcespedes27dds@gmail.com>

# Importar Bibliotecas
import sys
import csv
import subprocess
from psutil import cpu_count, cpu_percent
from os import getpid, geteuid, path
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
	cmd = ["py-spy", "top", "--subprocesses", "--pid", sys.argv[1]]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
	for line in iter(p.stdout.readline, b''):
		x = str(line.rstrip())[11:]
		if(len(x)>0):
			results_file.write(x)
			
        # Cerrar archivo en caso de que se presione C
		if("Control-C" in x):
			results_file.seek(0, 0)
			
		results_file.write("\n")
		if(PRINT_INFO):
			print(x)
	p.stdout.close()
	p.wait()

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