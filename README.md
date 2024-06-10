# Pruebas_de_Rendimiento

Este es el repositorio del curso para realizar pruebas de Validación de Sistemas Embebidos TSEV-008 del programa de Técnico en Sistemas Embebidos de la Universidad Fidélitas.

## Configurando RPI

Siga las instrucciones en el repositorio de la Máquina de Café [Proyecto final del curso] para configurar su RPI.

1. [Configurar RPI](https://github.com/rscd27p/Maquina_de_Cafe/blob/main/Documentos/Configurar_RPI.md)
2. [Sección - Instalación de Software en Raspberry PI](https://github.com/rscd27p/Maquina_de_Cafe/tree/main)

**Nota Importante:**  Se usa la misma nomenclatura para las consolas del Host y del RPI.

En el caso de la consola que corre en la computadora personal de Windows va a ser identificada de la siguiente forma:

```
C:\ <Comando> --parametro-1 --parametro-2
```
La consola en el RPI se identifica como:

```
~S <Comando> --parametro-1 --parametro-2
```

Para el ambiente "Fidelitas" en el RPI:

```
(.Fidelitas) ~S <Comando> --parametro-1 --parametro-2
```

### Instalación de Bibliotecas.

Adicional a esto se utilizaran las siguientes bibliotecas como parte del Ambiente Virtual llamado "Fidelitas" creado en la sección de instalación de software. Para esto ejecute el los siguientes comandos.

**Nota:** Vaya a la ubicación donde esta el ambiente virtual de Fidelitas en su Raspberry PI, por ejemplo, por defecto en la guia se instaló en root.

```
(.Fidelitas) ~S python -m pip install py-spy scalene
```

##