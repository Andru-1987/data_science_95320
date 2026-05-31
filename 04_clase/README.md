# Unidad 4 -Data Science I

## Temas principales

- Manejo de datos nulos (missing values)
- Series de tiempo en Pandas
- Manipulacion de DataFrames
- Visualizacion con Matplotlib

---

## Contenido teorico

### Manejo de datos nulos

Los datos nulos representan uno de los problemas mas frecuentes en ciencia de datos. Muchos algoritmos de machine learning no pueden procesar valores faltantes, lo que obliga a tratarlos antes de cualquier analisis.

**Origenes comunes:**
- Fallas en sensores o equipos de medicion
- Errores en esquemas de muestreo
- Respuestas omitidas en encuestas
- Defectos en sistemas de captura de datos

**Estrategias de imputacion:**

| Estrategia | Descripcion | Cuando usarla |
|---|---|---|
| Media | Reemplaza por el promedio de la columna | Datos numericos con distribucion simetrica |
| Mediana | Reemplaza por el valor central | Datos con outliers o distribucion sesgada |
| Moda | Reemplaza por el valor mas frecuente | Variables categoricas |
| Constante | Valor fijo (ej: "Desconocido") | Cuando se quiere preservar la ausencia como informacion |

En Python se puede implementar manualmente con Pandas (`fillna`) o mediante `SimpleImputer` de Scikit-learn, que automatiza el proceso y facilita integrarlo en pipelines de produccion.

---

### Series de tiempo

Las series de tiempo son conjuntos de datos donde cada observacion esta asociada a un momento especifico. El tiempo no es solo un atributo mas: es el eje estructural que da sentido a los valores.

**Tipos de datos temporales en Pandas:**

| Concepto | Representa | Objeto Pandas |
|---|---|---|
| Timestamp | Un punto exacto en el tiempo | `Timestamp` / `DatetimeIndex` |
| Periodo | Un intervalo con inicio y fin | `Period` / `PeriodIndex` |
| Duracion | Cantidad de tiempo transcurrido | `Timedelta` / `TimedeltaIndex` |

**Operaciones fundamentales:**
- Conversion de strings a fechas: `pd.to_datetime()`
- Generacion de rangos: `pd.date_range()`, `pd.period_range()`
- Cambio de frecuencia: parametro `freq` ('D' para dias, 'M' para meses, etc.)
- Aritmetica temporal: restar timestamps para obtener duraciones, convertir a periodos para contar intervalos

---

### Visualizacion con Matplotlib

Matplotlib es la libreria base para graficos en Python. Trabaja con dos enfoques:

1. **Interfaz orientada a objetos:** Se crean explicitamente figuras (`Figure`) y ejes (`Axes`), lo que permite control total sobre cada elemento visual. Es el metodo recomendado para graficos complejos o que requieren reutilizacion.

2. **Interfaz pyplot:** Comandos de estilo MATLAB, mas rapida para exploracion pero con menos control.

**Elementos clave para enriquecer graficos:**
- `axhline` / `axvline`: lineas de referencia horizontales o verticales (utiles para umbrales o maximos)
- Leyendas, titulos y etiquetas de ejes: indispensables para que el grafico se interprete sin ambiguedades
- Parametros de estilo: `color`, `linestyle`, `alpha` (transparencia), `linewidth`

**Principio de claridad:** Un grafico sobrecargado pierde efectividad. Cada elemento agregado debe aportar informacion nueva; de lo contrario, distrae al lector.

---

### Recomendaciones cuando estamos empezando

- Siempre inspeccionar los datos antes de imputar: entender el patron de valores faltantes (aleatorio o sistematico)
- Documentar las decisiones de imputacion; cambiar una estrategia puede alterar los resultados del modelo
- En series de tiempo, verificar que las fechas esten ordenadas y sin duplicados antes de analizar tendencias
- Preferir la interfaz orientada a objetos de Matplotlib desde el inicio; facilita la transicion a visualizaciones mas complejas

---

# Ejercicios Propuestos

---

## Ejercicio 1: Manejo de datos nulos (en vivo)

**Dataset:** Pima Indians Diabetes (`pima-indians-diabetes.csv`)

**Consigna:**
- Cargar el dataset desde la URL: `https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv`
- Identificar valores nulos (NaN) en el DataFrame
- Aplicar imputacion usando tres estrategias distintas:
  1. **Manual con Pandas:** `df.fillna(df.mean(), inplace=True)`
  2. **SimpleImputer con media:** `SimpleImputer(strategy='mean')`
  3. **SimpleImputer con mediana:** `SimpleImputer(strategy='median')`
  4. **SimpleImputer con moda:** `SimpleImputer(strategy='most_frequent')`
- Comparar los resultados de cada metodo

---

## Ejercicio 2: Manipulacion de objetos de tiempo (en vivo)

**Consigna:**
- Convertir un string a timestamp usando `pd.to_datetime()` con `dayfirst=True`
- Generar rangos de fechas con `pd.date_range()`:
  - Desde una fecha de inicio hasta una fecha de fin
  - Desde una fecha de inicio con 8 periodos (frecuencia diaria por defecto)
  - Desde una fecha de inicio con 8 periodos y frecuencia mensual (`freq='M'`)
- Generar rangos de periodos mensuales con `pd.period_range()`
- Calcular diferencias entre fechas (duracion en dias)
- Calcular diferencias en meses usando conversion a periodos (`.to_period('M')`)

---

## Ejercicio 3: Manipulacion de DataFrames con Pandas (actividad en clase)

**Dataset:** Bitcoin (`BTCUSD_1hr.csv`)

**Duracion:** 15 minutos

**Consigna paso a paso:**

1. Descargar el archivo `BTCUSD_1hr.csv` del repositorio indicado
2. Cargar el archivo usando `pd.read_csv()`
3. Aplicar el metodo `.describe()` para obtener un resumen numerico rapido de las variables
4. Obtener la cantidad de valores nulos usando el atributo apropiado
5. Extraer el mes de la columna `Date` y utilizar `.groupby()` para calcular la media mensual de cada variable
6. Graficar los precios de Bitcoin y analizar tendencias
7. Proponer una medida para establecer la volatilidad diaria

---

## Ejercicio 4: Creacion de graficos con Matplotlib (hands on lab)

**Duracion:** 25-30 minutos

**Consigna paso a paso:**

1. Seleccionar un dataset de los elegidos para la Clase 3
2. Cargar el archivo usando `pd.read_csv()` o `pd.read_excel()`
3. Elegir dos tipos de graficos apropiados para el analisis:
   - Lineplot (grafico de lineas)
   - Scatterplot (diagrama de dispersion)
   - Barras (bar plot)
   - Histograma
   - Boxplot
4. Realizar los graficos seleccionados utilizando la **interfaz orientada a objetos** de Matplotlib

---

## Ejercicio complementario: Enriquecimiento de visualizaciones (ejemplo en vivo)

**Dataset:** Precipitaciones de Pune, India (`pune_1965_to_2002.csv`)

**Consigna:**
- Graficar en el mismo eje las precipitaciones de enero y febrero a lo largo de los anos
- Calcular el valor maximo de cada mes
- Agregar lineas horizontales (`axhline`) para resaltar los maximos de cada serie, con distintos estilos de linea
- Incluir etiquetas de ejes, titulo y leyenda
- Aplicar el principio de no sobrecargar la figura con elementos innecesarios