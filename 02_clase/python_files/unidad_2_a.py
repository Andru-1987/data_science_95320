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
    # Operadores Matematicos
    """)
    return


@app.cell
def _():
    _x = 15 + 1.3
    print(_x)
    return


@app.cell
def _():
    _x = 40
    y = 12
    add = _x + y
    sub = _x - y
    pro = _x * y
    div = _x / y
    print(add)
    print(sub)
    print(pro)
    print(div)
    return


@app.cell
def _():
    _a = 13
    _b = 12.0
    _c = _a + int(_b)
    print(_c)
    return


@app.cell
def _():
    _a = 13
    _b = 5
    _c = _a / _b
    print(_c)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Desafio generico
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lectura de informacion

    Los datos se encuentran en la siguiente link:
    [Data Acciones](https://raw.githubusercontent.com/JJTorresDS/stocks-ds-edu/main/stocks.csv)
    """)
    return


@app.cell
def _():
    import pandas as pd

    url = 'https://raw.githubusercontent.com/JJTorresDS/stocks-ds-edu/main/stocks.csv'
    df = pd.read_csv(url, index_col=0)
    print(df.head(5))
    return df, pd


@app.cell
def _(df):
    df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Miremos el tamaño de nuestro datraframe
    """)
    return


@app.cell
def _(df):
    df.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    11 filas x 14 columnas
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Symbol | Company Name                 |
    |--------|------------------------------|
    | MCD    | McDonald's                   |
    | SBUX   | Starbucks                    |
    | GOOG   | Google                       |
    | AMZN   | Amazon                       |
    | MSFT   | Microsoft                    |
    | JPM    | JPMorgan Chase & Co.         |
    | BAC    | Bank of America Corp         |
    | C      | Citigroup                    |
    | MAR    | Pharma Mar                   |
    | HLT    | Hoteles Hilton               |
    | RCL    | Royal Caribbean Cruises      |
    | V      | Visa Inc.                    |
    | MA     | Mastercard                   |
    | PYPL   | Paypal                       |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Parte 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Analizando el comportamiento de una serie de tiempo
    """)
    return


@app.cell
def _(df):
    (
        df['GOOG']
            .plot(
                kind='line',
                figsize=(10,6),
                xlabel='Fecha',
                ylabel='Precio Accion',
                title='Precio Accion vs Fecha')
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Se observa un comportamiento creciente entre el 01/01/21 hasta el 11/01/2021
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Extraccion usando indices booleanos
    """)
    return


@app.cell
def _(df):
    columnas = list(df.columns)
    google = [_x for _x in columnas if _x == 'GOOG']
    google
    return


@app.cell
def _(df):
    indice_col=list(df.columns=='GOOG')
    df_goog=df.loc[:,indice_col]
    df_goog # Hemos terminado
    return (df_goog,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Grafico interactivo
    """)
    return


@app.cell
def _(df_goog, pd):
    df_n= df_goog.copy()
    df_n['Fecha']= df_n.index
    df_n= df_n.reset_index(drop=True)
    df_n['Fecha']=pd.to_datetime(df_n['Fecha'])
    df_n
    return (df_n,)


@app.cell
def _(df_n):
    import plotly.express as px

    _fig = (
            px.line(
                data_frame=df_n,
                x='Fecha',
                y='GOOG',
                title='Comportamiento GOOGLE',
                labels={'Fecha': 'Fecha_dias', 'value': 'Precio (USD)'})
    )

    _fig.update_layout(paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF')
    _fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Parte 2
    """)
    return


@app.cell
def _(df_n):
    df_n
    return


@app.cell
def _(df_n):
    pasos = 2

    def my_fun(x):
        return x.iloc[-1] - x.iloc[0]

    
    # Hacemos la diferencia del valor actual - anterior
    df_n['Dif'] = df_n['GOOG'].rolling(window=pasos).apply(my_fun)  

    df_n
    return


@app.cell
def _(df_n):
    # Hacemos un filtro de cuando los valores de Dif <0
    index_bool= df_n.Dif<0
    index_bool
    return (index_bool,)


@app.cell
def _(df_n, index_bool):
    # Ahora podemos aplicar el filtro sobre el objeto data frame
    df_neg=df_n.loc[index_bool,:]
    df_neg
    return (df_neg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Solo existieron dos días donde la accion bajo de precio
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Graficando fechas donde ocurrio la bajada
    """)
    return


@app.cell
def _(df_n, df_neg):
    import matplotlib.pyplot as plt

    _fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df_n.Fecha, df_n.GOOG)
    ax.scatter(x=df_neg.Fecha, y=df_neg.GOOG, s=20, color='red', label='R')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio')
    ax.set_title('Precio Accion vs tiempo')
    ax.legend(loc='upper left')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Desafio

    Intenten hacer le mismo procedimiento para AMZN y observen si existe el mismo patron
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Con esto entonces podemos monitorear cuando una accion puede disminuir su valor
    """)
    return


if __name__ == "__main__":
    app.run()
