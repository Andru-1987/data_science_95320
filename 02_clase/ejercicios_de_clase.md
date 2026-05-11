##  Ejercicio: Análisis de calificaciones de estudiantes

### Contexto
Tienes un conjunto de datos con las calificaciones (notas) de varios estudiantes en tres materias: Matemáticas, Ciencias y Lectura. Las notas están en una lista de diccionarios. Tu tarea es limpiar los datos, transformarlos y calcular el promedio de cada estudiante y la materia más alta.

### Objetivos de aprendizaje
- Usar **list comprehensions** y **unpacking** para procesar datos de forma idiomática.
- Comprender la **mutabilidad** (modificar una lista in-place vs. crear una nueva).
- Escribir **funciones modulares** y conectarlas en un **pipeline**.
- Aplicar **enumerate** para trabajar con índices cuando sea útil.

### Datos de ejemplo (proporcionados)
```python
# Opcional -> mostrar por caso de uso en google spreadsheet


datos_crudos = [
    {"nombre": "Ana", "matematicas": 85, "ciencias": 90, "lectura": 78},
    {"nombre": "Luis", "matematicas": "n/a", "ciencias": 88, "lectura": 92},
    {"nombre": "Marta", "matematicas": 95, "ciencias": 85, "lectura": 87},
    {"nombre": "Jorge", "matematicas": 70, "ciencias": 75, "lectura": 80},
    {"nombre": "Carla", "matematicas": 88, "ciencias": 92, "lectura": "n/a"},
]
```

### Instrucciones

#### 1. Limpieza de datos (función modular)
Escribe una función `limpiar_nota(valor)` que:
- Convierta a entero si el valor es un número (entero o flotante).
- Si el valor es `"n/a"` (string), lo reemplace por `0`.
- Si es otro tipo, lo convierta a entero si es posible, o ponga `0` por defecto.

> **Nota sobre mutabilidad**: ¿Debemos modificar los diccionarios originales o crear copias? Piensa en las consecuencias.

#### 2. Transformación (list comprehension idiomática)
Crea una nueva lista `datos_limpios` aplicando la función `limpiar_nota` a cada valor numérico de cada registro.  
**Requisito**: Usa una **list comprehension** anidada (o comprensión de diccionarios) para hacerlo en una sola expresión elegante.

#### 3. Añadir promedio por estudiante
Escribe una función `calcular_promedio(registro)` que reciba un diccionario (con las notas ya limpias) y devuelva un nuevo diccionario igual más una clave `"promedio"` con el promedio de las tres materias.  
Luego, usa `map` o una list comprehension para aplicar esta función a todos los registros.

#### 4. Encontrar la materia más alta (uso de enumerate y unpacking)
Escribe una función `mejor_materia(registro)` que reciba el diccionario (sin contar `"nombre"` ni `"promedio"`) y devuelva el nombre de la materia con mayor nota.  
**Ayuda**: puedes usar `max()` con un argumento `key` y `dict.items()`. Muestra también cómo podrías hacerlo sin `max()` usando `enumerate` y un bucle.

#### 5. Pipeline completo
Construye un pipeline (una función o secuencia de llamadas) que haga todo el proceso:
- Limpiar datos.
- Calcular promedios.
- Agregar la mejor materia.
- Mostrar los primeros 3 resultados ordenados por promedio descendente.

El pipeline debe ser fácil de leer y modificar, usando las funciones que definiste.

#### 6. Reflexión sobre mutabilidad (pregunta teórica)
¿Qué pasa si modificas la lista `datos_crudos` directamente dentro de la limpieza? ¿Y si trabajas con una copia? Explica con tus palabras la diferencia entre tipos mutables e inmutables en este contexto.

---

## Solucion propuesta

### 1. Función de limpieza
```python
def limpiar_nota(valor):
    if valor == "n/a":
        return 0
        
    return int(valor)
```

### 2. Transformación con list comprehension
```python

def limpieza_registro(registro):
    
    registro_a_limpiar = registro.copy()
    
    for k,v in registro_a_limpiar.items():
        if k != "nombre":
            registro_a_limpiar[k] = limpiar_nota(v)
    
    return registro


datos_limpios = [limpieza_registro(registro) for registro in datos_crudos]
```

### 3. Calcular promedio

```python
def calcular_promedio(registro):

    nuevo = registro.copy()

    notas = []

    for k, v in nuevo.items():
        if k != "nombre":
            notas.append(v)

    nuevo["promedio"] = round(sum(notas) / len(notas), 1)

    return nuevo
```

### 4. Mejor materia usando max

```python
def mejor_materia(registro):
    
    mejor = ""
    nota_max = -1

    for materia in registro:
        if materia != "nombre" and materia != "promedio":
            if registro[materia] > nota_max:
                nota_max = registro[materia]
                mejor = materia

    return mejor
```


### 5. Pipeline
```python
def pipeline_completo(datos):

    # Paso 1:
    # Limpiar los registros.
    # Convierte "n/a" en 0 y transforma las notas a enteros.
    limpios = [limpieza_registro(reg) for reg in datos]

    # Paso 2:
    # Calcular el promedio de cada estudiante.
    # Agrega la clave "promedio" a cada registro.
    con_promedio = [calcular_promedio(reg) for reg in limpios]

    # Paso 3:
    # Buscar la materia con mejor nota de cada estudiante.
    # Agrega la clave "mejor_materia".
    for reg in con_promedio:
        reg["mejor_materia"] = mejor_materia(reg)

    # Paso 4:
    # Ordenar los estudiantes por promedio de mayor a menor.
    # Luego devolver solo los primeros 3.
    con_promedio.sort(key=lambda x: x["promedio"], reverse=True)
    
    return con_promedio[:3]

```

### 6. Reflexión sobre mutabilidad
- **Mutables** (listas, diccionarios): si modificamos el diccionario original dentro de la función de limpieza, los cambios afectan a la lista original. Eso puede ser deseable para ahorrar memoria, pero peligroso si necesitamos conservar los datos crudos.
- **Inmutables** (enteros, strings, tuplas): cualquier operación genera un nuevo objeto. En este ejercicio, si reemplazamos el valor `"n/a"` por un entero, estamos reasignando la clave en el diccionario. El diccionario es mutable, pero los valores internos pueden ser reemplazados.
- **Buena práctica**: trabajar sobre una copia profunda si no se quiere alterar el original. En data science, normalmente se preservan los datos crudos y se generan nuevas estructuras.
