import pandas as pd

# This methods eliminates accents
def qt(y):
    y_new = y
    try:
        for i in y:
            if tildes["Tilde"].isin([i]).any():
                y_new=str.replace(y_new, i, tildes["Notilde"][tildes["Tilde"] == i].values[0])
        return y_new        
    except:
        return y_new

tildes = pd.DataFrame({
    "Tilde": ["á","é","í","ó","ú"],
    "Notilde": ["a","e","i","o","u"]})    

# This method normalizes a text
def norm(texto):
    return qt(texto.lower())

# This method normalizes a text in a pandas dataframe
def norm_df(tabla, cat):

    return tabla[cat].str.lower().apply(qt)

# This method is able to execute a vlookup with tkinter variables and a pandas dataframe
def buscarv(box_categor_menor, cat_menor, varbox_categor_mayor, cat_mayor, tabla_busqueda):
    try:

        varbox_categor_mayor.set(tabla_busqueda[cat_mayor][norm_df(tabla_busqueda, cat_menor) == norm(box_categor_menor.get())].values[0])

        return True
    
    except:

        return False
