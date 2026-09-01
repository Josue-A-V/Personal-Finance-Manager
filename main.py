# Public libraries
import ttkbootstrap as ttk
import pandas as pd

# Own libraries
import fp_widgets as fp

def close_window():
    root.destroy()

# === Log In GUI ===

login = fp.LogIn_GUI('a')

# Get csv names
csv_iyg = login.get("iyg")
csv_eu = login.get("eu")
csv_inv = login.get("inv")

# reading "ingresos y gastos" (iyg) and creating other variables
df_iyg = pd.read_csv(csv_iyg,index_col="i_iyg")

df_iyg["Neto"] = df_iyg["Ingreso"] - df_iyg["Salida"]
df_iyg["Uso Fecha"] = pd.to_datetime(df_iyg["Fecha"], dayfirst=True, format="%d/%m/%Y")
df_iyg["Año"] = df_iyg["Uso Fecha"].dt.year
df_iyg["Mes"] = df_iyg["Uso Fecha"].dt.month_name(locale="ES")

# reading "entradas usuales (eu)" database  
df_eu = pd.read_csv(csv_eu,index_col="i_eu")    

# reading "inversiones" (inv) database. +++++++++++ This module is not available yet
# inv = pd.read_csv(db_inv,index_col="i_inv")

root = ttk.Window(theme='darkly')
root.title(f"Finanzas personales {login.get("user")}")
# === Widgets ===
expenses_dashboard = fp.charts(root, "Salida" , df_iyg, "#E05E5E", "#F3C8C8","danger")
income_dashboard   = fp.charts(root, "Ingreso", df_iyg, "#69E05E", "#E4F3C8","success")

entryboxes = fp.iyg_Entryboxes_and_tail(root, df_iyg, csv_iyg, 6, "#535151", "#535151", "light gray", 6, df_eu, csv_eu, [expenses_dashboard,income_dashboard])

root.protocol("WM_DELETE_WINDOW", close_window)
root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
root.mainloop()
