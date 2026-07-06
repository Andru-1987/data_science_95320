# Fundamentos de Data Science I: Construyendo el Motor Predictivo

Vamos a hacer simples análisis estadísticos; vamos a construir un sistema cerrado, reproducible e iterativo que aprende del pasado para predecir el futuro.

A continuación, el mapa de ruta de lo que construiremos paso a paso.

## 1. La Matriz de Decisión: ¿Qué estamos cazando?

Antes de escribir una sola línea de código, necesitamos definir el problema. El Aprendizaje Supervisado funciona dándole al modelo un historial con las respuestas correctas. Pero, ¿qué forma tiene esa respuesta?

* **Clasificación (El modelo de las decisiones):**
* **Misión:** Asignar una etiqueta o categoría.
* **Pregunta clave:** *¿A qué grupo pertenece esto?*
* **Casos de uso:** ¿Este cliente se va a dar de baja (Sí/No)? ¿Este correo es fraude o legítimo?


* **Regresión (El modelo de las estimaciones):**
* **Misión:** Predecir un valor numérico continuo.
* **Pregunta clave:** *¿Cuánto?*
* **Casos de uso:** ¿Cuál será el precio de esta propiedad? ¿Cuántos ingresos generará este usuario en seis meses?



---

## 2. La Refinería: Preprocesamiento y Filtrado

Los algoritmos son matemáticos; no entienden de conceptos, colores o textos, solo entienden de números y distancias. Si introducimos "basura" al modelo, obtendremos predicciones "basura".

### El Filtro de Entrada (Limpieza)

* **Datos Incompletos:** No podemos dejar huecos. Rellenamos con estrategias matemáticas (media, mediana, moda) o eliminamos las filas irrecuperables.
* **Valores Ilegales:** Una edad de -5 años o un salario de cero en un cliente VIP destruyen la lógica del modelo. Requieren corrección manual o filtros estrictos.

### La Traducción Numérica (Ingeniería de Variables)

* **Textos a Números (One-Hot Encoding):** Transformamos variables categóricas (ej. Tipo de Cliente: Premium, Estándar) en columnas binarias independientes (Es_Premium: 1, Es_Estandar: 0).
* **Nivelando el Terreno (Estandarización):** Si una columna mide "hijos" (0 a 5) y otra "ingresos" ($0 a $100,000), el modelo le dará más peso a los ingresos solo por ser números más grandes. Usamos *StandardScaler* para llevar todo a un mismo idioma (media 0, desviación 1).
* **Domando los Extremos (Outliers):** Aplicamos técnicas como el *Capping* para limitar los valores absurdamente altos sin tener que borrar el registro completo.

---

## 3. Arquitectura del Sistema: Pipelines y Contención

Dividir los datos en Entrenamiento (Train, 70-80%) y Prueba (Test, 20-30%) es obligatorio. Pero aquí es donde la mayoría de los principiantes fallan debido al **Data Leakage (Fuga de Datos)**.

> **Regla de Oro:** El modelo jamás debe "ver" información del conjunto de prueba durante su entrenamiento. Si calculas la media de una columna usando todo el dataset y luego lo divides, acabas de hacer trampa.

**La Solución: El Pipeline.**
Es una estructura que encadena la limpieza, la transformación y el modelo predictivo en un solo bloque estanco. Garantiza que las reglas matemáticas se calculen *solo* con los datos de entrenamiento y se apliquen a ciegas sobre los datos nuevos.

---

## 4. Módulos Algorítmicos: El Cerebro del Sistema

Seleccionamos la herramienta adecuada según el terreno.

| Familia | Algoritmo | Perfil en la Práctica |
| --- | --- | --- |
| **Clasificación** | **Regresión Logística** | El punto de partida. Rápido, ligero y altamente interpretable. |
| **Clasificación** | **Árboles de Decisión** | Muy visual e intuitivo, pero propenso a memorizar los datos (*overfitting*). |
| **Clasificación** | **Random Forest** | El peso pesado. Un ensamble de árboles que corrige errores, resiste outliers y ofrece alta precisión. |
| **Regresión** | **Regresión Lineal** | El modelo base absoluto para trazar líneas de tendencia sobre valores continuos. |

---

## 5. Telemetría y Diagnóstico

Un modelo que predice sin ser evaluado es un peligro. Necesitamos paneles de control para medir su rendimiento real.

### Panel de Clasificación

* **Matriz de Confusión:** El mapa táctico de nuestros aciertos y errores (Falsos Positivos vs. Falsos Negativos).
* **Precision & Recall:** ¿De todos los que marcamos como positivos, cuántos acertamos? ¿De todos los positivos reales, cuántos logramos encontrar?
* **F1-Score:** El punto de equilibrio entre Precision y Recall.
* **Curva ROC (AUC):** La calificación final. Un AUC cercano a 1.0 significa que el modelo diferencia perfectamente entre clases.

### Panel de Regresión

* **MAE:** El error promedio crudo (ej. "Le erramos al precio por $5,000 en promedio").
* **RMSE:** Castiga fuertemente las equivocaciones grandes.
* **$R^2$:** La proporción de variabilidad explicada. Si $R^2 = 0.85$, el modelo explica el 85% del comportamiento de los datos.

### El Círculo de Retroalimentación (Diagnóstico Visual)

Los números mienten; los gráficos no. Analizamos los **residuos** (la diferencia entre lo predicho y lo real).

* **Gráfico de Residuos:** Si vemos patrones extraños (forma de embudo o U), el modelo no está capturando la realidad. Debe verse como ruido aleatorio.
* **Histograma de Residuos:** Los errores deben distribuirse como una campana simétrica.
