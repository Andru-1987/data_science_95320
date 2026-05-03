# Python Semana 2

### 1. Estilo y buenas prácticas en Python
- **PEP 8**: indentación (4 espacios), líneas máximas 79 caracteres, nombres `snake_case` para variables/funciones, `CamelCase` para clases.
- **Patrones idiomáticos**:
  - *List comprehensions*: `[x**2 for x in range(10)]`
  - *Unpacking*: `a, b = (1, 2)` o `func(*lista)`
  - *Context managers*: `with open(...) as f:`
- **Mutabilidad**: `list`, `dict`, `set` son mutables; `int`, `str`, `tuple` son inmutables. El aliasing puede causar efectos secundarios inesperados.

### 2. NumPy – arreglos y rendimiento
- **ndarray**: estructura homogénea, eficiente en memoria.
- Atributos: `shape`, `dtype`, `size`, `ndim`.
- **Operaciones vectorizadas**: evitan bucles explícitos en Python.
- **Broadcasting**: operaciones entre arrays de diferentes dimensiones.

### 3. Pandas – manipulación de datos tabulares
- **Series** (1D) y **DataFrame** (2D).
- Carga de datos: `pd.read_csv()`, `pd.read_json()`.
- Selección: `df['col']`, `df.loc[]`, `df.iloc[]`.
- Transformaciones: `groupby()`, `merge()`, manejo de nulos (`dropna`, `fillna`).
### 4. Control de flujo avanzado
- Condicionales anidados y operador ternario.
- `enumerate()` para iterar con índice.
- **Generadores** (`yield`) para trabajar con flujos de datos grandes.
- Módulo `itertools`: `cycle`, `chain`, `islice`.

### 5. Visualización de datos
- **Matplotlib** – control fino, múltiples figuras.
- **Seaborn** – sintaxis simplificada, gráficos estadísticos.
- **Plotly** – gráficos interactivos, exportación a HTML.
- Elementos esenciales: título, etiquetas de ejes, leyenda.

### 6. Funciones avanzadas
- **Argumentos variables**: `*args` (posicionales) y `**kwargs` (nominales).
- **Closures**: funciones que recuerdan el estado de su entorno exterior.

### 7. Testing ligero y depuración
- Depuración con `print()` o `pdb`.
- **`assert`** para pruebas unitarias simples.
- Casos borde: listas vacías, valores negativos, tipos incorrectos.

### 8. Estadística descriptiva y EDA
- Medidas de tendencia central: media, mediana, moda.
- Medidas de dispersión: varianza, desviación estándar, rango intercuartílico (IQR).
- Cuartiles y percentiles.
- Distribuciones: normal (campana) y uniforme.
- Análisis exploratorio (EDA): resumir datos con `.describe()`, detectar outliers.


### 9. Pipelines reproducibles y mini-proyecto
- Estructurar el código en funciones modulares y puras.
- Documentar con docstrings.
- Guardar resultados intermedios (CSV, gráficos).
- Usar control de versiones (git) para colaboración.

---

## Uso de Yield -> Una herramienta poco valorada.

### Ventaja de `yield` frente a Pandas (sin chunks)

Pandas está optimizado para operaciones vectorizadas en RAM, pero **carga todo el archivo de una vez**. Si tu archivo CSV pesa 10 GB y tienes 8 GB de RAM, el programa colapsará.

El enfoque con `yield` lee **una línea a la vez** (o un lote pequeño) y **nunca guarda todos los datos en memoria**. La memoria usada es constante (unas pocas MB).

**Comparación directa:**

| Método | Memoria máxima | Velocidad | Facilidad de código |
|--------|---------------|-----------|---------------------|
| `pd.read_csv('gigante.csv')` | Tamaño del archivo (∼10 GB) | Muy rápida (vectorizada) | Alta |
| `leer_csv_linea_a_linea` + `yield` (Python puro) | ∼línea (KB) | Lenta (Python puro) | Media |
| **Chunks con Pandas + `yield`** | Tamaño del chunk (ej. 100 MB) | Rápida (vectorizada por chunk) | Alta |

La solución óptima para archivos gigantes es usar el **argumento `chunksize` de Pandas**, que ya retorna un generador, y luego aplicar operaciones vectorizadas a cada chunk.

## Cómo usar `yield` con un archivo gigante sin que se rompa (combinando Pandas)

Aquí tienes un pipeline modular que procesa un CSV enorme por chunks, usando Pandas para la limpieza y normalización, y `yield` para ir entregando los resultados chunk a chunk.

### Ejemplo completo

```python
import pandas as pd
import numpy as np

def leer_csv_por_chunks(ruta_archivo, chunksize=10000):
    """Generador que lee el CSV en fragmentos (chunks)"""
    for chunk in pd.read_csv(ruta_archivo, chunksize=chunksize):
        yield chunk

def limpiar_nulos_pandas(iterador_chunks):
    """Recibe chunks y elimina filas con nulos o cadenas vacías"""
    for chunk in iterador_chunks:
        # Reemplazar cadenas vacías por NaN y luego dropna
        chunk = chunk.replace(r'^\s*$', np.nan, regex=True)
        chunk = chunk.dropna()
        if not chunk.empty:
            yield chunk

def normalizar_edad_pandas(iterador_chunks, columna_edad='edad'):
    """Normaliza la columna de edad en cada chunk"""
    for chunk in iterador_chunks:
        if columna_edad in chunk.columns:
            # Normalización (media 25, desvío 10) - ajusta según tus datos
            chunk['edad_normalizada'] = (chunk[columna_edad] - 25) / 10
        yield chunk

# Uso del pipeline
archivo_gigante = 'personas_100millones.csv'

chunks_brutos = leer_csv_por_chunks(archivo_gigante, chunksize=50000)
chunks_limpios = limpiar_nulos_pandas(chunks_brutos)
chunks_normalizados = normalizar_edad_pandas(chunks_limpios, columna_edad='edad')

# Procesar cada chunk resultante (por ejemplo, guardar o entrenar modelo)
for i, chunk in enumerate(chunks_normalizados):
    print(f"Procesando chunk {i+1} con {len(chunk)} filas")
    # Aquí podrías:
    # - Guardar chunk limpio a disco (parquet, csv)
    # - Acumular estadísticas parciales
    # - Entrenar un modelo en mini-batches
    # - Enviar a una base de datos
```

### ¿Qué ventaja tangible tiene esto?

1. **Memoria estable** – Sin importar si el archivo es 10 GB o 1 TB, la memoria usada es aproximadamente `chunksize * tamaño_fila`. En el ejemplo, 50 000 filas * 1 KB ≈ 50 MB.

2. **Velocidad** – Cada chunk se procesa con operaciones vectorizadas de Pandas (rápidas en C), no con bucles Python lentos.

3. **Modularidad** – Puedes agregar/eliminar etapas (como `limpiar_nulos_pandas`, `normalizar_edad_pandas`, etc.) sin afectar al resto. Cada etapa es un generador que recibe y devuelve chunks.

4. **Fallos controlados** – Si falla el chunk 42, ya procesaste los 41 anteriores. No pierdes todo el trabajo.

## ¿Entonces cuándo usar el primer enfoque (Python puro línea por línea)?

El código que pusiste al principio (`leer_csv_linea_a_linea`, `if None not in fila...`) es útil pero tiene limitaciones:

- **Lento** porque cada línea se manipula en Python puro.
- **Poco práctico** si necesitas operaciones complejas (agrupar, unir, ventanas temporales).

Lo recomiendo solo para:
- Archivos **enormes** (cientos de GB) donde incluso un chunk de Pandas de 10 000 filas sea demasiado (caso muy extremo).
- Datos **no tabulares** (logs, JSON líneas).
- Cuando no puedes usar Pandas por restricciones del entorno.

## Advertencia importante sobre el código original

Tu función `limpiar_nulos` verifica `None not in fila and '' not in fila`. Eso descarta filas donde **cualquier** campo sea `None` o `''`. Puede ser demasiado agresivo (pierdes muchas filas). Con Pandas puedes hacer `dropna(subset=['columna_especifica'])` para eliminar solo nulos en columnas críticas.

## Conclusión práctica para tu clase

- Enseña `yield` como **herramienta para trabajar con datos que no caben en memoria**.
- Muestra el **patrón chunk + Pandas** como el estándar de la industria para archivos grandes.
- Destaca que los generadores permiten **pipelines de datos eficientes** y reutilizables.