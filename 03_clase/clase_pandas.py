import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Uso de NumPy y Pandas

    ### Ejercicios de clase pokemon dataset
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from pathlib import Path

    # Cargar el archivo de datos
    df = pd.read_csv( Path('datasets') / 'pokemon.txt', sep='\t')

    # Visualizar las primeras filas
    df.head()
    return df, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tratamiento de datos ausentes: eliminación e imputación

    Al revisar la columna `Type 2`, notarás que muchos Pokémon no tienen un segundo tipo, por lo que Pandas los lee como valores nulos (`NaN`).
    """)
    return


@app.cell
def _(df):
    # 1. Verificar nulos por columna
    df.isnull().sum()
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, np):
    # 2. Imputación: Llenar los nulos de 'Type 2' con 'None' (Ya que es un estado válido)
    df['Type 2'] = df['Type 2'].replace(['None'],np.nan)

    df
    return


@app.cell
def _(df):
    # 3. Eliminación (Ejemplo): Si existieran filas sin nombre, las eliminaríamos
    _df = df.dropna(subset=['Type 2'])

    print("\nValores ausentes tras el tratamiento:")
    _df.isnull().sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Combinar y agregar datos: merge, join y groupby

    Vamos a agrupar los datos para extraer estadísticas clave (como el promedio de ataque y defensa por cada tipo principal) y simular una combinación con un dataframe de bonus.
    """)
    return


@app.cell
def _(df):
    # 1. Agrupación con groupby: Promedio de estadísticas por 'Type 1'

    stats_por_tipo = (
        df
            .groupby('Type 1')[['HP', 'Attack', 'Defense', 'Speed']]
            .mean()
            .reset_index()
    )

    stats_por_tipo.head()
    return


@app.cell
def _(df, pd):
    # 2. Combinación con merge: Creamos un dataframe ficticio de "Multiplicadores" para cruzar datos

    df_bonus = pd.DataFrame({
        'Type 1': ['Grass', 'Fire', 'Water'],
        'Bonus_Damage': [1.2, 1.5, 1.3]
    })

    # Fusionamos los multiplicadores con nuestro dataset original
    df_con_bonus = pd.merge(df, df_bonus, on='Type 1', how='left')
    print("\nDataset combinado con Bonus de Daño:")
    df_con_bonus[['Name', 'Type 1', 'Bonus_Damage']].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Introducción al EDA reproducible en Python

    Establecemos las bases del análisis estadístico descriptivo básico para entender la distribución de las variables numéricas y categóricas de forma estandarizada.
    """)
    return


@app.cell
def _(df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Resumen numérico general
    print("Resumen estadístico del dataset:")
    df.describe()
    return plt, sns


@app.cell
def _(df, plt, sns):
    # Conteo de Pokémon legendarios
    print("\nDistribución de Pokémon Legendarios:")
    print(df['Legendary'].value_counts())

    # Gráfico reproducible: Distribución del Total de HP
    plt.figure(figsize=(8, 4))
    sns.histplot(df['HP'], kde=True, color='skyblue')
    plt.title('Distribución de los puntos de Vida (HP) en Pokémon')
    plt.xlabel('HP')
    plt.ylabel('Frecuencia')
    plt.show()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Flujo reproducible de EDA en Jupyter/Colab (archivos de ejemplo)

    Para empaquetar el flujo de forma profesional, creamos una función automatizada que genere un reporte visual inmediato de cualquier subconjunto de datos (en este caso, comparando las Generaciones).
    """)
    return


@app.cell
def _(df, pd, plt, sns):
    def generar_reporte_generacion(data: pd.DataFrame, num_generacion:int) -> None:

        """Genera un reporte EDA rápido y reproducible para una generación específica."""

        df_gen = data[data['Generation'] == num_generacion]

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle(f'Reporte Automático - Generación {num_generacion}', fontsize=16)

        # Gráfico 1: Top 5 Tipos más comunes
        (
            sns
                .countplot(
                    data=df_gen,
                    y='Type 1',
                    hue="Type 1",
                    order=df_gen['Type 1'].value_counts().index[:5],
                    ax=axes[0],
                    palette='viridis'
                )
        )

        axes[0].set_title('Top 5 Tipos Principales')

        # Gráfico 2: Relación Ataque vs Defensa
        sns.scatterplot(
            data=df_gen,
            x='Attack',
            y='Defense',
            hue='Legendary',
            palette="viridis",
            ax=axes[1]
        )

        axes[1].set_title('Ataque vs Defensa')

        plt.tight_layout()
        plt.show()

    # Ejecución del archivo/flujo de ejemplo para la Generación 1
    generar_reporte_generacion(df, num_generacion=1)

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11 - Indexación avanzada y manejo de slices en arrays

    Pasamos los datos a estructuras de NumPy para realizar segmentaciones (*slicing*) y filtrados avanzados de alta velocidad en las matrices de estadísticas.
    """)
    return


@app.cell
def _(df, np):
    print("""
    Convertimos las columnas de estadísticas de combate en un Array de NumPy
    Columnas: HP, Attack, Defense, Sp. Atk, Sp. Def, Speed
    """)

    matriz_stats = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].to_numpy()

    # 1. Slicing básico: Obtener las estadísticas de los primeros 5 Pokémon
    print("Stats de los primeros 5 Pokémon:\n", matriz_stats[:5, :])

    # 2. Slicing avanzado: Obtener solo Attack y Defense (columnas en posición 1 y 2) de los Pokémon del índice 10 al 15
    print("\nAtaque y Defensa (filas 10 a 15):\n", matriz_stats[10:15, 1:3])

    # 3. Indexación lógica (Boolean Indexing): Filtrar filas donde el Attack (columna 1) sea mayor a 150
    ataque_alto_mask = matriz_stats[:, 1] > 150
    print("\nCantidad de Pokémon con ataque mayor a 150:", np.sum(ataque_alto_mask))
    return


if __name__ == "__main__":
    app.run()
