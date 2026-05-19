## Resumen Teórico: ¿Para qué sirven NumPy y Pandas?

### NumPy (Numerical Python)

Es la librería central e indispensable para la computación numérica dentro del ecosistema de Python. Su propósito es proveer estructuras de datos de alto rendimiento y herramientas matemáticas optimizadas para manipular grandes volúmenes de datos de manera eficiente.

* **Arrays N-Dimensionales (`ndarray`):** Introduce una estructura de datos homogénea (todos sus elementos son del mismo tipo) y de tamaño fijo, especialmente diseñada para realizar cálculos multidimensionales veloces.


* **Rendimiento optimizado (C y SIMD):** Gracias a su implementación interna en lenguaje C y al uso de instrucciones SIMD a nivel de CPU, ejecuta operaciones vectorizadas que eliminan la necesidad de usar bucles tradicionales en Python, siendo hasta 50x o 100x más rápida.


* **Eficiencia de memoria:** Almacena la información en bloques contiguos de memoria, a diferencia de las listas de Python que guardan referencias dispersas a objetos.


* **Broadcasting:** Cuenta con un mecanismo que permite realizar operaciones aritméticas automáticas entre arrays de diferentes dimensiones sin necesidad de duplicar o copiar físicamente los datos en la memoria.



### Pandas

Es una librería de código abierto que proporciona estructuras de datos flexibles y herramientas de análisis de alto rendimiento fáciles de usar. Permite trabajar con la comodidad de una interfaz tabular (estilo hoja de cálculo) pero combinada con todo el poder de automatización de Python.

***Estructuras tabulares principales:** Define las `Series` (estructuras unidimensionales con datos y etiquetas indexadas) y los `DataFrames` (estructuras bidimensionales de filas y columnas que pueden albergar tipos de datos heterogéneos).


***Conectividad con múltiples fuentes:** Facilita la importación y exportación de información desde y hacia formatos comunes como CSV, Excel, SQL, JSON y HTML con instrucciones simples de una sola línea.


* **Procesamiento a gran escala:** Elimina las barreras de herramientas tradicionales como Excel, haciendo posible procesar eficientemente millones de filas de datos.


* **Flujos reproducibles:** Permite limpiar, transformar y estructurar los datos mediante código documentado, garantizando que las tareas repetitivas se automaticen con precisión.



---

## ¿Qué es un EDA y cuál es su importancia?

El **EDA** (**Análisis Exploratorio de Datos**, por sus siglas en inglés) es el paso fundamental en el que un profesional examina, limpia y procesa estadísticamente un conjunto de datos antes de construir cualquier modelo predictivo o algoritmo de Machine Learning. Su objetivo principal es comprender la distribución de las variables, identificar anomalías o errores, y descubrir patrones o relaciones clave utilizando resúmenes numéricos y herramientas gráficas.

### Importancia de NumPy y Pandas en el EDA

Ambas librerías constituyen los cimientos de todo el ecosistema científico de Data Science en Python.

***Pandas** actúa como el centro de control del EDA, ya que permite interactuar con los datos de forma lógica, estructurada y legible, facilitando la detección rápida de problemas de integridad (como tipos de datos incorrectos o valores nulos).


* **NumPy** opera en una capa inferior (y complementaria), brindando el soporte matemático y la velocidad computacional para ejecutar cálculos estadísticos descriptivos masivos y segmentaciones avanzadas en fracciones de segundo.



---

## Pasos Básicos de un EDA para un Profesional de Data Science / ML

Tomando como base las metodologías y herramientas de análisis estructurado de datos, los pasos esenciales para llevar a cabo un EDA profesional y reproducible son:

### 1. Lectura e Importación de los Datos

El proceso inicia conectando el entorno de trabajo con la fuente donde residen los datos. Se utilizan las funciones de lectura de Pandas (como `pd.read_csv()`) para cargar los archivos y transformarlos de inmediato en un objeto de tipo DataFrame manejable.

### 2. Exploración Estructural Inicial

Consiste en realizar un reconocimiento general de las dimensiones y consistencia de la información cargada. Esto incluye:

* Visualizar los primeros registros del conjunto de datos mediante `df.head()` para entender el contexto de las variables.


* Inspeccionar el volumen total (filas y columnas) y las propiedades de las variables utilizando los atributos de forma y tipo (`shape`, `dtype`, `size`) o resúmenes del DataFrame como `df.info()`.



### 3. Limpieza de Datos (Data Cleaning)

Los datos del mundo real rara vez vienen perfectos; suelen contener registros faltantes o corruptos. En esta etapa se identifican los valores nulos (`NaN`, `None`, `NULL`) con `df.isnull()`  y se les aplica el tratamiento técnico correspondiente:

* **Eliminación:** Remover filas o columnas incompletas con `df.dropna()` si representan ruido o pérdida aceptable.


* **Imputación:** Reemplazar o rellenar las celdas vacías con ceros, constantes o valores representativos (como la media) usando `df.fillna()`.



### 4. Análisis Estadístico Descriptivo

Se aplican funciones matemáticas consolidadas para medir las tendencias centrales y la dispersión del conjunto de datos, ya sea de forma global o sobre dimensiones específicas (`axis=0` para columnas o `axis=1` para filas):

* Se extraen métricas individuales clave como la media aritmética (`np.mean()`), la mediana (`np.median()`), la desviación estándar (`np.std()`), la varianza (`np.var()`) y los rangos extremos (`np.min()` / `np.max()`).


* Se analizan los percentiles esenciales (P25, P50, P75) y el rango intercuartílico (IQR) para ubicar la concentración y dispersión central de los datos.


* Pandas permite automatizar por completo este paso en una sola instrucción condensada mediante `df.describe()`.



### 5. Filtrado, Transformación y Agregación

El profesional segmenta la información y manipula las variables para aislar comportamientos específicos o construir características descriptivas útiles para los modelos de Machine Learning. Esto comprende:

* Aplicar filtros basados en condiciones lógicas sobre las columnas (`df[condición]`).


* Modificar valores existentes o agregar nuevas columnas calculadas para enriquecer el análisis.


* Agrupar los registros en base a variables categóricas mediante `df.groupby()` y resumir sus métricas para descubrir tendencias ocultas por segmentos.



### 6. Visualización Estadística de Resultados

Finalmente, se integran los conjuntos de datos analizados con librerías gráficas (como Matplotlib o Seaborn) para interpretar visualmente las hipótesis y distribuciones descriptivas extraídas. Los gráficos indispensables en esta fase son:

* **Histogramas:** Útiles para observar la forma física y la distribución de frecuencias de las variables numéricas.


* **Diagramas de Caja y Bigotes (Box Plots):** Ideales para comparar la dispersión entre grupos, identificar los cuartiles y detectar gráficamente valores atípicos (*outliers*).


* **Gráficos de Dispersión (Scatter Plots):** Diseñados para estudiar la correlación entre dos variables continuas y trazar líneas de tendencia o regresión.


* **Gráficos de Barras (Bar Charts):** Empleados para realizar comparaciones cuantitativas directas entre distintas categorías.
