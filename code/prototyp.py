# PZSP2 - Prototyp prototypu
import tkinter as tk
from tkinter.ttk import *
from tkinter.messagebox import showinfo

root = tk.Tk() # tworzymy okno
root.geometry('800x600+300+200') # rozmiar (800x600) i poczatek (300,200) okna
root.attributes('-topmost', 1) # wyswietl nad innymi oknami

frame = None # ramka wyswietlana w oknie

# tworzenie ramki
def new_frame(title):
    root.title(title) # zmien tytul okna
    global frame
    # usun poprzednia ramke
    if frame is not None:
        frame.destroy()
    frame = Frame(root) # utworz nowa ramke
    frame.pack(expand = 'true') # rozciagnij ramke na cale okno

# Ekran 1
def frame_1():
    new_frame('Ekran 1')
    
	# Dodajemy przyciski
	# 'command' to akcja po nacisnieciu
    button_1 = Button(frame, text = 'Pokaz komunikat', command = lambda:
        showinfo(title = 'Informacja', message = 'Komunikat informacyjny'))
    button_2 = Button(frame, command = frame_2, text = 'Przejdz do ekranu 2')
    button_3 = Button(frame, command = root.destroy, text = 'Zakoncz')

    # Ukladamy przyciski na siatce
    # zobacz: https://www.pythontutorial.net/tkinter/tkinter-grid/
    button_1.grid(row = 0, column = 0, padx = 5, pady = 5)
    # 'padx' to dodatkowy odstep przed i po przyciku
    # 'pady' to dodatkowy odstep nad i pod przyciskiem,
    button_2.grid(row = 0, column = 1, padx = 5, pady = 5)
    button_3.grid(row = 1, column = 0, columnspan = 2, pady = 5)
    # 'columnspan' rozciaga komorke na kilka kolumn

# Ekran 2
# PZSP2 - Prototyp prototypu
import tkinter as tk
from tkinter.ttk import *
from tkinter.messagebox import showinfo
from pillow import ImageTk, Image

root = tk.Tk() # tworzymy okno
root.geometry('800x600+300+200') # rozmiar (800x600) i poczatek (300,200) okna
root.attributes('-topmost', 1) # wyswietl nad innymi oknami

frame = None # ramka wyswietlana w oknie

# tworzenie ramki
def new_frame(title):
    root.title(title) # zmien tytul okna
    global frame
    # usun poprzednia ramke
    if frame is not None:
        frame.destroy()
    frame = Frame(root) # utworz nowa ramke
    frame.pack(expand = 'true') # rozciagnij ramke na cale okno

# Ekran 1
def frame_1():
    new_frame('Ekran 1')
    
	# Dodajemy przyciski
	# 'command' to akcja po nacisnieciu
    button_1 = Button(frame, text = 'Pokaz komunikat', command = lambda:
        showinfo(title = 'Informacja', message = 'Komunikat informacyjny'))
    button_2 = Button(frame, command = frame_2, text = 'Przejdz do ekranu 2')
    button_3 = Button(frame, command = root.destroy, text = 'Zakoncz')

    # Ukladamy przyciski na siatce
    # zobacz: https://www.pythontutorial.net/tkinter/tkinter-grid/
    button_1.grid(row = 0, column = 0, padx = 5, pady = 5)
    # 'padx' to dodatkowy odstep przed i po przyciku
    # 'pady' to dodatkowy odstep nad i pod przyciskiem,
    button_2.grid(row = 0, column = 1, padx = 5, pady = 5)
    button_3.grid(row = 1, column = 0, columnspan = 2, pady = 5)
    # 'columnspan' rozciaga komorke na kilka kolumn

# Ekran 2
def frame_2():
    new_frame('Ekran 2')
    
    # Etykieta
    label_from = Label(frame, text = 'Skąd')
    
    # Pole tekstowe (30 znakow)
    entry_from = Entry(frame, width = 30)
    entry_from.insert(0, 'Skąd jedziesz')

    # Etykieta
    label_dest = Label(frame, text = 'Dokąd')
    
    # Pole tekstowe (30 znakow)
    entry_dest = Entry(frame, width = 30)
    entry_dest.insert(1, 'Dokąd jedziesz')
    
    # # Obszar tekstowy (4 linie, 50 znakow w linii)
    # text = tk.Text(frame, height = 4, width = 50)
    # text.insert('1.0', 'Wpisz wiecej tekstu...')

    # Pole wyboru
    checkbutton = Checkbutton(frame, text = 'Zaznacz to pole')
    checkbutton.invoke() # zaznaczony
    
    # Pola radio
    radiobutton_1 = Radiobutton(frame, text = 'Opcja 1', value = 0)
    radiobutton_2 = Radiobutton(frame, text = 'Opcja 2', value = 1)
    radiobutton_3 = Radiobutton(frame, text = 'Opcja 3', value = 2)
    radiobutton_1.invoke() # zaznaczony
    
    # Suwak
    slider = Scale(frame, orient = 'horizontal')
    
    # Pole combo
    combobox = Combobox(frame, values = ('C1', 'C2', 'C3'))
    combobox.current(0) # wybierz pierwsza pozycje
    
    # Pole listy
    listbox = tk.Listbox(frame,  height = 3)
    listbox.insert(0, 'L1')
    listbox.insert(1, 'L2')
    listbox.insert(2, 'L3')
    
    # Spinbox
    spinbox = tk.Spinbox(frame, from_ = 0, to = 10)
    
    # Pasek postepu
    progressbar = Progressbar(frame, orient = 'horizontal', length = 100)
    progressbar.step(50) # ustaw na 50%

    # Ukladamy na siatce
    # zobacz: https://www.pythontutorial.net/tkinter/tkinter-grid/
    

    interactive_map = ImageTk.PhotoImage(Image.open("map.jpg"))
    map_label = Label(frame, image=interactive_map)

    def useless():
        pass

    enter_button = Button(frame, text = 'Enter', command = useless)


    # text.grid(row = 1, column = 0, columnspan = 3, padx = 5, pady = 5)

    # checkbutton.grid(row = 2, column = 0, rowspan = 3)

    # radiobutton_1.grid(row = 2, column = 1)
    # radiobutton_2.grid(row = 3, column = 1)
    # radiobutton_3.grid(row = 4, column = 1)
    label_from.grid(row = 0, column = 0, padx = 5, pady = 5)
    entry_from.grid(row = 0, column = 1, padx = 5, pady = 5)
    label_dest.grid(row = 1, column = 0, padx = 5, pady = 5)
    entry_dest.grid(row = 1, column = 1, padx = 5, pady = 5)
    map_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    enter_button.grid(row = 3, column = 0, padx = 5, pady = 5)


    # slider.grid(row = 5, column = 0, padx = 5, pady = 5)
    # combobox.grid(row = 5, column = 1, padx = 5, pady = 5)
    # listbox.grid(row = 5, column = 2, padx = 5, pady = 5)
    
    # spinbox.grid(row = 6, column = 0, pady = 5)
    # progressbar.grid(row = 6, column = 2, pady = 5)
    
frame_1() # ekran startowy

root.mainloop()