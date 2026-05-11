import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    _Dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    _Valores = [200, 225, 232, 221, 243, 256, 255]
    import numpy as np
    Dif = np.diff(_Valores, n=1)
    for x, y in zip(_Dias[1:], Dif):
        if (x != 'Lunes') & (y < 0):
            print(x, y)
    return


@app.cell
def _():
    _Dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    _Valores = [200, 225, 232, 221, 243, 256, 255]
    import pandas as pd
    df = pd.DataFrame()
    df['Días'] = _Dias
    df['Valores'] = _Valores
    df['Variaciones'] = df['Valores'].diff(periods=1)
    df
    return


if __name__ == "__main__":
    app.run()
