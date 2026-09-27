# Tabla hash con separate chaining

Este proyecto implementa una tabla hash genérica en C++ usando **separate chaining**
(encadenamiento separado) para resolver colisiones. El programa de prueba ejecuta
varias operaciones, genera un registro en `trace.json` y una escena de Manim usa
ese registro para crear una animación de la tabla.

## Contenido del proyecto

- `Hash_table.h`: implementación de `Hash_table<Key, Value, HashPolicy>`.
- `main.cpp`: programa de demostración y generador de `trace.json`.
- `trace.json`: eventos producidos por la última ejecución del programa C++.
- `hash_table.py`: escena `AnimacionHashTable` de Manim.
- `CMakeLists.txt`: configuración de compilación con CMake.
- `media/`: videos y archivos intermedios generados por Manim.

## Cómo funciona la tabla

Cada clave se transforma en un índice mediante la política `DivisionHash`:

```text
indice = hash(clave) % capacidad
```

Cada posición de la tabla apunta al comienzo de una lista enlazada de nodos.
Cada nodo almacena una clave, su valor y el siguiente nodo de la misma lista.
Cuando dos claves producen el mismo índice, ambas se guardan en ese bucket y se
recorren mediante la lista enlazada.

La clase ofrece estas operaciones:

- `insert(key, value)`: inserta una clave o actualiza su valor si ya existe.
- `search(key)`: devuelve un puntero al valor encontrado o `nullptr`.
- `remove(key)`: elimina una clave y devuelve si la operación tuvo éxito.
- `contains(key)`, `empty()` y `size()`: consultas sobre el contenido.
- `bucketSize(index)`: cantidad de elementos en un bucket.
- `getCapacity()`, `getK()`, `getFillFactor()` y `getMaxFillFactor()`:
	consultas de configuración y carga.
- `print()`: imprime la tabla completa en la consola.

La tabla se crea inicialmente con capacidad `5`, `k = 3` y factor de carga
máximo `0.5`. Antes de insertar un elemento nuevo se calcula la carga proyectada:

```text
(elementos actuales + 1) / (capacidad * k)
```

Si supera el factor máximo, se duplica la capacidad y se realiza un **rehash**:
se crean nuevos buckets y se vuelven a insertar todos los nodos con sus nuevos
índices.

## Generar la traza con C++

Se necesita un compilador C++17 y CMake 3.20 o superior.

```bash
cmake -S . -B build
cmake --build build
./build/proyecto_1
```

La ejecución escribe `trace.json` en la carpeta del proyecto y también muestra
la tabla final en la consola. El ejemplo incluye inserciones, una actualización,
búsquedas existentes y no existentes, consultas, eliminaciones y un rehash al
ampliar la capacidad de 5 a 10.

## Generar el video con Manim

Desde la carpeta raíz del proyecto, crea y activa un entorno virtual e instala
Manim:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install manim
```

Después de generar `trace.json`, con el entorno activado ejecuta:

```bash
manim -pql hash_table.py AnimacionHashTable
```

También se puede ejecutar sin activar el entorno:

```bash
.venv/bin/manim -pql hash_table.py AnimacionHashTable
```

Opciones útiles:

- `-p`: abre el video al terminar el renderizado.
- `-q l`: usa calidad baja (`480p15`) para hacer pruebas rápidas.
- Para un video final de mayor calidad, usa por ejemplo `-pqh` o `-pqk`.

El video se guarda normalmente dentro de `media/videos/hash_table/`. La escena
lee los eventos de `trace.json` en orden, dibuja los buckets, muestra cada nodo
encadenado y colorea temporalmente el bucket afectado. Las búsquedas indican
éxito en verde y fallo en rojo.

### Duración mínima

`AnimacionHashTable` tiene una duración mínima de **120 segundos (2 minutos)**.
Al terminar de mostrar los eventos, consulta el tiempo acumulado del renderer y
espera únicamente lo que falta para alcanzar los 120 segundos. Por ello, incluso
si `trace.json` contiene pocos eventos, el video no termina antes de dos minutos.

## Flujo completo

```text
Hash_table.h + main.cpp
					|
					| ./build/proyecto_1
					v
			trace.json
					|
					| manim hash_table.py AnimacionHashTable
					v
			 video MP4
```

Para volver a generar una animación con datos nuevos, modifica las operaciones
de `main.cpp`, recompila, ejecuta `./build/proyecto_1` y vuelve a lanzar Manim.
No es necesario editar manualmente `trace.json`.