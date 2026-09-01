# Personal-Finance-Manager
[Work In Progress] This project is currently under development. Some features may be incomplete and subject to change. The project is built in Python using pandas, matplotlib, tkinter and ttkbootstrap to generate a data entry and interactive dashboard interface.

This project was originally created in Excel to help me track my expenses and income in a fast and easy way. As the project evolved with bigger and more complex tools, I came across with some of Excel limitations which drive me to find a more flexible environment. I started to migrate the project to Python, altough many features are still missing from the original project and there are new features that haven't still been added. The main philosophy of the app is to have a fast way to register one's transactions, without having unnecessary clicks or pop up windows; and be able to understand them easily by using categories, filters and visualizations.

The code is divided in three documents. A main document which wraps the other two and generates the interface. Another document contains personalized widgets in the form of classes. The third document contais some helper functions.

## main.py

This document generates the interface by using instances of the classes cointained in fp_widgets.py. The app first starts with a Log In window in which you can create a new user or enter as a guest. Once you log in the main app appears presenting four charts, divided in two frames. Each of them can have their data filtered with the buttons at the right. 

The app has four different states, the base state in which you can enter data by filling the Entry boxes, a Usual entries state, an Eraser state and an Edition state. They will be explained inmediately.

### States
Base state is the normal state of the app and the one you will find every time you open the app. In this state you can enter data by filling the Entry boxes, once you fill them you can save the whole entry by either pressing Shift+Enter when your cursor is in any Entry box or by pressing tab in any of the last two Entry boxes. This will update the entry visualization chart as well as the charts above.

Usual entries state allows you to save that type of data. You may be wondering what are Usual entries. These are entries that you would commonly fill on a weekly or monthly basis, in general you decide what would be "Usual" for you. Examples would be your favorite restaurant, monthly house bills, subscriptions, transportations expenses, a place you like to visit, any specific or general category that appears commonly like Food, Bills, Car, etc. Considering the amount of times you will be filling these, the vlookup-type of function saves time on the long run by just having to enter the first word or even a key word.

Erase state enables the option to select and erase an existing row in the database. Behaviour of this state will be explained below.

Edit sate enables the option to select and edit an existing row in the database. Behaviour of this state will be explained below.

### Data entry segment
At the bottom you will find this widget. First, you will see the Entry boxes in which you can fill your data according to the title of the box. "Fecha" (Date) will always try to get the date of the last entry, if not available, it will automatically fill with "today" date, it can be changd manually by filling the box. Other boxes have Quality-of-life functions to make data entry easier. "Detalle" (Detail) and "Categoría específica" (Specific category) have a built-in vlookup-type of function that will fill the next bigger category once a Usual entry is entered. Furthermore, alongside with "Categoría general" (General category) the previous spaces will automatically correct themselves in terms of lower and upper case as well as accents in Spanish when you write the complet word and it is registered as a Usual entry. For example, if you have the General category "Food" registered as a Usual entry and you write "fOOd" in the General category blank, it will change to "Food".

There is a Usual entries ("Entradas Usuales") Button desgined to change the interface and allow to save Usual entries. When you fill the Entry boxes that identify that Usual entry you can save them by pressing 
Shift + Enter when the cursor is in any Entry box. Once you saved them, the previous described functions will start working in the Base state. When you want to go back to the normal interface, click again that button which should have changed to indicate a different app state. 

The "Borrar" and "Modificar" buttons will enable the option to click on the observations and select an existing entry to then erase or edit it respectively, the frame containing the Entry boxes will change color to indicate a different app state. When you want to erase a row, you can click it and a pop up window will appear to confirm deletion. When editing, you can click on a row and the data will appear on the Entry boxes where you can edit it and save it by either pressing Shift+Enter on any Entry box or by pressing tab on the last two Entry boxes. When you want to go back to normal data entry state, just click the buttons again, a change of color of the frame and buttons will indicate you are in the Base state again.

## fp_widgets.py

This document contains all the personalized widgets which are created using dependencies of the libraries mentioned at the beginning.

### LogIn_Gui:
generates a log in window with methods to validate users, create new users or enter as a guest. When creating a new user the files where databases are stored are created. These files are csv files. When a user logs in, the program calls for the names of this databases which later are loaded as pandas dataframes to manage them.

### charts:
is the widget that contains the charts and the filter buttons. Matplotlib is used to generate charts. The widgets consists of two charts, one bar chart that groups the entries by General category, the other chart is a histogram that shows the distribution of the total sum of entries by month, this lets you analyze the distribution of monthly expenses or income. The buttons in this widget can filter the data to select data from only selected categories, months or years. The filters also have the option to make multiple selections, which means you can have multiple categories, months or years active, or an individual selection, which means just one category, month or year. When you select an individual category, the chart will show the Specific categories related to that General Category.

### Entryboxes_and_tail:
contains the Entry boxes frame, state buttons and a treeview taht shows the last five entries in your database. This is a parent class and serves as a template for other classes used in the project. Quality-of-life methods and Usual entries state is not available in this class.

### iyg_Entryboxes_and_tail:
is a child class from Entryboxes_and_tail. It adds Quality-of-life methods and Usual entries state. This additions serve as a personalized upgrade specific to that part of the project.

### inversiones_Entryboxes_and_tail:
is a child class from Entryboxes_and_tail. This widget will be used in next part of the project that helps to keep track of financial instruments. Adds coupon calculations.

## logic.py

This document has helper functions used in some methods of the classes described above.

### qt:
is a function to eliminate accents in texts.

### norm:
normalizes text. It is useful when comparing two texts that are the same but the case does not match or there are accents in one of them.

### norm_df:
normalizes text inside a pandas' dataframe. It is useful when comparing two texts that are the same but the case does not match or there are accents in one of them.

### buscar_v:
is a vlookup created specifically to work with tkinter variables as the looked up text and a pandas datafame as the table to look up.

## Technologies

### pandas:
I use pandas to manage the database. I generated dynamic pivot tables to create charts. Data cleaning and transformation are performed using this library to guarantee cohesion between old and new entries.

### matplotlib:
I use this library to create charts, with other methods and functions I was able to generate dynamic charts to make visual analysis and exploration of expenses and income.

### tkinter:
Is the main source for the GUI and interactive tools in the app.

### ttkbootstrap:
I use it to give the app a more modern and clean look.

## Challenges and next steps
The main challenge for this project has been keeping a fast experience when so many fucntions start to interconnect. An organized approach has been crucial to maintain order between methods and classes.
Other challenges have involved the connection of different libraries to develop sharp answers to the questions I wanted to answer. The charts class was specially complex to construct because of the connections that had to be done between the tkinter buttons, a pandas filtered dataframe and the matplotlit charts. The key to accomplishing a final product was to use the pdataframe as a connector between the firs and the last. Multiindex localization was a key component of the correct behaviour of the widget.

Some next steps will include an investment tracking system and a coupon calendar. Some charts are subject to change in order to offer a more clear view of the data not only by category, but by time variables too.

Some other interface changes could be done to accomplish a cleaner visualization.

One of the main concerns is the privacy and security of the data. In the future I am planning to use hashing to encrypt data and add a layer of security.


## Setup

To use the app you will need logic.py, fp_widgets.py and main.py, you should run the latter to open the app. Neccesary libraries are tkinter, ttkbootstrap, pandas and matplotlib. Additionally, if you want to try an existing database, you can use all four csv files: users.csv, fp_gue_db_iyg_193119_31_08_2026, fp_gue_db_eu_193119_31_08_2026, fp_gue_db_inv_193119_31_08_2026 which are a trial dataset for the guest user that you can access by clicking on the "Ingresar como invitado" (Enter as guest) button in the Log In window. Make sure all files are on the same folder.

## Gallery

## === Log In ===
<img width="495" height="325" alt="image" src="https://github.com/user-attachments/assets/e126cf27-47c4-4b39-b490-0a750eabf11c" />

### New User
<img width="490" height="326" alt="image" src="https://github.com/user-attachments/assets/a7a2dc27-4741-4910-912c-05387de18ab2" />

## === Main ===
<img width="1213" height="626" alt="image" src="https://github.com/user-attachments/assets/349efed8-0b61-4db5-8e3b-ea20029cc7da" />

## === Usual entries ===
<img width="1146" height="577" alt="image" src="https://github.com/user-attachments/assets/75c550cb-384f-4539-9149-ff138f5bcc76" />

## === Erase state ===
<img width="1206" height="626" alt="image" src="https://github.com/user-attachments/assets/ccb506df-55a1-48ff-ae89-0f74d6b850a0" />

### After clicking the button
<img width="1210" height="630" alt="image" src="https://github.com/user-attachments/assets/71af9859-4e3c-4e43-9fda-fca072ed8c3c" />

### After clicking a row
<img width="1213" height="632" alt="image" src="https://github.com/user-attachments/assets/699242af-113b-4d81-8de1-cd6506bc5e9b" />

## === Edit state ===
<img width="1207" height="629" alt="image" src="https://github.com/user-attachments/assets/e7acc79e-e3aa-4bf3-b434-ac0776f332e4" />

### After clicking the button
<img width="1207" height="627" alt="image" src="https://github.com/user-attachments/assets/35d056a6-dbe4-4ba7-9d20-89c0418d26f7" />

### After clicking a row
<img width="1211" height="631" alt="image" src="https://github.com/user-attachments/assets/62d85d3a-fb76-49f2-b5d9-dade8d1e3c8d" />









