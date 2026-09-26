# Proyecto 1 AED 2026-1
El proyecto busca presentar el funcionamiento de la estructura de datos **Tabla Hash** mediante la animación de un video con un máximo de 2 minutos de duración con el uso de la Biblioteca `Manim` para Python 11 desarrollado por el canal de Youtube [https://www.3blue1brown.com/](https://www.3blue1brown.com/)

| Integrante | Codigo |
| --- | --- |
| Zavaleta Alvino, Roger | 202010438 |
| Aquino Reyna, Jesus Emmanuel |  |
| Mendoza Palacios, Gracia Luz |  |

## Funcionalides a explicar:

-   Creación de la tabla hash.
-   Uso de las Operaciones de Inserción, Busqueda y Eliminación.
-   El funcionamiento interno de la tabla hash al realizar las operaciones.
-   El manejo de colisiones dentro de la tabla hash.

## Acerca de la estructura de datos a presentar


## Instrucciones de compilación

Se requiere el uso del siguente software:
-   Python  [(ultima version disponible)](https://www.python.org/downloads/)
-   uv
-   Manim [(main page)](https://pypi.org/project/manim/)

### Paso 1: instalar uv:
Ejecutar el siguente código en powershell para instalar uv:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
### Paso 2: instalar python y manim:
Ejecutar el siguente código en el directorio donde se encuentra descargado el repositorio para instalar python y manim:
```
uv python install
uv add manim
```
### Paso 3: Compilar video:
Ejecutar el siguente código en el directorio donde se encuentra descargado el repositorio para generar el video
```
manim 
manim -pql hash_table.py AnimacionHashTable
```
