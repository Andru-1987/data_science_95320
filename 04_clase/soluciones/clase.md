## Importación de bibliotecas

```python
# Importacion de bibliotecas para analisis y visualizacion
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')
```

---

## Ejercicio 1 – Manejo de datos nulos (en vivo)

### 1.1 Cargar el dataset desde la URL

```python
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
column_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
                'insulin', 'bmi', 'diabetes_pedigree', 'age', 'outcome']
df_original = pd.read_csv(url, names=column_names)
```

### 1.2 Identificar valores nulos (NaN)

```python
print("Valores nulos por columna (usando isnull().sum()):")
print(df_original.isnull().sum())
print("\n" + "="*50 + "\n")

columns_with_missing = ['glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi']
df_simulated = df_original.copy()
df_simulated[columns_with_missing] = df_simulated[columns_with_missing].replace(0, np.nan)

print("Valores nulos despues de simular datos faltantes (reemplazando 0 por NaN):")
print(df_simulated.isnull().sum())
```

**Explicacion:** En este paso, ademas de identificar los NaN existentes, convertimos manualmente los ceros en NaN para simular datos faltantes, ya que el dataset original no los tiene implicitos.

### 1.3 Aplicar cuatro estrategias de imputacion

```python
def compare_imputation(df_with_nulls, column_name):
    """Funcion que muestra los resultados de distintas imputaciones"""
    
    # 1. Imputacion manual con Pandas usando la media
    df_manual = df_with_nulls.copy()
    df_manual.fillna(df_manual.mean(), inplace=True)
    
    # 2. SimpleImputer con estrategia 'mean' (media)
    imputer_mean = SimpleImputer(strategy='mean')
    df_imputer_mean = pd.DataFrame(
        imputer_mean.fit_transform(df_with_nulls),
        columns=df_with_nulls.columns
    )
    
    # 3. SimpleImputer con estrategia 'median' (mediana)
    imputer_median = SimpleImputer(strategy='median')
    df_imputer_median = pd.DataFrame(
        imputer_median.fit_transform(df_with_nulls),
        columns=df_with_nulls.columns
    )
    
    # 4. SimpleImputer con estrategia 'most_frequent' (moda)
    imputer_mode = SimpleImputer(strategy='most_frequent')
    df_imputer_mode = pd.DataFrame(
        imputer_mode.fit_transform(df_with_nulls),
        columns=df_with_nulls.columns
    )
    
    # Mostrar comparacion para una columna especifica
    print(f"Comparacion para la columna '{column_name}':")
    print("-" * 50)
    print(f"Original (con NaN)        : {df_with_nulls[column_name].describe()['mean']:.2f} (mean)")
    print(f"Manual (fillna con media) : {df_manual[column_name].describe()['mean']:.2f} (mean)")
    print(f"SimpleImputer (media)     : {df_imputer_mean[column_name].describe()['mean']:.2f} (mean)")
    print(f"SimpleImputer (mediana)   : {df_imputer_median[column_name].describe()['mean']:.2f} (mean)")
    print(f"SimpleImputer (moda)      : {df_imputer_mode[column_name].describe()['mean']:.2f} (mean)")
    
    return df_manual, df_imputer_mean, df_imputer_median, df_imputer_mode

df_manual, df_imputer_mean, df_imputer_median, df_imputer_mode = compare_imputation(df_simulated, 'glucose')
```

**Explicacion:** `SimpleImputer` permite reemplazar los valores faltantes usando una estadistica descriptiva de cada columna. Las opciones `'mean'`, `'median'` y `'most_frequent'` son las que se piden en el ejercicio. Al comparar las estrategias, vemos como cambian los resultados estadisticos.

### 1.4 Comparacion de metodos

```python
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

datasets = [
    (df_imputer_mean, "Imputer con Media"),
    (df_imputer_median, "Imputer con Mediana"),
    (df_imputer_mode, "Imputer con Moda"),
    (df_manual, "Manual con Media")
]

for i, (data, title) in enumerate(datasets):
    axes[i].hist(data['glucose'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[i].set_title(title, fontsize=12)
    axes[i].set_xlabel("Glucosa")
    axes[i].set_ylabel("Frecuencia")

plt.suptitle("Comparacion de la distribucion de glucosa segun metodo de imputacion", fontsize=16)
plt.tight_layout()
plt.show()
```

---

## Ejercicio 2 – Manipulacion de objetos de tiempo (en vivo)

### 2.1 Convertir string a timestamp

```python
date_string = "15/03/2025"
timestamp = pd.to_datetime(date_string, dayfirst=True)

print(f"String original: {date_string}")
print(f"Timestamp convertido: {timestamp}")
print(f"Tipo de dato: {type(timestamp)}")
```

**Explicacion:** El parametro `dayfirst=True` le indica a pandas que interprete el primer elemento del string como el dia, util cuando trabajamos con formatos internacionales.

### 2.2 Generar rangos de fechas con `pd.date_range()`

```python
start_date = "2025-01-01"
end_date = "2025-01-10"
date_range_1 = pd.date_range(start=start_date, end=end_date)
print("Rango de fechas (inicio a fin):")
print(date_range_1)

start_date = "2025-01-01"
periodos = 8
date_range_2 = pd.date_range(start=start_date, periods=periodos)
print("\nRango de fechas con 8 periodos (diario):")
print(date_range_2)

date_range_3 = pd.date_range(start=start_date, periods=periodos, freq='M')
print("\nRango de fechas con 8 periodos (mensual):")
print(date_range_3)
```

### 2.3 Generar rangos de periodos mensuales con `pd.period_range()`

```python
period_range = pd.period_range(start="2025-01", periods=8, freq='M')
print("Rangos de periodos mensuales:")
print(period_range)
print(f"Tipo de dato: {type(period_range[0])}")
```

**Explicacion:** La diferencia entre `date_range` y `period_range` es crucial: mientras `date_range` genera timestamps con una frecuencia, `period_range` genera periodos de tiempo definidos.

### 2.4 Calcular diferencias entre fechas

```python
fecha_inicio = pd.to_datetime("2025-01-01")
fecha_fin = pd.to_datetime("2025-12-31")
diferencia_dias = (fecha_fin - fecha_inicio).days
print(f"Dias transcurridos entre {fecha_inicio.date()} y {fecha_fin.date()}: {diferencia_dias} dias")

periodo_inicio = pd.Period("2025-01", freq='M')
periodo_fin = pd.Period("2025-12", freq='M')
diferencia_meses = periodo_fin - periodo_inicio
print(f"Meses transcurridos entre {periodo_inicio} y {periodo_fin}: {diferencia_meses} meses")

fecha_inicio_ts = pd.to_datetime("2025-01-01")
fecha_fin_ts = pd.to_datetime("2025-12-15")
dif_meses_periodos = fecha_fin_ts.to_period('M') - fecha_inicio_ts.to_period('M')
print(f"Diferencia en meses (usando to_period): {dif_meses_periodos} meses")
```

---

## Ejercicio 3 – Manipulacion de DataFrames con Pandas (actividad en clase)

### 3.1 Cargar y explorar el dataset

```python
df_bitcoin = pd.read_csv('BTCUSD_1hr.csv')
print("Vista previa de los datos:")
print(df_bitcoin.head())

print("\nResumen estadistico con describe():")
print(df_bitcoin.describe())

print("\nCantidad de valores nulos por columna:")
print(df_bitcoin.isnull().sum())

print("\nInformacion del DataFrame:")
print(df_bitcoin.info())
```

**Explicacion sobre la volatilidad diaria:** La volatilidad diaria mide la fluctuacion del precio de un activo en un dia. Se calcula como la desviacion estandar de los retornos diarios, donde los retornos son el cambio porcentual del precio de cierre entre dos periodos consecutivos.

### 3.2 Extraer mes y calcular media mensual

```python
df_bitcoin['Date'] = pd.to_datetime(df_bitcoin['Date'])
df_bitcoin['Month'] = df_bitcoin['Date'].dt.month
monthly_means = df_bitcoin.groupby('Month').mean()
print("Medias mensuales de cada variable:")
print(monthly_means)
```

### 3.3 Graficar precios de Bitcoin

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

ax1.plot(df_bitcoin['Date'], df_bitcoin['Close'], linewidth=0.8, color='orange')
ax1.set_title('Evolucion del Precio de Bitcoin (Close Price)', fontsize=14)
ax1.set_ylabel('Precio (USD)', fontsize=12)
ax1.grid(True, alpha=0.3)

ax2.plot(df_bitcoin['Date'], df_bitcoin['Volume'], linewidth=0.8, color='green')
ax2.set_title('Volumen de Transacciones de Bitcoin', fontsize=14)
ax2.set_ylabel('Volumen', fontsize=12)
ax2.set_xlabel('Fecha', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 3.4 Propuesta para medir volatilidad diaria

```python
df_bitcoin['Daily_Return'] = df_bitcoin['Close'].pct_change()
df_bitcoin['Volatility_7d'] = df_bitcoin['Daily_Return'].rolling(window=7).std() * np.sqrt(365)

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_bitcoin['Date'], df_bitcoin['Volatility_7d'], linewidth=1, color='red')
ax.set_title('Volatilidad Diaria de Bitcoin (Desviacion Estandar de Retornos en 7 dias)', fontsize=14)
ax.set_ylabel('Volatilidad Anualizada', fontsize=12)
ax.set_xlabel('Fecha', fontsize=12)
ax.grid(True, alpha=0.3)

print("\nEstadisticas de Volatilidad:")
print(f"   Volatilidad media: {df_bitcoin['Volatility_7d'].mean():.4f}")
print(f"   Volatilidad maxima: {df_bitcoin['Volatility_7d'].max():.4f}")
print(f"   Volatilidad minima: {df_bitcoin['Volatility_7d'].min():.4f}")

plt.show()
```

---

## Ejercicio 4 – Creacion de graficos con Matplotlib (hands on lab)

### 4.1 Cargar y preparar datos

```python
df_bitcoin = pd.read_csv('BTCUSD_1hr.csv')
df_bitcoin['Date'] = pd.to_datetime(df_bitcoin['Date'])
df_bitcoin.set_index('Date', inplace=True)
df_sample = df_bitcoin.tail(500)

print("Datos preparados para visualizacion:")
print(df_sample.head())
```

### 4.2 Grafico de lineas (Lineplot) con interfaz orientada a objetos

```python
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_sample.index, df_sample['Close'], 
        color='blue', linewidth=1.5, label='Precio de Cierre')
ax.plot(df_sample.index, df_sample['High'], 
        color='green', linewidth=0.8, alpha=0.7, label='Precio Maximo')
ax.plot(df_sample.index, df_sample['Low'], 
        color='red', linewidth=0.8, alpha=0.7, label='Precio Minimo')

ax.set_title('Evolucion del Precio de Bitcoin (OHLC)', fontsize=14)
ax.set_xlabel('Fecha', fontsize=12)
ax.set_ylabel('Precio (USD)', fontsize=12)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 4.3 Diagrama de dispersion (Scatterplot) con interfaz orientada a objetos

```python
fig, ax = plt.subplots(figsize=(10, 6))

price_range = df_sample['High'] - df_sample['Low']
scatter = ax.scatter(df_sample.index, df_sample['Close'], 
                     c=price_range, cmap='viridis', 
                     alpha=0.6, s=20)

ax.set_title('Relacion entre Precio de Cierre y Rango de Precios', fontsize=14)
ax.set_xlabel('Fecha', fontsize=12)
ax.set_ylabel('Precio de Cierre (USD)', fontsize=12)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Rango de Precios (High - Low)', fontsize=10)

z = np.polyfit(range(len(df_sample)), df_sample['Close'], 1)
p = np.poly1d(z)
ax.plot(df_sample.index, p(range(len(df_sample))), 
        "r--", alpha=0.8, label='Tendencia lineal')

ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

**Explicacion de la interfaz orientada a objetos:** A diferencia de la interfaz procedural (usando `plt.plot()` directamente), la interfaz orientada a objetos da un control mas granular sobre todos los elementos de la figura. Se crea una `figura` y un `eje` explicitamente con `plt.subplots()`, y luego se usan metodos como `ax.plot()` para agregar elementos. Esto facilita la personalizacion y es especialmente util cuando se crean graficos complejos con multiples subplots.

---

## Ejercicio complementario – Enriquecimiento de visualizaciones (ejemplo en vivo)

### 5.1 Cargar dataset de precipitaciones

```python
df_pune = pd.read_csv('pune_1965_to_2002.csv')
print("Vista previa de los datos:")
print(df_pune.head())
print("\nInformacion del dataset:")
print(df_pune.info())
```

### 5.2 Graficar precipitaciones de enero y febrero

```python
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(df_pune['Year'], df_pune['Jan'], 
        marker='o', linewidth=2, label='Enero', color='blue')
ax.plot(df_pune['Year'], df_pune['Feb'], 
        marker='s', linewidth=2, label='Febrero', color='green')

max_jan = df_pune['Jan'].max()
max_feb = df_pune['Feb'].max()
year_max_jan = df_pune.loc[df_pune['Jan'].idxmax(), 'Year']
year_max_feb = df_pune.loc[df_pune['Feb'].idxmax(), 'Year']

ax.axhline(y=max_jan, color='blue', linestyle='--', alpha=0.7, 
           label=f'Maximo Enero: {max_jan:.1f} mm ({year_max_jan})')
ax.axhline(y=max_feb, color='green', linestyle=':', alpha=0.7, 
           label=f'Maximo Febrero: {max_feb:.1f} mm ({year_max_feb})')

ax.set_title('Precipitaciones en Pune: Comparacion Enero vs Febrero (1965-2002)', 
             fontsize=16, fontweight='bold')
ax.set_xlabel('Anio', fontsize=12)
ax.set_ylabel('Precipitacion (mm)', fontsize=12)
ax.legend(loc='upper right', fontsize=10)
ax.grid(True, alpha=0.3)

plt.xticks(rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
```

### 5.3 Aplicando el principio de minimalismo y claridad

```python
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_pune['Year'], df_pune['Jan'], linewidth=2, label='Enero', color='#1f77b4')
ax.plot(df_pune['Year'], df_pune['Feb'], linewidth=2, label='Febrero', color='#2ca02c')

ax.axhline(y=max_jan, color='#1f77b4', linestyle='--', alpha=0.5)
ax.axhline(y=max_feb, color='#2ca02c', linestyle='--', alpha=0.5)

ax.text(df_pune['Year'].max(), max_jan + 5, f'Max Ene: {max_jan:.0f}mm', ha='right', va='bottom', color='#1f77b4', fontsize=9)
ax.text(df_pune['Year'].max(), max_feb + 5, f'Max Feb: {max_feb:.0f}mm', ha='right', va='bottom', color='#2ca02c', fontsize=9)

ax.set_title('Precipitaciones en Pune (1965-2002)', fontsize=14)
ax.set_xlabel('Anio', fontsize=11)
ax.set_ylabel('Precipitacion (mm)', fontsize=11)
ax.legend(loc='upper left', frameon=False)
ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
```

---

## Resumen y reflexiones finales

- **Imputacion de datos:** La eleccion del metodo de imputacion (mean, median, most_frequent) debe basarse en la naturaleza de los datos y la distribucion de los valores faltantes. La media puede verse afectada por valores atipicos, mientras que la mediana es mas robusta.
- **Manejo de fechas:** Pandas ofrece herramientas potentes para trabajar con series temporales. La diferencia entre `date_range` y `period_range` es importante segun se necesite trabajar con instantes de tiempo o intervalos.
- **Visualizacion:** La interfaz orientada a objetos de Matplotlib proporciona un control mas fino sobre los graficos y es la practica recomendada para visualizaciones complejas.
- **Volatilidad:** Es una metrica clave en finanzas que se calcula a partir de la desviacion estandar de los retornos diarios, y ayuda a cuantificar el riesgo del activo.
- **Minimalismo en graficos:** Eliminar elementos innecesarios (bordes superfluos, etiquetas redundantes) mejora la comunicacion visual de los datos.
