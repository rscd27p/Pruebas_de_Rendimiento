# Pruebas_de_Rendimiento

Este repositorio contiene los programas, herramientas e instrucciones necesarias para realizar pruebas de rendimiento como parte del curso de **Validación de Sistemas Embebidos TSEV-008** del programa de Técnico en Sistemas Embebidos de la Universidad Fidélitas.

El objetivo principal de este material es que el estudiante pueda ejecutar programas que generen consumo de CPU y memoria, observar el comportamiento del sistema mientras se ejecutan y generar evidencias que puedan ser utilizadas en los reportes del curso.

Este README contempla dos escenarios de trabajo:

1. Estudiantes que cuentan con un **Raspberry PI físico**.
2. Estudiantes que trabajan desde una **computadora personal**, **Windows** o una **máquina virtual**.

Ambos escenarios son válidos, pero los comandos cambian dependiendo de la plataforma utilizada. Por esta razón, es importante leer primero la sección de selección de plataforma.

---

## Tabla de Contenidos

- [Pruebas_de_Rendimiento](#pruebas_de_rendimiento)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Configurando RPI](#configurando-rpi)
  - [Nomenclatura de Consolas](#nomenclatura-de-consolas)
  - [Importante - Selección de Plataforma](#importante---selección-de-plataforma)
    - [Si usted tiene un Raspberry PI físico](#si-usted-tiene-un-raspberry-pi-físico)
    - [Si usted utiliza una máquina virtual o Windows](#si-usted-utiliza-una-máquina-virtual-o-windows)
  - [Estructura del Repositorio](#estructura-del-repositorio)
  - [Instalación de Bibliotecas](#instalación-de-bibliotecas)
    - [Instalación en Raspberry PI](#instalación-en-raspberry-pi)
    - [Instalación en Windows](#instalación-en-windows)
  - [Uso de Scalene en Raspberry PI](#uso-de-scalene-en-raspberry-pi)
    - [Verificar versión de Scalene](#verificar-versión-de-scalene)
    - [Perfilado en consola en Raspberry PI](#perfilado-en-consola-en-raspberry-pi)
    - [Generar perfil guardado en Raspberry PI](#generar-perfil-guardado-en-raspberry-pi)
    - [Ver reporte guardado en consola en Raspberry PI](#ver-reporte-guardado-en-consola-en-raspberry-pi)
    - [Ver reporte HTML en Raspberry PI](#ver-reporte-html-en-raspberry-pi)
    - [Reporte JSON en Raspberry PI](#reporte-json-en-raspberry-pi)
  - [Uso de Perfilador en Raspberry PI](#uso-de-perfilador-en-raspberry-pi)
    - [Paso 1 - Ejecutar el programa a perfilar](#paso-1---ejecutar-el-programa-a-perfilar)
    - [Paso 2 - Copiar el PID del proceso](#paso-2---copiar-el-pid-del-proceso)
    - [Paso 3 - Ejecutar Perfilador.py](#paso-3---ejecutar-perfiladorpy)
    - [Paso 4 - Continuar el programa principal](#paso-4---continuar-el-programa-principal)
    - [Paso 5 - Revisar resultados](#paso-5---revisar-resultados)
  - [Uso de Scalene en PC Windows](#uso-de-scalene-en-pc-windows)
    - [Verificar versión de Scalene en Windows](#verificar-versión-de-scalene-en-windows)
    - [Perfilado en consola en Windows](#perfilado-en-consola-en-windows)
    - [Generar perfil guardado en Windows](#generar-perfil-guardado-en-windows)
    - [Ver reporte guardado en consola en Windows](#ver-reporte-guardado-en-consola-en-windows)
    - [Ver reporte HTML en Windows](#ver-reporte-html-en-windows)
    - [Reporte JSON en Windows](#reporte-json-en-windows)
  - [Uso de Perfilador en PC Windows](#uso-de-perfilador-en-pc-windows)
    - [Paso 1 - Ejecutar el programa en Windows](#paso-1---ejecutar-el-programa-en-windows)
    - [Paso 2 - Copiar el PID del proceso en Windows](#paso-2---copiar-el-pid-del-proceso-en-windows)
    - [Paso 3 - Ejecutar Perfilador_PC.py](#paso-3---ejecutar-perfilador_pcpy)
    - [Paso 4 - Continuar el programa principal](#paso-4---continuar-el-programa-principal-1)
    - [Paso 5 - Revisar resultados en Windows](#paso-5---revisar-resultados-en-windows)
  - [Procesado de Datos](#procesado-de-datos)
  - [Programas a Correr](#programas-a-correr)
    - [Nota Importante para Windows o Máquina Virtual](#nota-importante-para-windows-o-máquina-virtual)
    - [Alto_CPU.py](#alto_cpupy)
    - [Multiples_hilos_starvation.py](#multiples_hilos_starvationpy)
    - [Alto_Memoria.py](#alto_memoriapy)
  - [Uso de Sleep](#uso-de-sleep)
  - [Errores Comunes y Soluciones](#errores-comunes-y-soluciones)
  - [Recomendaciones Finales](#recomendaciones-finales)

---

## Configurando RPI

Siga las instrucciones en el repositorio de la Máquina de Café para configurar su Raspberry PI.

1. [Configurar RPI](https://github.com/rscd27p/Maquina_de_Cafe/blob/main/Documentos/Configurar_RPI.md)
2. [Sección - Instalación de Software en Raspberry PI](https://github.com/rscd27p/Maquina_de_Cafe/tree/main)
3. [Real VNC](https://github.com/rscd27p/Maquina_de_Cafe/blob/main/Documentos/RealVNC.md)

Estas guías permiten preparar el Raspberry PI con el sistema operativo, herramientas de acceso remoto y ambiente de trabajo necesario para las prácticas.

> **Nota:** Si usted no cuenta con un Raspberry PI físico, puede continuar con las secciones de Windows o máquina virtual. No debe intentar ejecutar comandos de Raspberry PI si está trabajando desde Windows.

---

## Nomenclatura de Consolas

Para evitar confusiones, este documento utiliza una nomenclatura diferente para identificar dónde debe ejecutarse cada comando.

En el caso de la consola que corre en la computadora personal de Windows, los comandos se identifican de la siguiente forma:

```bash
C:\ <Comando> --parametro-1 --parametro-2
```

La consola normal del Raspberry PI se identifica como:

```bash
~S <Comando> --parametro-1 --parametro-2
```

Para el ambiente virtual `Fidelitas` en el Raspberry PI, la consola se identifica como:

```bash
(.Fidelitas) ~S <Comando> --parametro-1 --parametro-2
```

> **Nota:** No copie literalmente `C:\` o `(.Fidelitas) ~S` si su consola no lo requiere. Estos prefijos se utilizan para indicar en qué plataforma debe ejecutarse el comando.

---

# Importante - Selección de Plataforma

Antes de ejecutar cualquier comando, el estudiante debe identificar cuál ambiente está utilizando.

Este repositorio está preparado para dos tipos de estudiantes:

- Estudiantes con Raspberry PI físico.
- Estudiantes sin Raspberry PI físico, que trabajan con Windows, una computadora personal o una máquina virtual.

La selección correcta de la plataforma es importante porque:

- Los comandos de rutas cambian entre Linux/Raspberry PI y Windows.
- El perfilador del Raspberry PI no es el mismo que el perfilador de Windows.
- El consumo de CPU y memoria puede variar mucho entre una PC y un Raspberry PI.
- Una PC normalmente ejecuta los programas más rápido, por lo que puede ser necesario aumentar los ciclos.

---

## Si usted tiene un Raspberry PI físico

Debe utilizar principalmente las siguientes secciones:

- [Uso de Scalene en Raspberry PI](#uso-de-scalene-en-raspberry-pi)
- [Uso de Perfilador en Raspberry PI](#uso-de-perfilador-en-raspberry-pi)

Estas secciones fueron diseñadas para ejecutarse directamente en el Raspberry PI utilizando el ambiente virtual `Fidelitas`.

Los comandos se verán de esta forma:

```bash
(.Fidelitas) ~S python programa.py
```

### Recomendaciones para estudiantes con Raspberry PI físico

1. Verifique que el Raspberry PI esté encendido.
2. Verifique que tenga conexión de red.
3. Active el ambiente virtual `Fidelitas`.
4. Ejecute los comandos dentro del repositorio `Pruebas_de_Rendimiento`.
5. Use las rutas con `/`, por ejemplo:

```bash
./Alto_Consumo_de_CPU/Alto_CPU.py
```

6. No utilice los comandos de Windows con `.\` si está trabajando en Raspberry PI.

---

## Si usted utiliza una máquina virtual o Windows

Debe utilizar principalmente las siguientes secciones:

- [Uso de Scalene en PC Windows](#uso-de-scalene-en-pc-windows)
- [Uso de Perfilador en PC Windows](#uso-de-perfilador-en-pc-windows)

Estas instrucciones están pensadas para estudiantes que no tienen un Raspberry PI físico o que deben ejecutar las pruebas desde una computadora personal.

Los comandos se verán de esta forma:

```bash
C:\ python programa.py
```

### Recomendaciones para estudiantes con Windows o máquina virtual

1. Abra `CMD` o `PowerShell`.
2. Navegue hasta la raíz del repositorio `Pruebas_de_Rendimiento`.
3. Ejecute los comandos desde la raíz del proyecto.
4. Use las rutas con `\`, por ejemplo:

```bash
.\Alto_Consumo_de_CPU\Alto_CPU.py
```

5. Utilice el perfilador de Windows llamado `Perfilador_PC.py`.
6. Si el programa termina demasiado rápido, aumente el número de ciclos.

---

# Estructura del Repositorio

Los archivos principales se encuentran distribuidos de la siguiente forma.

En la raíz del repositorio `Pruebas_de_Rendimiento` se encuentran:

```text
Perfilador.py
Perfilador_PC.py
README.md
```

El perfilador para Raspberry PI es:

```text
Perfilador.py
```

El perfilador para Windows es:

```text
Perfilador_PC.py
```

Los programas de prueba se encuentran en los siguientes folders:

```text
./Alto_Consumo_de_CPU/
./Alto_Consumo_de_Memoria/
```

Por ejemplo:

```text
./Alto_Consumo_de_CPU/Alto_CPU.py
./Alto_Consumo_de_CPU/Multiples_hilos_starvation.py
./Alto_Consumo_de_Memoria/Alto_Memoria.py
```

En Windows, según la imagen de referencia del repositorio, `Perfilador_PC.py` se encuentra en la raíz del proyecto, al mismo nivel que `Perfilador.py` y `README.md`. Por esta razón, el comando correcto para Windows es:

```bash
C:\ python Perfilador_PC.py <PID> True
```

y no debe ejecutarse como si estuviera dentro de otro folder.

---

# Instalación de Bibliotecas

## Instalación en Raspberry PI

Adicional a esto se utilizarán las siguientes bibliotecas como parte del ambiente virtual llamado `Fidelitas`.

**Nota:** Vaya a la ubicación donde está el ambiente virtual de Fidelitas en su Raspberry PI. Por defecto, en la guía se instaló en root.

```bash
(.Fidelitas) ~S python -m pip install py-spy scalene
```

Puede verificar que Scalene quedó instalado con:

```bash
(.Fidelitas) ~S python -m scalene --version
```

Si el comando anterior muestra la versión de Scalene, entonces la instalación fue correcta.

---

## Instalación en Windows

En Windows, abra una consola de `CMD` o `PowerShell` en la raíz del repositorio.

Ejecute:

```bash
pip install py-spy psutil pandas scalene
```

También puede instalar solo Scalene con:

```bash
pip install scalene
```

Puede verificar la instalación con:

```bash
python -m scalene --version
```

Si aparece la versión de Scalene, la instalación fue correcta.

> **Nota:** Si Windows indica que `pip` no se reconoce como comando, intente usar:

```bash
python -m pip install py-spy psutil pandas scalene
```

---

# Uso de Scalene en Raspberry PI

Scalene es una herramienta de perfilado para programas de Python. Permite identificar qué partes del código consumen más CPU y memoria.

Scalene puede generar diferentes tipos de salida:

- Reporte directamente en consola.
- Reporte guardado en archivo JSON.
- Reporte HTML para abrir en navegador.
- Visualización posterior de resultados guardados.

---

## Nota sobre la versión nueva de Scalene

La versión nueva de Scalene cambió la forma de ejecutar los comandos.

Antes se usaba una sintaxis como:

```bash
python -m scalene --cpu --memory --cli programa.py
```

Sin embargo, en versiones nuevas esto puede generar errores como:

```text
ambiguous option: --cpu could match --cpu-only, --cpu-percent-threshold, --cpu-sampling-rate
```

Por esta razón, en este README se utiliza la sintaxis nueva:

```bash
python -m scalene run
```

y para visualizar resultados guardados:

```bash
python -m scalene view
```

> **Nota importante:** En Scalene 2.x ya no es necesario agregar `--cpu --memory` para las pruebas básicas. Scalene perfila automáticamente la información necesaria.

---

## Verificar versión de Scalene

En Raspberry PI, ejecute:

```bash
(.Fidelitas) ~S python -m scalene --version
```

Esto debería mostrar una salida similar a:

```text
Scalene: a high-precision CPU and memory profiler
```

---

## Perfilado en consola en Raspberry PI

Para ejecutar un programa y ver el reporte directamente en consola, utilice:

```bash
(.Fidelitas) ~S python -m scalene run --cli -- ./Alto_Consumo_de_CPU/Alto_CPU.py 1000000
```

También puede usar el comando directo si está disponible:

```bash
(.Fidelitas) ~S scalene run --cli -- ./Alto_Consumo_de_CPU/Alto_CPU.py 1000000
```

El resultado se verá de esta forma:

![Resultados_Scalene_CLI](./imgs/Resultados-Scalene-CLI.png)

### Explicación del comando

```bash
python -m scalene
```

Ejecuta Scalene como módulo de Python.

```bash
run
```

Indica que se desea perfilar un programa.

```bash
--cli
```

Indica que el resultado debe mostrarse en la consola.

```bash
./Alto_Consumo_de_CPU/Alto_CPU.py
```

Es el programa que se desea perfilar.

```bash
1000000
```

Es el argumento enviado al programa. En este caso representa la cantidad de operaciones o ciclos.

---

## Generar perfil guardado en Raspberry PI

Si desea guardar el perfilado para revisarlo después, ejecute:

```bash
(.Fidelitas) ~S python -m scalene run ./Alto_Consumo_de_CPU/Alto_CPU.py 1000000
```

Esto genera un archivo llamado:

```text
scalene-profile.json
```

Este archivo contiene la información del perfilado.

---

## Ver reporte guardado en consola en Raspberry PI

Después de generar `scalene-profile.json`, puede ver el reporte en consola con:

```bash
(.Fidelitas) ~S python -m scalene view --cli
```

Este comando no vuelve a ejecutar el programa. Solamente abre el perfil guardado.

---

## Ver reporte HTML en Raspberry PI

Después de generar el archivo `scalene-profile.json`, puede abrir el reporte HTML con:

```bash
(.Fidelitas) ~S python -m scalene view --html
```

El reporte HTML permite revisar los resultados de forma más visual desde el navegador.

Puede abrir el archivo **profile.html**, el cual se verá de la siguiente forma:

![Resultados_Scalene_HTML](./imgs/Resultados-Scalene-HTML.png)

---

## Reporte JSON en Raspberry PI

Con la versión nueva de Scalene, el archivo JSON se genera automáticamente al ejecutar:

```bash
(.Fidelitas) ~S python -m scalene run ./Alto_Consumo_de_CPU/Alto_CPU.py 1000000
```

El archivo generado por defecto será:

```text
scalene-profile.json
```

Este archivo puede conservarse como evidencia o utilizarse posteriormente con:

```bash
(.Fidelitas) ~S python -m scalene view --cli
```

o:

```bash
(.Fidelitas) ~S python -m scalene view --html
```

---

# Uso de Perfilador en Raspberry PI

Se adjunta una herramienta de perfilado sencilla escrita en Python que utiliza el módulo [py-spy](https://github.com/benfred/py-spy), que hace perfilado de línea similar a Scalene, y la herramienta [top](https://www.geeksforgeeks.org/top-command-in-linux-with-examples/).

El perfilador para Raspberry PI se llama:

```text
Perfilador.py
```

Este archivo se encuentra en la raíz del repositorio.

---

## Paso 1 - Ejecutar el programa a perfilar

Primero se debe ejecutar el programa que se desea analizar.

Por ejemplo:

```bash
(.Fidelitas) ~S python ./Alto_Consumo_de_CPU/Alto_CPU.py 10000000
```

El programa mostrará un mensaje similar al siguiente:

```text
------------ Bienvenido al programa para probar consumo de CPU ------------
El PID del proceso es: 5251 - Este puede ser usado por el perfilador
Presione enter para continuar
```

---

## Paso 2 - Copiar el PID del proceso

El PID es el identificador del proceso.

En el ejemplo anterior, el PID es:

```text
5251
```

Debe copiar ese número porque será utilizado por el perfilador.

> **Nota:** Cada vez que ejecute el programa, el PID puede cambiar. No utilice siempre el mismo número.

---

## Paso 3 - Ejecutar Perfilador.py

Antes de presionar ENTER en la consola del programa principal, abra otra consola en el mismo folder raíz de `Pruebas_de_Rendimiento`.

Ejecute:

```bash
(.Fidelitas) ~S python Perfilador.py 5251 True
```

Donde:

```text
5251
```

debe reemplazarse por el PID que mostró su programa.

El valor:

```text
True
```

indica que se generará un archivo de resultados en el folder `Logs`.

---

## Paso 4 - Continuar el programa principal

Una vez que el perfilador esté corriendo, vuelva a la primera consola donde está `Alto_CPU.py`.

Luego presione ENTER.

El programa continuará su ejecución y el perfilador comenzará a recopilar información.

Cuando el programa termine, el perfilador también terminará automáticamente.

---

## Paso 5 - Revisar resultados

Se verá de esta forma:

![Resultados_Perfilador](./imgs/Resultados-Perfilador.png)

En el folder de **Logs** encontrará los resultados del perfilador.

![Resultados_Perfilador_Logs](./imgs/Resultados-Perfilador-Logs.png)

Los resultados se ven de la siguiente forma:

![Resultados_Perfilador_Logs_Line](./imgs/Resultados-Perfilador-Line.png)
![Resultados_Perfilador_Logs_CPU](./imgs/Resultados-Perfilador-CPU.png)

---

# Uso de Scalene en PC Windows

En caso de no utilizar el Raspberry PI físico, o si se está trabajando desde una máquina virtual o computadora personal con Windows, se debe utilizar esta sección.

Scalene en Windows permite analizar:

- Uso de CPU.
- Consumo de memoria.
- Líneas de código con mayor tiempo de ejecución.
- Generación de reportes en consola.
- Generación de reportes HTML.
- Generación de reportes JSON.

---

## Verificar versión de Scalene en Windows

Desde la raíz del repositorio, ejecute:

```bash
python -m scalene --version
```

Si la instalación fue correcta, debería aparecer la versión instalada.

---

## Perfilado en consola en Windows

La versión nueva de Scalene utiliza el comando `run`.

Desde la raíz del repositorio `Pruebas_de_Rendimiento`, ejecute:

```bash
C:\ python -m scalene run --cli -- .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
```

También puede ejecutarse de esta forma si el comando `scalene` está disponible en la terminal:

```bash
C:\ scalene run --cli -- .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
```

### Explicación del comando

```bash
python -m scalene
```

Ejecuta Scalene como módulo de Python.

```bash
run
```

Indica que se desea perfilar un programa.

```bash
--cli
```

Muestra el resultado directamente en consola.

```bash
.\Alto_Consumo_de_CPU\Alto_CPU.py
```

Indica la ruta del programa en Windows.

```bash
1000000
```

Indica la cantidad de ciclos u operaciones que ejecutará el programa.

---

## Generar perfil guardado en Windows

Para ejecutar el perfilado y guardar el resultado:

```bash
C:\ python -m scalene run .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
```

Scalene guardará el resultado en el archivo:

```text
scalene-profile.json
```

---

## Ver reporte guardado en consola en Windows

Después de generar el archivo `scalene-profile.json`, ejecute:

```bash
C:\ python -m scalene view --cli
```

Este comando mostrará en consola el perfil guardado.

---

## Ver reporte HTML en Windows

Para ver el reporte guardado en formato HTML:

```bash
C:\ python -m scalene view --html
```

Si desea hacerlo en dos pasos:

```bash
C:\ python -m scalene run .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
C:\ python -m scalene view --html
```

El reporte se abrirá en el navegador web.

---

## Reporte JSON en Windows

Con la versión nueva de Scalene, el archivo JSON se genera automáticamente al ejecutar:

```bash
C:\ python -m scalene run .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
```

El archivo generado por defecto será:

```text
scalene-profile.json
```

Este archivo puede utilizarse luego con:

```bash
C:\ python -m scalene view --cli
```

o:

```bash
C:\ python -m scalene view --html
```

---

# Uso de Perfilador en PC Windows

En caso de que el estudiante esté utilizando una máquina virtual o computadora personal, debe utilizar el perfilador para PC.

El perfilador para PC Windows se llama:

```text
Perfilador_PC.py
```

Este archivo se encuentra en la raíz del repositorio, al mismo nivel que:

```text
Perfilador.py
README.md
```

Esta herramienta funciona de forma similar al perfilador del RPI, utilizando las bibliotecas `py-spy` y `psutil` para obtener información de consumo de CPU y procesos desde la computadora personal.

---

## Paso 1 - Ejecutar el programa en Windows

Primero ejecute el programa a analizar desde la raíz del repositorio:

```bash
C:\ python .\Alto_Consumo_de_CPU\Alto_CPU.py 10000000
```

El programa mostrará un mensaje similar al siguiente:

```text
------------ Bienvenido al programa para probar consumo de CPU ------------
El PID del proceso es: 12540 - Este puede ser usado por el perfilador
Presione enter para continuar
```

---

## Paso 2 - Copiar el PID del proceso en Windows

El PID es el identificador del proceso.

En el ejemplo anterior, el PID es:

```text
12540
```

Debe copiar ese número para usarlo con `Perfilador_PC.py`.

> **Nota:** El PID cambia cada vez que se ejecuta el programa.

---

## Paso 3 - Ejecutar Perfilador_PC.py

Antes de presionar ENTER en la consola del programa principal, abra otra consola en el mismo folder raíz del proyecto.

Ejecute:

```bash
C:\ python Perfilador_PC.py 12540 True
```

Donde:

```text
12540
```

debe reemplazarse por el PID real mostrado por el programa.

---

## Paso 4 - Continuar el programa principal

Una vez iniciado el perfilador, vuelva a la consola del programa principal y presione ENTER.

El perfilador terminará automáticamente cuando el proceso monitoreado finalice.

---

## Paso 5 - Revisar resultados en Windows

Los resultados se almacenarán en el folder:

```text
Logs
```

Los archivos generados pueden abrirse posteriormente en:

- Microsoft Excel.
- LibreOffice Calc.
- Google Sheets.

---

# Procesado de Datos

El archivo se puede abrir en LibreOffice del RPI o en Excel si está trabajando desde Windows.

Se recomienda darle formato a la columna A haciendo click derecho y seleccionando **Format Cell** o **Formato de Celdas** en español.

![click_derecho_tiempo](./imgs/Click_derecho_tiempo.png)
![Configuracion_Tiempo](./imgs/Formato%20Tiempo.png)

Se puede usar LibreOffice para graficar al ir a:

```text
Insert >> Chart
```

Seleccione:

```text
X-Y (Scatter)
```

y el tipo:

```text
Lines-Only
```

Esto generará un gráfico con los valores de CPU vs Tiempo.

![Resultados_Perfilador_Logs_Chart](./imgs/Resultados-Perfilador-Logs-Chart.png)

![First_Row](./imgs/First_Row.png)

Por favor genere los gráficos de sus pruebas y guárdelos para presentar sus resultados.

**Nota:** Se recomienda agregar títulos y cambiar el nombre de las columnas por `Core_#`.

![Chart](./imgs/Chart.png)

Al hacer grande el gráfico se verá mejor.

**Nota:** Se recomienda cambiar la escala del eje Y a un máximo de 100 en las propiedades del gráfico.

![Chart_grande](./imgs/Chart_grande.png)

---

# Programas a Correr

Los programas de prueba se encuentran en:

```text
./Alto_Consumo_de_CPU/
./Alto_Consumo_de_Memoria/
```

---

## Nota Importante para Windows o Máquina Virtual

Si las pruebas se ejecutan desde una computadora personal o máquina virtual, se recomienda aumentar la cantidad de ciclos u operaciones para visualizar mejor el comportamiento del consumo de CPU y memoria, ya que la PC normalmente tiene mayor capacidad de procesamiento que el Raspberry PI.

Por ejemplo, si en Raspberry PI se utilizan:

```bash
1000000
```

en Windows se podrían utilizar valores mayores como:

```bash
10000000
```

o incluso:

```bash
100000000
```

dependiendo de la capacidad de la computadora.

---

## Alto_CPU.py

[Alto_CPU.py](./Alto_Consumo_de_CPU/Alto_CPU.py)

Este programa permite generar carga de CPU.

### Ejecución en Raspberry PI

```bash
(.Fidelitas) ~S python ./Alto_Consumo_de_CPU/Alto_CPU.py 10000000
```

### Ejecución en Windows

```bash
C:\ python .\Alto_Consumo_de_CPU\Alto_CPU.py 10000000
```

**Nota:** El `10000000` indica la cantidad de operaciones. Por favor ver la consigna de la semana 3 para verificar con qué valores se debe correr.

En Windows o máquina virtual puede aumentar este número si el programa termina muy rápido.

---

## Multiples_hilos_starvation.py

[Multiples_hilos_starvation.py](./Alto_Consumo_de_CPU/Multiples_hilos_starvation.py)

Este programa permite generar carga de CPU utilizando múltiples hilos.

### Ejecución en Raspberry PI

```bash
(.Fidelitas) ~S python ./Alto_Consumo_de_CPU/Multiples_hilos_starvation.py 8 10000000
```

### Ejecución en Windows

```bash
C:\ python .\Alto_Consumo_de_CPU\Multiples_hilos_starvation.py 8 10000000
```

**Nota:** El `8` indica la cantidad de hilos paralelos de ejecución y el `10000000` indica la cantidad de operaciones.

En Windows o máquina virtual puede aumentar el segundo valor si el programa termina muy rápido.

---

## Alto_Memoria.py

[Alto_Memoria.py](./Alto_Consumo_de_Memoria/Alto_Memoria.py)

Este programa permite generar consumo de memoria.

### Ejecución en Raspberry PI

```bash
(.Fidelitas) ~S python ./Alto_Consumo_de_Memoria/Alto_Memoria.py 1000000
```

### Ejecución en Windows

```bash
C:\ python .\Alto_Consumo_de_Memoria\Alto_Memoria.py 1000000
```

**Nota:** El `1000000` indica la cantidad de valores a almacenar.

En Windows o máquina virtual puede aumentar este número si el programa termina muy rápido, siempre teniendo cuidado de no consumir demasiada memoria.

---

# Uso de Sleep

```python
# Debe importar la siguiente librería en el código

import time

# Ejemplo de agregar wait a la función guardar_numeros_random() de Alto_Memoria.py

def guardar_numeros_random(cantidad: int = 1, num_random: list = []):
    for i in range(cantidad):
        num_random.append(random.random())
        time.sleep(0.001) # valor en segundos, el programa va a esperar 1 ms.
```

El uso de `time.sleep()` permite introducir pausas controladas en el programa, lo cual puede ayudar a observar mejor el comportamiento del consumo de CPU o memoria durante una prueba.

---

# Errores Comunes y Soluciones

## Error: ambiguous option --cpu

Si Scalene muestra un error similar a:

```text
ambiguous option: --cpu could match --cpu-only, --cpu-percent-threshold, --cpu-sampling-rate
```

significa que está usando una versión nueva de Scalene y el comando viejo ya no es compatible.

No utilice:

```bash
python -m scalene --cpu --memory --cli programa.py
```

Utilice:

```bash
python -m scalene run --cli programa.py
```

---

## Error: el perfilador no encuentra el PID

Verifique que:

1. El programa principal siga abierto.
2. No haya presionado ENTER antes de iniciar el perfilador.
3. El PID copiado sea correcto.
4. En Windows esté usando `Perfilador_PC.py`.
5. En Raspberry PI esté usando `Perfilador.py`.

---

## Error: el comando scalene no se reconoce

Si el comando:

```bash
scalene
```

no funciona, use:

```bash
python -m scalene
```

Por ejemplo:

```bash
python -m scalene run --cli .\Alto_Consumo_de_CPU\Alto_CPU.py 1000000
```

---

## Error: el programa termina muy rápido

Si el programa termina demasiado rápido y no se logra observar consumo de CPU o memoria, aumente el número de ciclos.

Por ejemplo, en lugar de:

```bash
1000000
```

puede usar:

```bash
10000000
```

o:

```bash
100000000
```

---

# Recomendaciones Finales

- Ejecute siempre los comandos desde la raíz del repositorio.
- Use `Perfilador.py` solamente en Raspberry PI.
- Use `Perfilador_PC.py` solamente en Windows o máquina virtual.
- Use la sintaxis nueva de Scalene con `run` y `view`.
- No utilice `--cpu --memory` con la versión nueva de Scalene.
- Guarde capturas de pantalla de los resultados.
- Genere gráficos para evidenciar el comportamiento de CPU y memoria.
- Revise el folder `Logs` después de ejecutar los perfiladores.
- Si trabaja en PC, puede aumentar la cantidad de ciclos para obtener resultados más visibles.
