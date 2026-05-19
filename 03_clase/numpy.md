## Numpy 

El archivo corresponde al **Índice y Material Didáctico de un Curso Mejorado de NumPy (Numerical Python) desde Cero**. Está orientado a la preparación en Data Science, analizando los fundamentos de la librería, el mecanismo de *Broadcasting*, operaciones vectorizadas, funciones estadísticas aplicadas y buenas prácticas de optimización.

---

## Resumen del Contenido

NumPy es la librería central y la base fundamental para la computación numérica y el ecosistema científico de Python. Su estructura principal es el `ndarray` (array N-dimensional) , el cual destaca frente a las listas nativas de Python por ser homogéneo (mismo tipo de datos) y ocupar bloques contiguos en memoria , permitiendo operaciones matemáticas vectorizadas que evitan bucles y alcanzan velocidades de ejecución hasta 100 veces mayores.

### Puntos Destacados del Aprendizaje:

* **Instalación y Entorno:** Se detallan métodos de instalación estándar mediante `pip` o entornos virtuales de `Anaconda`, recordando que la librería requiere Python 3.8 o superior y viene preinstalada en Google Colab.


* **Creación y Propiedades:** Permite generar arrays desde listas o mediante funciones predefinidas (`np.zeros`, `np.ones`, `np.eye`, `np.arange`, arrays aleatorios). Sus propiedades críticas a inspeccionar son `shape` (forma), `dtype` (tipo de dato), `size` (tamaño total) y `ndim` (dimensiones).


* **Indexing, Slicing y Memoria:** Explica el acceso multidimensional. Es crucial entender que el *slicing* genera **vistas** (modificar el corte altera el array original) , por lo que se requiere el método `.copy()` si se desea un subconjunto independiente.


* **Mecanismo de Broadcasting:** Permite operar aritméticamente con arrays de diferentes dimensiones sin duplicar datos físicamente en memoria. Las dimensiones se comparan de derecha a izquierda y deben ser iguales, ser 1 o no existir. En caso de incompatibilidad, se resuelve estratégicamente mediante transformaciones con `reshape` o `np.newaxis`.


* **Análisis Estadístico y Visualización:** Incluye un set de funciones optimizadas (`np.mean`, `np.median`, `np.std`, percentiles) que pueden aplicarse a todo el bloque o a lo largo de un eje específico (`axis=0` para columnas, `axis=1` para filas). Además, se integra de forma nativa con *Matplotlib* para la generación de histogramas, diagramas de caja (Box Plots) y gráficos de dispersión.

---

## 1. Arrays vs. Listas: Diferencia de Eficiencia y Sintaxis

Los arrays de NumPy permiten realizar operaciones vectorizadas (elemento a elemento) directamente, mientras que las listas de Python requieren bucles explícitos o comprensiones de listas, lo que resulta mucho más lento e ineficiente.

```python
import numpy as np

# --- Enfoque con Listas de Python ---
lista = [1, 2, 3, 4, 5]
# Para multiplicar cada elemento por 2, necesitamos un bucle
resultado_lista = [x * 2 for x in lista]
print("Resultado Lista:", resultado_lista)

# --- Enfoque con Arrays de NumPy (Vectorizado) ---
array = np.array([1, 2, 3, 4, 5])
# Operación directa sobre todo el bloque de memoria contiguo
resultado_array = array * 2
print("Resultado Array:", resultado_array)

```

---

## 2. Creando Arrays con Propósito

NumPy provee diferentes funciones optimizadas para inicializar estructuras de datos según la necesidad (llenar con ceros, unos, rangos o valores aleatorios).

```python
import numpy as np

# Matriz de ceros de 3x3 de tipo entero
matriz_ceros = np.zeros((3, 3), dtype=int)

# Rango numérico del 0 al 9 (equivalente al range de Python)
rango = np.arange(10)

# Matriz identidad de 3x3
identidad = np.eye(3)

print("Ceros:\n", matriz_ceros)
print("Rango:", rango)
print("Identidad:\n", identidad)

```

---

## 3. Propiedades Clave de los Arrays

Antes de operar con los datos, es fundamental inspeccionar sus atributos para asegurar la compatibilidad matemática.

```python
import numpy as np

numatriz = np.array([[1, 2, 3], [4, 5, 6]])

print("Forma (filas, columnas):", matriz.shape)  # Retorna (2, 3)
print("Tipo de datos interno:", matriz.dtype)   # Retorna int64 (o int32)
print("Cantidad total de elementos:", matriz.size) # Retorna 6
print("Número de dimensiones:", matriz.ndim)    # Retorna 2

```

---

## 4. Indexing y Slicing (Vistas vs. Copias)

El particionado (*slicing*) en NumPy genera **vistas** de los datos para ahorrar memoria. Si necesitas modificar un subconjunto sin alterar el array original, debes forzar una **copia**.

```python
import numpy as np

# --- Comportamiento de una Vista ---
original = np.array([1, 2, 3, 4, 5])
vista = original[0:3]  # Genera una vista lógica
vista[0] = 99          # Al modificar la vista...

print("Original modificado por la vista:", original)  # [99, 2, 3, 4, 5]

# --- Comportamiento de una Copia ---
a = np.array([1, 2, 3, 4, 5])
copia = a[0:3].copy()  # Crea un bloque independiente en memoria
copia[0] = 888         # Solo modifica la copia

print("Original intacto:", a)      # [1, 2, 3, 4, 5]
print("Copia modificada:", copia)  # [888, 2, 3]

```

---

## 5. Mecanismo de Broadcasting

El *broadcasting* extiende conceptualmente las dimensiones de un array menor para que sea matemáticamente compatible con uno mayor, optimizando el uso de memoria.

```python
import numpy as np

# Matriz de 3x3
A = np.array([[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 9]])

# Vector de tamaño 3 (1 dimensión)
v = np.array([10, 20, 30])

# NumPy expande virtualmente 'v' en 3 filas para sumarlo a cada fila de 'A'
resultado = A + v
print("Resultado del Broadcasting:\n", resultado)

```

---

## 6. Soluciones a Errores Comunes de Broadcasting (`reshape` / `newaxis`)

Si intentas operar dos estructuras cuyas dimensiones no coinciden ni cumplen las reglas de comparación de derecha a izquierda, se lanzará un error de valor. La solución es ajustar sus ejes.

```python
import numpy as np

matriz_3x2 = np.array([[1, 2], [3, 4], [5, 6]])  # Formato (3, 2)
vector_3 = np.array([10, 20, 30])                # Formato (3,)

# Solución: Añadir una dimensión virtual al vector para transformarlo de (3,) a (3, 1)
vector_columna = vector_3[:, np.newaxis] 

resultado_ajustado = matriz_3x2 + vector_columna
print("Resultado ajustado con newaxis:\n", resultado_ajustado)

```

---

## 7. Operaciones Matemáticas y Vectorizadas

NumPy cuenta con funciones universales matemáticas preparadas para trabajar directamente a nivel de registros de la CPU de forma optimizada.

```python
import numpy as np

valores = np.array([1, 4, 9, 16, 25])

# Aplicar raíz cuadrada a todos los elementos simultáneamente
raices = np.sqrt(valores)

# Logaritmo natural
logaritmos = np.log(valores)

print("Raíces:", raices)         # [1., 2., 3., 4., 5.]
print("Logaritmos:", logaritmos) # [0., 1.386, 2.197, ...]

```

---

## 8. Funciones Estadísticas y el Parámetro `axis`

Las métricas descriptivas pueden evaluar el total del array de manera plana, o colapsar dimensiones específicas orientándose por columnas (`axis=0`) o por filas (`axis=1`).

```python
import numpy as np

# Matriz de calificaciones de ejemplo (3 alumnos, 3 materias cada uno)
notas = np.array([[5, 2, 9],
                  [1, 3, 7],
                  [8, 4, 6]])

# 1. Media global de todos los exámenes realizados
media_total = np.mean(notas)

# 2. Promedio por MATERIA (Colapsar verticalmente las filas -> axis=0)
media_por_materia = np.mean(notas, axis=0)

# 3. Promedio por ALUMNO (Colapsar horizontalmente las columnas -> axis=1)
media_por_alumno = np.mean(notas, axis=1)

print("Media Global:", media_total)         # 5.0
print("Media por Materia:", media_por_materia) # [4.67, 3.  , 7.33]
print("Media por Alumno:", media_por_alumno)   # [5.33, 3.67, 6.  ]

```

---

## 9. Análisis Estadístico Aplicado con Máscaras Booleanas

Puedes evaluar condiciones lógicas vectorizadas sobre los arrays y usarlos para filtrar, contar o extraer elementos rápidamente.

```python
import numpy as np

clase_a = np.array([65, 78, 82, 90, 45, 88, 75, 95, 64, 70])

# Generar una máscara booleana (True para los aprobados con nota >= 70)
mascara_aprobados = (clase_a >= 70)

# Contar cuántos estudiantes aprobaron (True equivale numéricamente a 1)
total_aprobados = np.sum(mascara_aprobados)
print(f"Aprobados: {total_aprobados} de {len(clase_a)}") # 7 de 10

```

## Cargar informacion desde un archivo CSV desde GoogleSheet

```python
import numpy as np

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSrBmOZLnrVcUxSAakGgU-hp24fPt0DDty8OyeBJdHUOip3fdOxSQfCg7Hedw2fSSvMphyYPu4J0NgK/pub?gid=0&single=true&output=csv"

# Cargar los datos desde la URL, ignorando la cabecera y usando comas como delimitador 
# Sin embargo, vemos que asume que son todos numeros. 
data_numpy = np.genfromtxt(url, delimiter=",", skip_header=1)

# Si queremos cargar los datos con los nombres de las columnas, podemos usar dtype=None y names=True
data = np.genfromtxt(url, delimiter=",", dtype=None, names=True, encoding='utf-8')

print(data_numpy)
print(data)


# Slicing the two last columns
data_sliced = data[['Tax','Total']]

# Stack the extracted columns vertically
matrix_2x100 = np.vstack([data['Tax'], data['Total']])

print(matrix_2x100.shape)

# --- 1. Basic Aggregations ---
# Sum of all elements in the matrix
total_sum = np.sum(matrix_2x100)         

# Lowest and highest values across both Tax and Total
overall_min = np.min(matrix_2x100)       
overall_max = np.max(matrix_2x100)       

# --- 2. Central Tendency (Using axis=1 to separate Tax and Total) ---
# Arithmetic averages
# Output will be: [mean_of_tax, mean_of_total]
mean_vals = np.mean(matrix_2x100, axis=1)     

# Middle values (50th percentile)
median_vals = np.median(matrix_2x100, axis=1) 


# --- 3. Dispersion / Variability (Using axis=1) ---
# Standard deviations
std_devs = np.std(matrix_2x100, axis=1)       

# Variances
variances = np.var(matrix_2x100, axis=1)      


# --- 4. Percentiles (Using axis=1) ---
# 25th percentile (1st quartile)
p25_vals = np.percentile(matrix_2x100, 25, axis=1) 

# 75th percentile (3rd quartile)
p75_vals = np.percentile(matrix_2x100, 75, axis=1) 


# --- Print Results Safely ---
print("--- Central Tendency ---")
print(f"Mean (Tax, Total):    {mean_vals}")
print(f"Median (Tax, Total):  {median_vals}")

print("\n--- Dispersion ---")
print(f"Std Dev (Tax, Total): {std_devs}")
print(f"Variance (Tax, Total):{variances}")

print("\n--- Percentiles ---")
print(f"25th Percentile:      {p25_vals}")
print(f"75th Percentile:      {p75_vals}")

```
