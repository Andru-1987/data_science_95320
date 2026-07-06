# Práctica en Python: Fundamentos de Data Science I

El código utiliza las librerías estándar `pandas`, `scikit-learn`, `matplotlib` y `seaborn`.

---

## 1. Carga de Datos y Configuración Inicial

Primero, importamos las librerías necesarias y cargamos el conjunto de datos desde la URL proporcionada.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración visual
sns.set_theme(style="whitegrid")

# 1. Carga de Datos
url = "https://raw.githubusercontent.com/readytensor/rt-datasets-binary-classification/refs/heads/main/datasets/processed/credit_approval/credit_approval.csv"

column_names = [
    "gender", "age", "debt_ratio", "marital_status", "customer_type",
    "occupation", "employment_status", "years_employed", "has_default_history",
    "owns_assets", "credit_score", "has_other_loans", "citizenship",
    "annual_income", "balance", "approved"
]

df = pd.read_csv(url, names=column_names, header=0)

# Mostramos las primeras filas para entender la estructura
print(df.head())


```

---

## 2. Preparación y Filtrado (Pre-Pipeline)

Antes de automatizar el proceso, abordamos los valores ilegales y los extremos (outliers).

```python
# 2.1. Corrección Manual de Valores Ilegales
# Asumimos que no puede haber edades negativas o ingresos negativos.
df = df[(df['age'] >= 0) & (df['annual_income'] >= 0)]

# 2.2. Tratamiento de Outliers (Capping / Winsorization)
# Limitamos los ingresos atípicos al percentil 99 para no distorsionar el modelo
percentil_99 = df['annual_income'].quantile(0.99)
df['annual_income'] = np.where(df['annual_income'] > percentil_99, percentil_99, df['annual_income'])


```

---

## 3. El Pipeline de Preprocesamiento

Para evitar el *Data Leakage* (fuga de información) , estructuramos todo el preprocesamiento en un Pipeline. Esto asegura que la imputación y el escalado se calculen únicamente con los datos de entrenamiento.

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Separar características numéricas y categóricas
numeric_features = ['age', 'debt_ratio', 'years_employed', 'credit_score', 'annual_income', 'balance']
categorical_features = ['gender', 'marital_status', 'customer_type', 'occupation', 'employment_status', 'has_default_history', 'owns_assets', 'has_other_loans', 'citizenship']

# Pipeline para variables numéricas: Imputación de faltantes por la mediana y escalado
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), # Filtro: Imputación 
    ('scaler', StandardScaler()) # Variables Numéricas StandardScaler 
])

# Pipeline para variables categóricas: Imputación por la moda y codificación binaria
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # One-Hot Encoding 
])

# Ensamblar el preprocesador
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])


```

---

## 4. Problema de Clasificación: Predicción de Aprobación

En esta sección, el objetivo es predecir a qué grupo pertenece un dato  (Target: `approved`).

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 1. División de Datos (Train/Test)
X_clf = df.drop('approved', axis=1)
y_clf = df['approved']

# Train (80%) / Test (20%) 
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

# 2. Definición de Modelos
modelos_clasificacion = {
    "Regresión Logística": LogisticRegression(max_iter=1000), # Rápido, interpretable 
    "Árbol de Decisión": DecisionTreeClassifier(random_state=42), # Intuitivo y visual 
    "Random Forest": RandomForestClassifier(random_state=42) # Robusto ante outliers 
}

# 3. Entrenamiento y Evaluación
for nombre, modelo in modelos_clasificacion.items():
    # Estructurar Pipeline
    clf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', modelo)])
    
    # Entrenar
    clf_pipeline.fit(X_train_clf, y_train_clf)
    
    # Predecir
    y_pred_clf = clf_pipeline.predict(X_test_clf)
    y_pred_proba = clf_pipeline.predict_proba(X_test_clf)[:, 1]
    
    # Panel de Evaluación: Clasificación 
    print(f"--- {nombre} ---")
    print(f"Matriz de Confusión:\n{confusion_matrix(y_test_clf, y_pred_clf)}") # Matriz de Confusión 
    print(f"Reporte de Clasificación (Precision, Recall, F1-Score):\n{classification_report(y_test_clf, y_pred_clf)}")
    print(f"AUC ROC: {roc_auc_score(y_test_clf, y_pred_proba):.4f}\n")


```

---

## 5. Problema de Regresión: Predicción de Puntaje de Crédito

Para transformar este conjunto de datos en un problema de regresión, cambiaremos nuestra variable objetivo. En lugar de predecir si el crédito es aprobado, predeciremos un valor numérico continuo: el **`credit_score`** (puntaje de crédito), basándonos en el resto del perfil financiero.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Modificar el Dataset para Regresión
# Target = 'credit_score'. Eliminamos 'approved' para evitar correlaciones espurias o sesgos.
X_reg = df.drop(['credit_score', 'approved'], axis=1)
y_reg = df['credit_score']

# Actualizamos las listas de características numéricas para el preprocesador
numeric_features_reg = ['age', 'debt_ratio', 'years_employed', 'annual_income', 'balance']

preprocessor_reg = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features_reg),
        ('cat', categorical_transformer, categorical_features)
    ])

# 2. División Train/Test
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

# 3. Pipeline de Regresión Lineal
reg_pipeline = Pipeline(steps=[('preprocessor', preprocessor_reg),
                               ('regressor', LinearRegression())]) # El modelo base 

# 4. Entrenamiento y Predicción
reg_pipeline.fit(X_train_reg, y_train_reg)
y_pred_reg = reg_pipeline.predict(X_test_reg)

# 5. Panel de Evaluación: Regresión 
mae = mean_absolute_error(y_test_reg, y_pred_reg)
rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))
r2 = r2_score(y_test_reg, y_pred_reg)

print("--- Evaluación Regresión Lineal ---")
print(f"MAE: {mae:.2f}") # Error promedio en unidades reales 
print(f"RMSE: {rmse:.2f}") # Penaliza fuertemente los errores grandes 
print(f"R²: {r2:.4f}") # Proporción de variabilidad explicada 


```

---

## 6. Diagnóstico Visual (Regresión)

El último paso de nuestro ciclo es diagnosticar métricas y gráficos visuales  para validar las suposiciones de nuestro modelo lineal.

```python
# Calcular los residuos
residuos = y_test_reg - y_pred_reg

fig, ax = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de Residuos
sns.scatterplot(x=y_pred_reg, y=residuos, ax=ax[0], alpha=0.6)
ax[0].axhline(y=0, color='r', linestyle='--')
ax[0].set_title('Gráfico de Residuos')
ax[0].set_xlabel('Valores Predichos')
ax[0].set_ylabel('Residuos')
# Interpretación: Si hay un patrón (ej. embudo), el modelo falla.

# Histograma de Residuos
sns.histplot(residuos, kde=True, ax=ax[1], bins=30)
ax[1].set_title('Histograma de Residuos')
ax[1].set_xlabel('Residuos')
# Interpretación: Los errores deben distribuirse simétricamente (distribución normal).

plt.tight_layout()
plt.show()


```

---

## 7. Integración de Validación Cruzada (Cross-Validation)

La **Validación Cruzada (Cross-Validation)** es una excelente adición:

> En lugar de confiar en una única división entre entrenamiento y prueba (Train/Test Split), la validación cruzada divide los datos en $K$ partes (folds) para entrenar y evaluar el modelo $K$ veces. Esto ayuda a asegurar que las métricas de evaluación sean robustas y no dependan de una división aleatoria afortunada o desafortunada.


> La elección entre **K-Fold Estándar** y **K-Fold Estratificado** (Stratified K-Fold) depende fundamentalmente del tipo de problema que estás resolviendo (Regresión vs. Clasificación) y de la naturaleza de tu variable objetivo (Target).

Aquí tienes una tabla comparativa para saber exactamente cuándo usar cada una:

| Criterio | K-Fold Estándar (Standard K-Fold) | K-Fold Estratificado (Stratified K-Fold) |
| --- | --- | --- |
| **Tipo de Problema Ideal** | Regresión | Clasificación |
| **Tipo de Variable a Predecir (Target)** | Numérica y continua (ej. precios, edades, temperaturas). | Categórica y discreta (ej. sí/no, spam/no spam, alto/medio/bajo). |
| **Mecánica de Partición** | Divide el conjunto de datos en $K$ partes de forma puramente aleatoria. | Divide en $K$ partes, pero **preserva el porcentaje de muestras de cada clase** en cada parte. |
| **Manejo de Desbalanceo** | Pobre. Al ser aleatorio, un *fold* podría quedarse sin valores extremos o atípicos de la distribución. | Excelente. Garantiza que si tu dataset tiene un 90% de clase A y 10% de clase B, todos los *folds* mantendrán esa misma proporción 90/10. |
| **Riesgo Principal si se usa mal** | Usarlo en clasificación con clases muy desbalanceadas puede resultar en un *fold* que contenga solo ejemplos de una clase, haciendo que el modelo falle al entrenar o evaluar. | No se puede aplicar directamente a variables continuas porque requeriría tratar cada número exacto como una "clase" distinta (lo cual es infinito o computacionalmente inviable). |
| **Ejemplo Práctico del Dataset** | Predecir el `credit_score` (de 0 a 1000). | Predecir si el crédito es `approved` (aprobado o rechazado). |

### Regla de oro

* **Si predices una categoría (Clasificación):** Usa siempre **Stratified K-Fold**. Es el estándar de la industria porque te protege contra el desbalanceo de clases y asegura evaluaciones consistentes.
* **Si predices una cantidad (Regresión):** Usa **K-Fold Estándar**. Si tus datos tienen una distribución muy extraña o sesgada, puedes llegar a usar técnicas avanzadas (como agrupar los números en rangos y estratificar esos rangos), pero por defecto, el estándar es la opción correcta.


### 7.1. Validación Cruzada para Clasificación (Stratified K-Fold)

En problemas de clasificación, es fundamental usar `StratifiedKFold`, el cual asegura que cada fold mantenga aproximadamente la misma proporción de las clases de la variable objetivo (`approved`).

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Definimos el esquema de validación cruzada (5 folds)
cv_estrategia_clf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("--- Validación Cruzada: Clasificación (Métrica AUC ROC) ---")

for nombre, modelo in modelos_clasificacion.items():
    # Creamos el pipeline completo para cada modelo
    pipeline_eval = Pipeline(steps=[('preprocessor', preprocessor),
                                    ('classifier', modelo)])
    
    # cross_val_score ejecuta internamente el ajuste (fit) del preprocesamiento 
    # y del modelo de forma aislada en cada fold, previniendo el Data Leakage.
    scores_cv = cross_val_score(pipeline_eval, X_clf, y_clf, cv=cv_estrategia_clf, scoring='roc_auc')
    
    print(f"{nombre}:")
    print(f"  Scores por fold: {scores_cv}")
    print(f"  AUC Promedio: {scores_cv.mean():.4f} (+/- desviación estándar: {scores_cv.std() * 2:.4f})\n")

```

### 7.2. Validación Cruzada para Regresión (K-Fold Estándar)

Para variables continuas como el puntaje de crédito (`credit_score`), utilizamos un `KFold` estándar ya que no existen clases discretas que estratificar.

```python
from sklearn.model_selection import KFold, cross_validate

# Definimos el esquema de validación cruzada para regresión
cv_estrategia_reg = KFold(n_splits=5, shuffle=True, random_state=42)

# Usamos cross_validate para evaluar múltiples métricas simultáneamente
metricas = ['neg_mean_absolute_error', 'r2']
resultados_cv = cross_validate(reg_pipeline, X_reg, y_reg, cv=cv_estrategia_reg, scoring=metricas)

# scikit-learn devuelve los errores en formato negativo para maximizarlos internamente, los convertimos a positivo
mae_scores = -resultados_cv['test_neg_mean_absolute_error']
r2_scores = resultados_cv['test_r2']

print("--- Validación Cruzada: Regresión Lineal ---")
print(f"MAE Promedio: {mae_scores.mean():.2f} (+/- {mae_scores.std() * 2:.2f})")
print(f"R² Promedio: {r2_scores.mean():.4f} (+/- {r2_scores.std() * 2:.4f})")

```


