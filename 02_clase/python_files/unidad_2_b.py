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
    # Ejercicio 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vanilla forma
    """)
    return


@app.cell
def _():
    dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    valores = [200, 225, 232, 221, 243, 256, 255]

    # Lista que guarda los dias en donde la accion decrecio
    decrease_days = []

    # Zip dias y valores pero extrayendo el valor anterior
    for day, current_value, prev_value in zip(dias[1:], valores[1:], valores[:-1]):
        if current_value < prev_value:
            decrease_days.append((day, current_value - prev_value))

    print("Dias en donde decrecio la accion:", decrease_days)
    return (valores,)


@app.cell
def _(valores):
    valores[:-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Primera forma
    """)
    return


@app.cell
def _():
    # L = [ ] En python esto es una lista vacia
    _Dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    _Valores = [200, 225, 232, 221, 243, 256, 255]
    import numpy as np
    #Importamos la libreria en Numpy
    Dif = np.diff(_Valores, n=1)
    for _x, y in zip(_Dias[1:], Dif):
    #Guardamos la diferencia de de los valores, donde n es el número de veces que se diferencian los valores.
        if (_x != 'Lunes') & (y < 0):
    #Creamos un ciclo for para (x, y), unimos con zip Dias y Dif
            print(_x, y)  #Condicion: Si x es diferente de Lunes, & , y es menor que 0  #Imprimimos el resultado de iterar nuestro ciclo for en x,y
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Segunda forma
    """)
    return


@app.cell
def _():
    _Dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    _Valores = [200, 225, 232, 221, 243, 256, 255]
    import pandas as pd
    df = pd.DataFrame()
    df['Dias'] = _Dias
    df['Valores'] = _Valores
    df
    return df, pd


@app.cell
def _(df):
    df['Variaciones'] = df['Valores'].diff(periods=1)
    df
    return


@app.cell
def _(df):
    # Ahora hacemos el filtro de las variaciones negativas
    booleano = df.Variaciones < 0
    booleano
    return (booleano,)


@app.cell
def _(booleano, df):
    # Filtramos las variaciones
    df.loc[booleano , : ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ejercicio 2
    """)
    return


@app.cell
def _():
    _Valores = [200, 225, 232, 221, 243, 2556, 25]

    def retorno_semanal(cantidad_acciones, p_ganancia, p_no_ganancia):
        Inversion = [_x * cantidad_acciones for _x in _Valores]
        Ganancias = [y * 0.15 for y in Inversion]  # Calcular la cantidad invertida cada mes
        Perdidas = [y * -0.18 for y in Inversion]  # Variable local
        Valor_esperado = [_x * p_ganancia + y * p_no_ganancia for _x, y in zip(Ganancias, Perdidas)]
        return Valor_esperado  # Ahora calculamos las posibles ganancias cada dia  # En el resto de los casos el valor ganado es 0  # Ahora calculamos el valor esperado

    return (retorno_semanal,)


@app.cell
def _(retorno_semanal):
    retorno_semanal(20,p_ganancia=0.56, p_no_ganancia=0.44)
    return


@app.cell
def _(retorno_semanal):
    # La suma total luego de una semana es:
    sum(retorno_semanal(20,p_ganancia=0.56, p_no_ganancia=0.44))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Estarían conformes con esta cantidad ganada luego de una semana si el tiempo para coseguir el objetivo es 2 horas diarias todos los días
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ejercicio 3
    """)
    return


@app.cell
def _(pd):
    url = 'https://raw.githubusercontent.com/JJTorresDS/stocks-ds-edu/main/stocks.csv'
    df_1 = pd.read_csv(url, index_col=0)
    df_1.head()
    return (df_1,)


@app.cell
def _(df_1):
    for _x in df_1.columns:
        _col = df_1[_x]
        media = _col.mean()
        std = _col.std()
        var = _col.var()
        print('Accion:', _x, 'Media: ', media, 'Desviacion: ', std, 'Varianza: ', var)
        print('---------------------')
    return


@app.cell
def _(df_1):
    for _x in df_1.columns:
        _col = df_1[_x]
        max = _col.max()
        min = _col.min()
        print('Accion:', _x, 'Maximo: ', max, 'Minimo: ', min)
        print('---------------------')
    return


if __name__ == "__main__":
    app.run()
