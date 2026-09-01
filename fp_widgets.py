import pandas as pd
import tkinter as tk
import ttkbootstrap as ttk
import matplotlib.pyplot as plt

from tkinter import messagebox
from ttkbootstrap import Style
from datetime import datetime
from logic import buscarv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LogIn_GUI:
    def __init__(self, main):
        self.main = main
        # Create users database columns: USER, PASSWORD and DB names
        self.list_users_columns = ["USER", "PASSWORD", "DB_iyg", "DB_eu", "DB_inv"]

# === Charge users database ===
        # if it exists, just charge it
        try:
            
            self.users = pd.read_csv("users.csv", index_col="id")

        # if it does not exist, create it and charge it
        except: 
            # Create dictionary with keys as columns
            temp_user_dict = {}

            for i in self.list_users_columns:

                temp_user_dict[i] = []

            # Convert dictionary to dataframe
            pd.DataFrame(temp_user_dict).to_csv("users.csv", index_label="id")

            # Charge database
            self.users = pd.read_csv("users.csv", index_col="id")

        # Create list with databases code
        self.list_database_code = ["iyg", "eu", "inv"]

# === GUI ===
    # === Create window ===
        self.root = ttk.Window(theme='darkly')
        self.root.title("Log in")
        self.root.geometry("500x300")
  

    # === Frames ===

        # Frame for logo
        self.frame_logo = ttk.Frame(self.root)
        self.frame_logo.pack(side="left", expand=True, fill="both")

        ttk.Label(self.frame_logo, text="Aqui va el logo").pack()

        # Frame for Entryboxes
        self.frame_entryboxes = ttk.Frame(self.root)
        self.frame_entryboxes.pack(pady=7)

        # Frame for bottons
        self.frame_btn = ttk.Frame(self.root)
        self.frame_btn.pack(pady=7)

# === Widgets ===
        # User Label
        self.user_l = ttk.Label(self.frame_entryboxes, text="Usuario", anchor="w")
        self.user_l.pack(pady=7, fill="x")

        # User Entrybox
        self.user = tk.StringVar()
        self.user_entry = ttk.Entry(self.frame_entryboxes, textvariable=self.user)
        self.user_entry.pack(padx=10, pady=7, fill="x")
        self.user_entry.focus_set()

        # Password Label
        self.password_l = ttk.Label(self.frame_entryboxes, text="Contraseña", anchor="w")
        self.password_l.pack(pady=7, fill="x")

        # Password Entrybox
        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(self.frame_entryboxes, show="*", textvariable=self.password)
        self.password_entry.pack(padx=10, pady=7, fill="x")

# === Buttons ===
        # Login button
        self.login_btn = ttk.Button(self.frame_btn, text="Ingresar", style="Success", command=lambda users = self.users: self.login_func(users))
        self.login_btn.pack(pady=7)

        # New user button
        self.new_user_btn = ttk.Button(self.frame_btn, text="Crear nuevo usuario", style='Info', command=self.new_func)
        self.new_user_btn.pack(pady=7, side="left", fill="both")

        # Guest button
        self.guest_btn = ttk.Button(self.frame_btn, text= "Ingresar como invitado", style='info', command=self.guest_func)
        self.guest_btn.pack(pady=7, side="right", fill="both")

        self.root.mainloop()


# === Methods ===

    # This method logs in when a correct user is given
    def login_func(self, users):

        # Find coincidence between user entries and "users" database. Hashing should be applied here to add security
        if ((users["USER"]==self.user.get()) & (users["PASSWORD"]==self.password.get())).any():

            # Get user entries
            user_name=self.user.get()
            password=self.password.get()

            # Destroy Log In window and open main app window
            self.root.destroy()

            # Create dictionary with user's specific databases
            self.db_dict = {}
            for i in self.list_database_code:
                x = "DB_" + i
                self.db_dict[i] = users[x][((users["USER"]==user_name) & (users["PASSWORD"]==password))].values[0]

            self.db_dict["user"] = user_name

                            
        # Message for incorrect or unfound user
        else:
            messagebox.showinfo(message = "Usuario o contraseña incorrecto")


    # This method opens the window to create a new user
    def new_func(self):

        self.new_user_root = ttk.Toplevel(self.main)
        self.new_user_root.title("Crear usuario nuevo")
        self.new_user_root.geometry("270x300")

        
        new_user_l = ttk.Label(self.new_user_root, text="Nuevo Usuario (Mínimo 5 caracteres)", anchor="w")
        new_user_l.pack(fill="x")

        new_user = ttk.Entry(self.new_user_root)
        new_user.pack(padx=10, pady=7, fill="x")

        new_password_l = ttk.Label(self.new_user_root, text="Nueva Contraseña", anchor="w")
        new_password_l.pack(fill="x")

    
        new_password = ttk.Entry(self.new_user_root, show="*")
        new_password.pack(padx=10, pady=7, fill="x")

        confirm_password_l = ttk.Label(self.new_user_root, text="Confirmar Contraseña", anchor="w")
        confirm_password_l.pack(fill="x")

        confirm_password = ttk.Entry(self.new_user_root, show="*")
        confirm_password.pack(padx=10, pady=7, fill="x")

        new_user_btn = ttk.Button(self.new_user_root, text="Crear nuevo usuario",style='Success', command=lambda: self.confirm_new_func(new_user.get(), new_password.get(), confirm_password.get()))
        new_user_btn.pack(pady=7)

        self.new_user_root.mainloop()


    # Validate new user data: non repeated user and confirmed password
    def confirm_new_func(self,new_user, new_pass, confirm_pass):

        # Correct condition: Valid user, Any password and its confirmation
        if new_pass == confirm_pass and confirm_pass and new_pass and not (self.users["USER"] == new_user).any() and len(new_user)>=5:
            
            # Pop up: New user succesfully created 
            messagebox.showinfo(title="Usuario nuevo", message=f"¡Nuevo usuario [{new_user}] creado con éxito!")

            # creation of new user's Databases:

            # parameters for db's names
            user_id = new_user[:(len(new_user)-2)] #users code: all characters except last two
            creation_moment = datetime.now().strftime("%S%M%H_%d_%m_%Y") # Date of creation for unique identification

            user_new = {} # Dictionary to save as an Entry for "users" database
            temp_dict_code = {} # Dicitonary to temporary store databases names to create them

            # for loop for database name: user first three characters + _db_ + code + _ + user creation date
            for code, col in zip(self.list_database_code, self.list_users_columns[2:len(self.list_users_columns)]):
                                 
                new_database = user_id + "_db_" + code + "_" + creation_moment + ".csv"
                user_new.update({col:new_database})
                temp_dict_code.update({col:new_database})

            # add new user to users database
            user_new.update({"USER":new_user, "PASSWORD":new_pass}) #dictionary with data
            self.users.loc[len(self.users)] = user_new #finally add dicitonary to users database
            self.users.to_csv("users.csv") #save csv with new information

            # === Create .csv dbs for new user ===

            # iyg database creation
            pd.DataFrame({"Fecha":[], 
                        "Categoría general":[], 
                        "Categoría específica":[], 
                        "Detalle":[], 
                        "Salida":[], 
                        "Ingreso":[]}).to_csv(temp_dict_code["DB_iyg"], index_label="i_iyg")
        
            # eu database creation
            pd.DataFrame({"Categoría general":[], 
                        "Categoría específica":[], 
                        "Detalle":[]}).to_csv(temp_dict_code["DB_eu"], index_label="i_eu")

            # inversiones database creation
            pd.DataFrame({"Fecha de Inicio":[],
                          "Fecha de cierre":[],
                          "Días":[],
                          "Detalle":[],
                          "Tipo":[],
                          "Monto":[],
                          "Periodicidad Cupones":[],
                          "Tasa anual":[],
                          "Tasa impuesto":[],
                          "Tasa real (con impuestos)":[],
                          "Intereses Banco":[],
                          "Impuesto Banco":[],
                          "Interes Final":[],
                          "Cupón mensual":[],
                          "Cupón residual":[]}).to_csv(temp_dict_code["DB_inv"], index_label="i_inv")

            try:
                self.new_user_root.destroy()
            except:
                pass
            
        # incorrect condition: passwords don't match or are empty 
        elif new_pass != confirm_pass or not confirm_pass or not new_pass:
            messagebox.showinfo(title="Contraseña incorrecta", message=f"Contraseña incorrecta")

        # incorrect condition: user already exists or doesn't have at least five characters
        else:
            messagebox.showinfo(title="Usuario ya resgistrado", message=f"El usuario que intenta registrar ya existe o no es válido")


    # This method creates a guest user if it doesn't exist, logs in on it otherwise
    def guest_func(self):

        # if guest user does not exist
        if not (self.users["USER"] == "fp_guest").any():

            self.confirm_new_func("fp_guest","fp_guest_password","fp_guest_password")

        self.user.set("fp_guest")
        self.password.set("fp_guest_password")
        self.login_func(self.users)

    # A method to externally call for username and databases
    def get(self,i):
        return self.db_dict[i]


class charts():
    def __init__(self, root, entry_type, database, color_graf, color_frame_bg, color_btn):
        self.root = root

        # Type of entry: Salida ("Expenses") o Ingreso ("Incomes")
        self.entry_type = entry_type

        # Pivot table
        self.df_pivot_table = database.groupby(["Año", "Mes",  "Categoría general","Categoría específica"]).agg({
                        "Salida":"sum",
                        "Ingreso": "sum",
                        "Neto":"sum"}).sort_values(["Año", "Mes", "Categoría general"])

        # GUI color variables
        self.color_graf = color_graf
        self.color_frame_bg = color_frame_bg
        self.color_btn = color_btn

        # Main Frame
        self.frame_main = ttk.Frame(self.root, bootstyle='secondary',  height=50)
        self.frame_main.pack(expand=True, fill="both", side="top")

        # Groupby parameters
        self.list_agrupar_bar = ["Categoría general"] #,"Categoría específica"
        self.list_agrupar_histogram = ["Año","Mes"]

        # Filtered lists
        self.list_filtered_year         = self.df_pivot_table[self.df_pivot_table[entry_type]>0].index.get_level_values("Año").unique().to_list()
        self.list_filtered_month        = self.df_pivot_table[self.df_pivot_table[entry_type]>0].index.get_level_values("Mes").unique().sort_values().to_list()
        self.list_filtered_general      = self.df_pivot_table[self.df_pivot_table[entry_type]>0].index.get_level_values("Categoría general").unique().sort_values().to_list()
        self.list_filtered_especifica   = self.df_pivot_table[self.df_pivot_table[entry_type]>0].index.get_level_values("Categoría específica").to_list()

        # Filter
        self.tuple_every_filter = (self.list_filtered_year, self.list_filtered_month, self.list_filtered_general)

        # Initial data
        self.df_bar_data        = self.df_pivot_table[self.entry_type].loc[self.tuple_every_filter].groupby(self.list_agrupar_bar).sum().sort_values()
        self.df_histogram_data  = self.df_pivot_table[self.entry_type].loc[self.tuple_every_filter].groupby(self.list_agrupar_histogram).sum()

# === Charts ===
        self.fig,self.ax= plt.subplots(1,2, figsize = (7,1.5))

        self.draw_charts(self.df_bar_data, self.df_histogram_data)

        self.ax[0].set_axisbelow(True)
        self.ax[1].set_axisbelow(True)
        
        for i in ["right", "bottom", "left", "top"]:
            self.ax[0].spines[i].set_visible(False)
            self.ax[1].spines[i].set_visible(False)

        # Pack charts in window
        self.charts_canvas = FigureCanvasTkAgg(self.fig, self.frame_main).get_tk_widget()
        self.charts_canvas.pack(side="left", expand=True, fill="both", padx=10, pady=10)


# === Buttons ===
        self.dict_filter_type = {0:False,1:False,2:False}
        self.dict_filter_type_text={}
        self.list_frames = []
        self.dict_buttons = {}

        for j, true_filter in zip(reversed(range(0,len(self.tuple_every_filter))), reversed(self.tuple_every_filter)): 
            # Button's frame
            frame = ttk.Frame(self.frame_main, bootstyle = 'primary')
            self.list_frames.append(frame)
            frame.pack(side="left", expand=True, fill="y", padx=3, pady=7)

            # Label
            Label = ttk.Label(frame, text=self.df_pivot_table.index.names[j],bootstyle='primary-inverse', anchor='center')
            Label.pack(side="top", fill="x", pady=7)

            # Filter type dictionary and button
            self.dict_filter_type_text[j] = tk.StringVar(value="Selección individual")
            ttk.Button(frame, bootstyle='secondary', textvariable = self.dict_filter_type_text[j], command= lambda j=j: self.filter_type_mult_func(j) ).pack(side="top", padx=5, pady=5, fill="both")

            # === Categories' Buttons ===

            # Buttons' dictionary
            self.dict_buttons[j] = dict()

            for i in true_filter:
                boton = ttk.Button(frame, text=i, command=lambda cat=i,lista=true_filter,j=j :self.filter_category(cat, lista,j), bootstyle = self.color_btn)
                self.dict_buttons[j][i] = boton
                self.dict_buttons[j][i].pack(side="top", fill = 'x', expand = True, padx = 3, pady=1)

        self.filter_type_mult_func(2) # Cambiar categoria general a seleccion multiple

# === Methods ===

    # This method resets filtered lists to their original values (no filter)
    def lists_valores_base(self):
        self.list_filtered_general[:]   = self.df_pivot_table[self.df_pivot_table[self.entry_type]>0].index.get_level_values("Categoría general").unique().to_list()
        self.list_filtered_month[:]     = self.df_pivot_table.index.get_level_values("Mes").unique().sort_values().to_list()
        self.list_filtered_year[:]      = self.df_pivot_table.index.get_level_values("Año").unique().to_list()

    # This method switches the filter type between seleccion "multiple" (True) o "individual" (False)
    def filter_type_mult_func(self, j):

        if self.dict_filter_type[j]:
            self.dict_filter_type[j] = False
            self.dict_filter_type_text[j].set("Selección individual")
        
        elif not self.dict_filter_type[j]:
            self.dict_filter_type[j] = True
            self.dict_filter_type_text[j].set("Selección múltiple")
            if j == 2:
                try:
                    self.list_agrupar_bar.remove("Categoría específica")
                except:
                    None


    # Method to apply filters by button
    def filter_category(self, cat,lista, j):
        # Change filtered list
        if not self.dict_filter_type[j]: # Seleccion individual
            if j == 2 and "Categoría específica" not in self.list_agrupar_bar:
                self.list_agrupar_bar.append("Categoría específica")

            lista.clear()
            lista.append(cat)    

        else: # Seleccion multiple
            if cat in lista:
                lista.remove(cat)
            else:
                lista.append(cat)

        # Change button's color depending on filter
        for i in self.dict_buttons[j].keys():
            if i not in lista:
                self.dict_buttons[j][i].configure(bootstyle='primary-outline')
            else:
                self.dict_buttons[j][i].configure(bootstyle=self.color_btn)

        self.update_chart_data()

    # Method to update chart data based on current filter
    def update_chart_data(self):
        try:

            bar_height = self.df_pivot_table[self.entry_type].loc[self.tuple_every_filter].groupby(self.list_agrupar_bar).sum().sort_values()
            hist_height = self.df_pivot_table[self.entry_type].loc[self.tuple_every_filter].groupby(self.list_agrupar_histogram).sum()

        except:
            bar_height = pd.Series([0,0], index=["No se encontaron datos","No se encontaron datos"])
            bar_height.index.name = self.list_agrupar_bar[-1]
            hist_height = pd.Series([0])

        self.draw_charts(bar_height, hist_height)     

    # Method to redraw charts based on current filtered data
    def draw_charts(self, bar_height, hist_height):

        self.ax[0].clear()
        self.ax[1].clear()    

        etiquetas = bar_height.index.get_level_values(self.list_agrupar_bar[-1]).unique().to_list()

        sal_barras = self.ax[0].bar(etiquetas, bar_height, width = 0.5, color = self.color_graf)
        sal_hist = self.ax[1].hist(hist_height, bins = 10, color = self.color_graf)

        self.ax[0].set_title(f"{self.entry_type} por categoría")
        self.ax[1].set_title(f"Histograma de {self.entry_type} totales por mes")

        self.ax[0].bar_label(sal_barras)

        try:
            self.ax[0].set_ylim(top = max(bar_height)*1.2)
        except:
            None
        self.ax[0].tick_params(
            bottom = False,
            left = False
        )
     
        self.ax[0].grid(axis = "y", linewidth = 0.4) 
        self.ax[1].grid(axis = "y", linewidth = 0.4)

        self.ax[1].tick_params(
            bottom = False,
            left = False
        )
        
        self.fig.tight_layout(h_pad=2)

        self.fig.canvas.draw()

    # Method to update when there is a new data entry, a data is modified or erased
    def update_by_newentry(self, database):
        self.df_pivot_table = database.groupby(["Año", "Mes",  "Categoría general","Categoría específica"]).agg({
                        "Salida":"sum",
                        "Ingreso": "sum",
                        "Neto":"sum"}).sort_values(["Año", "Mes", "Categoría general"])        
        

        # Update self.dict_buttons 
        for j,i in zip(reversed(range(0, 3)),["Categoría general", "Mes", "Año"]):
            nuevo = set(self.df_pivot_table[self.df_pivot_table[self.entry_type]>0].index.get_level_values(i))-set(self.dict_buttons[j].keys())
            quitar = set(self.dict_buttons[j].keys()) - set(self.df_pivot_table[self.df_pivot_table[self.entry_type]>0].index.get_level_values(i))
            
            if nuevo:
                bot_nueva = nuevo.pop()
                boton = ttk.Button(self.list_frames[len(self.list_frames)-1-j], text=bot_nueva, command=lambda cat=bot_nueva,lista=self.tuple_every_filter[j],j=j :self.filter_category(cat, lista,j), bootstyle='primary')
                self.dict_buttons[j][bot_nueva]=boton
                self.dict_buttons[j][bot_nueva].pack(side="top", fill="x", expand=True, padx = 3, pady=1)
                self.filter_category(bot_nueva, self.tuple_every_filter[j], j)

            if quitar:
                bot_quitar = quitar.pop()

                if bot_quitar in self.tuple_every_filter[j]:
                    self.filter_category(bot_quitar, self.tuple_every_filter[j], j)

                self.dict_buttons[j][bot_quitar].destroy()
                self.dict_buttons[j].pop(bot_quitar, None)
        
        self.update_chart_data()


# === Entry boxes and treeview class ===
class Entryboxes_and_tail():
    def __init__(self, root, own_dataframe, own_csv, n_columns,color_frame_bg, color_frame_bg_2, font_color,n_columns_showing):
        self.dataframe_own = own_dataframe

        self.csv_own = own_csv

        self.list_n_columns   = self.dataframe_own.columns[0:n_columns].tolist() # Define list of columns showing
        self.n_columns_showing = n_columns_showing # Define number of columns showing

        self.color_frame_bg = color_frame_bg
        self.color_frame_bg_2 = color_frame_bg_2
        

# === Frames ===
        self.frame_main = ttk.Frame(root)
        self.frame_main.pack(fill='both', expand = True)


        self.tree_frame = ttk.Frame(self.frame_main)
        self.tree_frame.pack(pady=7,padx=7)

        self.boxes_frame = ttk.Frame(self.frame_main)
        self.boxes_frame.pack(pady=7,padx=7, fill="x")

        self.buttons_frame = ttk.Frame(self.boxes_frame)

# === Treeview ===

        self.datostree = ttk.Treeview(self.tree_frame, columns = self.list_n_columns,show = "headings", height=self.n_columns_showing)

        # Create Treeview columns
        for i in self.list_n_columns:
            self.datostree.heading(i,text = i)

        # Pack Treeview
        self.datostree.pack()


        # Introduce already existing data into the Treeview
        for i in self.dataframe_own.tail().itertuples(index=False):

            self.datostree.insert(parent="",index="end" ,values = i)

        # Treeview bind
        self.datostree.bind("<Button-1>", lambda event, treeview = self.datostree, dataframe = self.dataframe_own, csv = self.csv_own  : self.click_treeview(event, treeview, dataframe, csv))


# === Dicitonaries ===

        # App states dictionary
        self.state_dict = {"Base" : False, "Modificar": False, "mod_index": 0, "Already select" : False, "Borrar": False}
        self.var_state = "Base"
        
        # Variables and widgets storing dictionaries

        self.dict_current_treeview = {False: self.datostree} # False siempre representa al estado mas base de la aplicacion
        self.dict_current_dataframe = {False:{"Dataframe" : self.dataframe_own, "csv": self.csv_own}} # False siempre representa al estado mas base de la aplicacion

        self.dict_columns_label = {}
        self.dict_columns_entry = {}
        self.dict_varbox = {}

        self.dict_buttons_config = {}

# === Create Entry boxes and Labels ===

        # for loop to createLabels, Entryboxes and variables for Entryboxes
        cont = 0
        cont_row = 0
        cont_col = 0

        for i in self.list_n_columns:
    
            self.boxes_frame.columnconfigure(cont, weight=1)

            self.dict_columns_label[i] = ttk.Label(self.boxes_frame, text = i)
            self.dict_columns_label[i].grid(row = cont_row,column = cont_col, sticky = "wne")

            self.dict_varbox[i] = tk.StringVar()

            self.dict_columns_entry[i] = ttk.Entry(self.boxes_frame)
            self.dict_columns_entry[i].grid(row=cont_row + 1, column = cont_col, pady = 5)
            self.dict_columns_entry[i].configure(textvariable = self.dict_varbox[i])

            cont += 1

            cont_row = 2 * (cont // 7)
            cont_col = cont % 7

        list(self.dict_columns_entry.values())[0].focus_set()

        self.buttons_frame.grid(row=0,column=cont, rowspan=2, sticky="nes")

# === Buttons ===

        self.button_borrar      = ttk.Button(self.buttons_frame, width = 15,bootstyle = "danger-outline"  ,text="Borrar",    command=self.borrar_func)
        self.button_modificar   = ttk.Button(self.buttons_frame, width = 15,bootstyle = "warning-outline" ,text="Modificar", command=self.mod_func)

        self.button_borrar      .grid(row=1, column = 1, padx= 5, pady= 2)
        self.button_modificar   .grid(row=1, column = 2, padx= 5, pady= 2)    

    
        self.dict_buttons_config = {"Borrar" :    {"Btn":self.button_borrar,    False : "Borrar",    True : "Borrando"},
                                    "Modificar" : {"Btn":self.button_modificar, False : "Modificar", True : "Modificando"}} 

# === Last entrybox bind
        self.dict_columns_entry[self.list_n_columns[-1]].bind("<KeyPress>",self.enter)


# === Methods ===
    
    # Basic validation method
    def validar(self):

        if any(x.get() == "" for x in self.dict_columns_entry.values()):
            entry = {}

            for i in self.list_n_columns:
                entry[i] = self.dict_columns_entry[i].get()

        else:
            return True

    # Method to save entry as a dictionary
    def save_dict(self):
        dict_entry = {}

        for i in self.list_n_columns:
            dict_entry[i] = self.dict_columns_entry[i].get()
        
        return dict_entry

    # Method to save entry in the dataframe and csv
    def save_entry(self, df, csv):
        if self.validar():

            dict_entry = self.save_dict() # Crea y guarda el diccionario con las entradas necesarias segun el modo (iyg o eu)

            df.loc[len(df) + self.state_dict["mod_index"]] = dict_entry # Agrega la entrada nueva al dataframe

            df.to_csv(csv, index=True) # Guarda y sobreescribe el dataframe en el csv

            self.update_treeview(df) # Actualiza la visualizacion del treeview

            self.reset()

    # Funcion para guardar entrada cuando se presiona Tab
    def enter(self, event):

        if event.state == 8 and event.keysym == "Tab":

            self.save_entry(self.dict_current_dataframe[self.state_dict[self.var_state]]["Dataframe"], self.dict_current_dataframe[self.state_dict[self.var_state]]["csv"])

    # Funcion para actualizar datos en el treeview
    def update_treeview(self, dataframe):
        self.erase_treeview()

        dataframe_data_view = dataframe.tail()

        self.fill_treeview(dataframe_data_view)

    def erase_treeview(self):
        try:
            for i in range(0,5):

                self.dict_current_treeview[self.state_dict[self.var_state]].delete(self.dict_current_treeview[self.state_dict[self.var_state]].get_children()[0])

        except:
            pass

    def fill_treeview(self, data_view):

        for i in data_view.itertuples(index=False):
            self.dict_current_treeview[self.state_dict[self.var_state]].insert(parent="",index="end" ,values = i)
    
    # Method to clear entry boxes
    def clear_entryboxes(self):

        for var in self.dict_varbox.values():
            var.set("")

    # Method to reset other variables
    def reset(self):

        self.clear_entryboxes()

        self.state_dict["Already select"] = False
        self.state_dict["mod_index"] = 0
 

# === States methods ===

    # === 1. Method to activate or deactivate Mod state ===
    def mod_func(self):

        # === Deactivate Modificar state ===
        if self.state_dict["Modificar"]:
            self.state_dict["Modificar"] = False

            button_color ="warning-outline"
            color2 =      "default"
            
            # If something was selected but not modified
            if self.state_dict["Already select"]:

                # Return existing and unaltered data
                self.dict_current_dataframe[self.state_dict[self.var_state]]["Dataframe"].iloc[len(self.dict_current_dataframe[self.state_dict[self.var_state]]["Dataframe"]) + self.state_dict["mod_index"]] = self.exis_entry # cambiar self.dataframe.own por algo que permita cambiar segun por eu

                # Reset entryboxes and treeview
                self.clear_entryboxes()
                self.update_treeview(self.dict_current_dataframe[self.state_dict[self.var_state]]["Dataframe"])

            self.state_dict["Already select"] = False
            self.state_dict["mod_index"] = 0


        # === Activate Modificar state ===
        else:
            self.state_dict["Modificar"] = True

            button_color = "warning"
            color2 =       "warning" 
            
            # Deactivate Borrar state
            if self.state_dict["Borrar"]:
                self.borrar_func()

        # Switch button's color and text
        self.change_color("Modificar", button_color, color2)

    # === 2. Method to activate or deactivate Borrar state ===
    def borrar_func(self):

        # === Deactivate Borrar state ===
        if self.state_dict["Borrar"]:
            self.state_dict["Borrar"] = False

            button_color = "danger-outline"
            color2 =       "default"

        # === Activate Borrar state ===
        else:
            self.state_dict["Borrar"] = True

            button_color = "danger"
            color2 =       "danger"

            # Deactivate Modificar state
            if self.state_dict["Modificar"]:
                self.mod_func()

        # Switch button's color and text
        self.change_color("Borrar", button_color, color2)

    # === Method to access existing entry ===
    def modificar(self, treeview, dataframe, event):

        if self.state_dict["Already select"]:
            self.state_dict["Already select"] = False

            dataframe.iloc[self.state_dict["mod_index"]] = self.exis_entry

            self.reset()
            self.update_treeview(dataframe)       

        try:
            row = treeview.index(treeview.identify_row(event.y))

            self.state_dict["mod_index"] = row - 5

            self.state_dict["Already select"] = True

            self.exis_entry = {}
            self.exis_entry = dataframe.iloc[len(dataframe) + self.state_dict["mod_index"]]

            dataframe.iloc[len(dataframe) + self.state_dict["mod_index"]] = None

            self.update_treeview(dataframe)

            for col, var in zip(self.exis_entry, self.dict_varbox.values()):

                    var.set(col)

        except:
            pass

    # === Method to erase existing entry ===
    def borrar(self, treeview, dataframe, csv, event):

        fila = treeview.index(treeview.identify_row(event.y))

        borrar_index = fila - 5

        borrar_entry = dataframe.iloc[borrar_index].to_string(index=False)

        if messagebox.askyesno(title="Borrar entrada", message=f"¿Borrar? \n {borrar_entry}"):

            var_index_name = dataframe.index.name
            
            dataframe.drop([len(dataframe) + borrar_index], inplace = True)
            dataframe.reset_index(drop=True, inplace=True)

            dataframe.index.name = var_index_name
            dataframe.to_csv(csv, index = True)

            self.update_treeview(dataframe)


    # === Method to switch buttons' color === 
    def change_color(self, button, btn_style, frame_style):
        
        # Button's color
        self.dict_buttons_config[button]["Btn"].configure(bootstyle=btn_style)

        # Button's text
        self.dict_buttons_config[button]["Btn"].configure(text = self.dict_buttons_config[button][self.state_dict[button]])

        # Frame's color
        self.boxes_frame.configure(bootstyle=frame_style)


    # === Treeview binding method for Modificar y Borrar ===
    def click_treeview(self, event, treeview, dataframe, csv):

        if self.state_dict["Modificar"]:

            self.modificar  (treeview, dataframe, event)

        elif self.state_dict["Borrar"]:

            self.borrar     (treeview, dataframe, csv, event)


# === Child class from Entryboxes_and_tail ===
# This class contains specific quality-of-life methods to make data entry easier. iyg stands for "Entradas y Gastos" (Income and Expenses)
class iyg_Entryboxes_and_tail(Entryboxes_and_tail):
    def   __init__(self, root, iyg_dataframe, own_csv, n_columns, color_frame_bg, color_frame_bg_2, font_color, columns_showing, eu_dataframe, eu_csv, chart_list):
        super().__init__(root, iyg_dataframe, own_csv, n_columns, color_frame_bg, color_frame_bg_2, font_color, columns_showing)

        self.dataframe_iyg = iyg_dataframe
        self.dataframe_eu = eu_dataframe

        self.csv_eu = eu_csv

        self.list_esp_eu = self.dataframe_eu["Categoría específica"].unique().tolist()
        self.list_gen_eu = self.dataframe_eu["Categoría general"].unique().tolist()

        self.list_n_eu_columns = self.list_n_columns[1:4]

        self.list_chart = chart_list


# === Create "Entradas Usuales" (Usual Entries) treeview ===
        self.treeview_eu = ttk.Treeview(self.tree_frame, columns = self.list_n_eu_columns,show = "headings", height=len(self.list_n_eu_columns))

        # Create Treeview columns
        for i in self.list_n_eu_columns:
            self.treeview_eu.heading(i,text = i)

        # Introduce already existing data into the Treeview

        for i in self.dataframe_eu.itertuples(index=False):
            self.treeview_eu.insert(parent="",index="end" ,values = i)

        # Treeview bind
        self.treeview_eu.bind("<Button-1>", lambda event, treeview = self.treeview_eu, dataframe = self.dataframe_eu,csv = self.csv_eu : self.click_treeview(event, treeview, dataframe, csv))


# === Add specific states for iyg ===
        self.state_dict.update({"Entradas Usuales": False,
                                "flag_especifica_buscarv": False,
                                "flag_general_buscarv": False})

        self.var_state = "Entradas Usuales"

        self.dict_current_treeview.update({True:self.treeview_eu})

        # Update dicitonary with multiple dataframes used depending on self.state_dict["Entradas Usuales"]
        self.dict_current_dataframe.update({True: {"Dataframe" : self.dataframe_eu, "csv": self.csv_eu}})


        self.str_var_list = ["Detalle", "Categoría específica", "Categoría general"] # String variables list
        self.num_var_list = ["Salida", "Ingreso"] # Float variables list (Moneda)

        try:
            self.dict_varbox["Fecha"].set(self.dataframe_own["Fecha"].iloc[-1])
        except:
            self.dict_varbox["Fecha"].set(datetime.today().strftime("%d/%m/%Y"))

# === Change Entrybox to combobox ===
        self.dict_columns_entry["Categoría específica"].destroy()
        self.dict_columns_entry["Categoría general"]   .destroy()

        self.dict_columns_entry["Categoría específica"] = ttk.Combobox(self.boxes_frame, values = self.list_esp_eu, textvariable=self.dict_varbox["Categoría específica"])
        self.dict_columns_entry["Categoría general"]    = ttk.Combobox(self.boxes_frame, values = self.list_gen_eu, textvariable=self.dict_varbox["Categoría general"])

        self.dict_columns_entry["Categoría específica"].grid(row = 1, column = 2)
        self.dict_columns_entry["Categoría general"]   .grid(row = 1, column = 3)

# === Switch Entryboxes to correct order
        self.dict_columns_entry["Detalle"]          .forget()

        self.dict_columns_label["Detalle"]          .forget()
        self.dict_columns_label["Categoría general"].forget()

        self.dict_columns_entry["Detalle"]          .grid(row = 1, column = 1, padx = 10)

        self.dict_columns_entry["Detalle"]              .lift(self.dict_columns_entry["Fecha"])
        self.dict_columns_entry["Categoría específica"] .lift(self.dict_columns_entry["Detalle"])
        self.dict_columns_entry["Categoría general"]    .lift(self.dict_columns_entry["Categoría específica"])

        self.dict_columns_label["Detalle"]          .grid(row = 0, column = 1, sticky = "wne")
        self.dict_columns_label["Categoría general"].grid(row = 0, column = 3, sticky = "wne")

#  === Create "Entradas Usuales" (Usual Entries) Button ===
        self.button_eu = ttk.Button(self.buttons_frame, width = 15, text="Entradas Usuales", bootstyle="info", command=self.eu_func)

        self.button_eu.grid(row=0, column = 1, padx= 5, pady= 2, columnspan=2, sticky="we")

        self.dict_buttons_config.update({"Entradas Usuales" : {"Btn": self.button_eu, False : "Entradas Usuales", True : "Registro Salidas e Ingresos"}}) 
     
# === Assign specific methods to Entryboxes ===

    # Methods for saving entries
        self.dict_columns_entry["Fecha"]                .bind("<KeyPress>", self.enter_robust)
        self.dict_columns_entry["Detalle"]              .bind("<KeyPress>", self.enter_robust)
        self.dict_columns_entry["Categoría específica"] .bind("<KeyPress>", self.enter_robust)
        self.dict_columns_entry["Categoría general"]    .bind("<KeyPress>", self.enter_robust)
        self.dict_columns_entry["Salida"]               .bind("<KeyPress>", self.enter_sal)
        self.dict_columns_entry["Ingreso"]              .bind("<KeyPress>", self.enter_ing)

    # Quality-of-life methods
        self.dict_columns_entry["Detalle"]              .bind("<KeyRelease>", self.rell_detalle)
        self.dict_columns_entry["Categoría específica"] .bind("<KeyRelease>", self.rell_esp)
        self.dict_columns_entry["Categoría general"]    .bind("<KeyRelease>", self.rell_gen)

# === Edited Methods ===
    def validar(self):
        cont = True

        if not self.state_dict["Entradas Usuales"]:

            # Validar que los espacios para categorias y detalle esten llenos
            for i in self.str_var_list:

                cont *= bool(self.dict_columns_entry[i].get())

            # Validar que los espacios anteriores y al menos un espacio para dinero esten llenos
            cont = cont * (bool(float(self.dict_columns_entry["Salida"].get() or False)) ^ bool(float(self.dict_columns_entry["Ingreso"].get() or False)))

        return cont


    def save_dict(self):
        entry={}
        
        # Fill dictionary with string variables
        for i in self.str_var_list: #["Detalle", "Categoría específica", "Categoría general"]
            entry[i] = self.dict_columns_entry[i].get()

        if not self.state_dict["Entradas Usuales"]: # This variables should only be filled in Base mode
            # Fill "Fecha" (Date)
            entry.update({"Fecha": self.dict_columns_entry["Fecha"].get() or self.dataframe_iyg["Fecha"].iloc[-1]})

            # Fill float variables
            for i in self.num_var_list: #["Salida", "Ingreso"]
                entry[i] = float(self.dict_columns_entry[i].get() or 0)

            # Date variables needed for the dashboard, not visible to user
            uso_fecha_var = pd.to_datetime(entry["Fecha"], dayfirst=True)
            entry.update({  "Neto":entry["Ingreso"]-entry["Salida"],
                            "Uso Fecha": uso_fecha_var,
                            "Año":uso_fecha_var.year,
                            "Mes": uso_fecha_var.month_name(locale="ES")})
            
        return entry

    def enter(self, event):
        pass

    def update_treeview(self, dataframe):
        self.erase_treeview()

        if not self.state_dict["Entradas Usuales"]:
            dataframe_data_view = dataframe.tail()

        elif self.state_dict["Entradas Usuales"]:
            dataframe_data_view = dataframe

        self.fill_treeview(dataframe_data_view)

        for dash in self.list_chart:
            dash.update_by_newentry(self.dataframe_iyg)

    def clear_entryboxes(self):
        super(iyg_Entryboxes_and_tail,self).clear_entryboxes()

        try:
            self.dict_varbox["Fecha"].set(self.dataframe_own["Fecha"].iloc[-1])
        except:
            self.dict_varbox["Fecha"].set(datetime.today().strftime("%d/%m/%Y"))

# === Edited state methods ===

    def modificar(self, treeview, dataframe, event):

        if self.state_dict["Already select"]:
            self.state_dict["Already select"] = False

            dataframe.iloc[self.state_dict["mod_index"]] = self.exis_entry

            self.reset()
            self.update_treeview(dataframe)       

        try:
            row = treeview.index(treeview.identify_row(event.y))

            if not self.state_dict["Entradas Usuales"]:
                self.state_dict["mod_index"] = row - 5
                lista_var = self.dict_varbox.values()

            elif self.state_dict["Entradas Usuales"]:
                self.state_dict["mod_index"] = row - len(dataframe)
                lista_var = list(self.dict_varbox.values())[1:4] 

            self.state_dict["Already select"] = True

            self.exis_entry = {}
            self.exis_entry = dataframe.iloc[len(dataframe) + self.state_dict["mod_index"]]

            dataframe.iloc[len(dataframe) + self.state_dict["mod_index"]] = None

            self.update_treeview(dataframe)

            for col, var in zip(self.exis_entry, lista_var):
                    var.set(col)
        except:
            pass


# === New methods ===

    # === Quality-of-life (QoL) ===

    # Normalize "Detalle", applies a vlookup on "Categoria especifica" and "Categoria general"
    def rell_detalle(self, event):
        if event.keysym != "Tab":
        
            if buscarv(self.dict_columns_entry["Detalle"], "Detalle", self.dict_varbox["Detalle"], "Detalle", self.dataframe_eu):
                if not self.state_dict["Modificar"]:
                    buscarv(self.dict_columns_entry["Detalle"], "Detalle", self.dict_varbox["Categoría específica"], "Categoría específica", self.dataframe_eu)
                    self.state_dict["flag_especifica_buscarv"] = True

                    buscarv(self.dict_columns_entry["Categoría específica"], "Categoría específica", self.dict_varbox["Categoría general"], "Categoría general", self.dataframe_eu)
                    self.state_dict["flag_general_buscarv"] = True

            elif self.state_dict["flag_especifica_buscarv"]:
                self.dict_varbox            ["Categoría específica"].set("")
                self.state_dict["flag_especifica_buscarv"] = False
                
                if self.state_dict["flag_general_buscarv"]:
                    self.dict_varbox        ["Categoría general"].set("")
                    self.state_dict["flag_general_buscarv"] = False


    # Normalize "Categoria especifica" and applies vlookup on "Categoria general"
    def rell_esp(self, event):
        if event.keysym != "Tab":
            self.state_dict["flag_especifica_buscarv"] = False
        if buscarv(self.dict_columns_entry["Categoría específica"], "Categoría específica", self.dict_varbox["Categoría específica"], "Categoría específica", self.dataframe_eu): 

            if not self.state_dict["Modificar"]:
                buscarv(self.dict_columns_entry["Categoría específica"], "Categoría específica", self.dict_varbox["Categoría general"], "Categoría general", self.dataframe_eu)
                self.state_dict["flag_general_buscarv"] = True

        elif self.state_dict["flag_general_buscarv"]:
            self.dict_varbox["Categoría general"].set("")

            self.state_dict["flag_general_buscarv"] = False


    # Normalize "Categoria general"
    def rell_gen(self, event):     
        if event.keysym != "Tab":
            self.state_dict["flag_general_buscarv"] = False

        buscarv(self.dict_columns_entry["Categoría general"], "Categoría general", self.dict_varbox["Categoría general"], "Categoría general", self.dataframe_eu)


    # === Methods for saving entries ===

    # You can save by pressing Shift + Enter in any entrybox
    def enter_robust(self, event):
        if event.state == 9 and event.keysym == "Return": 
            self.save_entry(self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["Dataframe"], 
                            self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["csv"] )


    # Method for saving entry by pressing tab in "Salida" entrybox
    def enter_sal(self, event):
        if event.state == 8 and event.keysym == "Tab" and self.validar():

            self.save_entry(self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["Dataframe"], 
                            self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["csv"])

        self.enter_robust(event)


    # Method for saving entry by pressing tab in "Ingreso" entrybox
    def enter_ing(self,event):
        if event.state == 8 and event.keysym == "Tab" and self.validar():

            self.save_entry(self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["Dataframe"], 
                            self.dict_current_dataframe[self.state_dict["Entradas Usuales"]]["csv"])

        self.enter_robust(event)


    # === Method to activate "Entradas Usuales" state ===
    def eu_func(self):

        if self.state_dict["Modificar"]:
            self.mod_func()
        elif self.state_dict["Borrar"]:
            self.borrar_func()


        if self.state_dict["Entradas Usuales"]:

            self.state_dict["Entradas Usuales"] = False

            color = "info"

            # Pack hidden labels
            self.dict_columns_label["Fecha"].   grid(row = 0,  column=0, sticky = "wne")
            self.dict_columns_label["Salida"].  grid(row = 0,  column=4, sticky = "wne")
            self.dict_columns_label["Ingreso"]. grid(row = 0,  column=5, sticky = "wne")

            # Pack hidden entryboxes 
            self.dict_columns_entry["Fecha"].   grid(row = 1,  column=0, padx = 10)
            self.dict_columns_entry["Salida"].  grid(row = 1,  column=4, padx = 10)
            self.dict_columns_entry["Ingreso"]. grid(row = 1,  column=5, padx = 10)

            self.treeview_eu.forget()
            self.datostree.pack()

            self.dict_columns_entry["Fecha"].focus_set()


        else:
            self.state_dict["Entradas Usuales"] = True

            color = "#CFAA41"

            # Hide labels
            self.dict_columns_label["Fecha"].   grid_forget()
            self.dict_columns_label["Salida"].  grid_forget()
            self.dict_columns_label["Ingreso"]. grid_forget()

            # Hide entryboxes
            self.dict_columns_entry["Fecha"].   grid_forget()
            self.dict_columns_entry["Salida"].  grid_forget()
            self.dict_columns_entry["Ingreso"]. grid_forget()

            self.datostree.forget()
            self.treeview_eu.pack()

            self.dict_columns_entry["Detalle"].focus_set()

        self.change_color("Entradas Usuales", color, "default")


# === Child class from Entryboxes_and_tail ===
# This class contains specific methods for investment instruments data entry 
class inversiones_Entryboxes_and_tail(Entryboxes_and_tail):
    def __init__(self, root, own_dataframe, own_csv, n_columns, color_frame_bg,color_frame_bg_2, font_color, columns_showing):
        super().__init__(root, own_dataframe, own_csv, n_columns, color_frame_bg,color_frame_bg_2, font_color, columns_showing)
        self.str_var_list = ["Fecha de Inicio", "Fecha de cierre", "Detalle","Tipo"]
        self.num_var_list = ["Días", "Monto" ,"Periodicidad Cupones","Intereses Banco","Impuesto Banco","Interes Final","Cupón mensual","Cupón residual"]
        self.num_percentage_var_list = ["Tasa anual", "Tasa impuesto", "Tasa real (con impuestos)"]

# === Methods ===

# === Edited methods ===

    # Add coupons calculations
    def save_dict(self):
        entry = {}

        for i in self.str_var_list:
            entry[i] = self.dict_columns_entry[i].get()

        for i in self.num_var_list:
            entry[i] = float(self.dict_columns_entry[i].get() or 0)

        for i in self.num_percentage_var_list:
            entry[i] = float(self.dict_columns_entry[i].get())/100

        entry = self.calc_cupons(entry)

        return entry

# === Funciones nuevas ===

    # Funcion para calcular cupones
    def calc_cupons(self, entry_dict):

        if entry_dict["Periodicidad Cupones"] > 0 and entry_dict["Días"] >= 30:

            entry_dict["Cupón mensual"] = entry_dict["Interes Final"]/entry_dict["Días"] * 30 * entry_dict["Periodicidad Cupones"]
            entry_dict["Cupón residual"] = entry_dict["Interes Final"] - entry_dict["Cupón mensual"] * int(entry_dict["Días"]/(30 * entry_dict["Periodicidad Cupones"]))
        
        else:

            entry_dict["Cupón mensual"] = 0
            entry_dict["Cupón residual"] = 0

        return entry_dict
