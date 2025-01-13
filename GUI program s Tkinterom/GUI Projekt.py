import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
from tkinter import filedialog
import pickle

class odabirdodataka:
    def __init__(self,root,checklista,stvoricanvas):
        self.frame2 = tk.Frame(root)
        self.frame2.pack()
        
        self.MenuBttn = tk.Menubutton(self.frame2, text = "Dodaci", relief = tk.RAISED)
        
        self.Var1 = tk.IntVar()
        self.Var2 = tk.IntVar()
        
        self.Menu1 = tk.Menu(self.MenuBttn, tearoff = 0)
        
        self.Menu1.add_checkbutton(label = "Check lista", variable = self.Var1, command=checklista)
        self.Menu1.add_checkbutton(label = "Canvas", variable = self.Var2, command=stvoricanvas)
        
        self.MenuBttn["menu"] = self.Menu1

        self.MenuBttn.pack()

    def __del__(self):
        print("Destruktor se pozvao dodatci")


class unos_zadatka:
    def __init__(self,root,ime,menubar):

        
        self.dodaci=odabirdodataka(root,self.checklista,self.stvoricanvas)

        self.menubar=menubar
        self.imezadatka=ime
        self.sadrzaj=""

        self.zadatak=tk.Text(root,height=10,font=('Arial',16))
        self.zadatak.pack(padx=10,pady=10)
        self.zadatak.bind("<Control-Return>",self.izadi)

        if not (self.sadrzaj.strip()):
            self.zadatak.insert("1.0",self.sadrzaj)

        self.dodajzad = tk.Button(root, text="Izađi (Ctrl+Enter)", command=self.izadi)
        self.dodajzad.pack(pady=10)

        self.listaprovjeraVar=[]
        self.listaprovjeraStr=[]
        self.listafontova=[]
        self.listabotuna=[]

        self.nacrtano=[]

        self.frame3 = tk.Frame(root)


    def checklista(self):
        if self.dodaci.Var1.get()==1:
            
            self.frame3.pack()

            self.brbotuna=0
            
            self.dodatibr = tk.simpledialog.askinteger(title="Unos", prompt="Unesite broj 'check' marki:")
            if self.dodatibr==None or self.dodatibr <= 0:
                if self.dodatibr != None:
                    messagebox.showinfo(title='Loš odabir', message="Loš broj ste unijeli.")
                self.dodaci.Var1.set(0)
                return

            for i in range(self.dodatibr):
                self.fontYeah = font.Font(family="Helvetica", size=14)
                self.listafontova.append(self.fontYeah)

                self.dodati = tk.simpledialog.askstring(title="Unos", prompt=f"Unesite tekst za {i+1}. 'kutiju':")
                self.listaprovjeraStr.append(self.dodati)

                self.listaprovjeraVar.append(tk.IntVar())

                checkbutton = tk.Checkbutton(self.frame3, font=self.listafontova[i],text=self.listaprovjeraStr[i], variable=self.listaprovjeraVar[i], command=lambda idx=i: self.strikethrough(idx))
                self.listabotuna.append(checkbutton)
                self.brbotuna+=1
                self.listabotuna[i].pack()       

        else:
            if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite poništiti check listu?"):
                for widget in self.frame3.winfo_children():
                    widget.destroy()
                self.frame3.destroy()
                self.brbotuna=0
            else:
                self.dodaci.Var1.set(1)
                return
    
    def strikethrough(self,i):
        print(i)
        if self.listaprovjeraVar[i].get():
            self.listafontova[i].configure(overstrike=1)  
        else:
            self.listafontova[i].configure(overstrike=0)

    def stvoricanvas(self):
        if self.dodaci.Var2.get()==1:
            
            self.canvas = tk.Canvas(root, width=1000, height=500, bg='white')
            self.canvas.pack(pady = 10)

            self.line_id = None
            self.line_points = []
            self.line_options = {}
            

            self.frame4 = tk.Frame(root)
            self.frame4.pack()

            self.botunMijenjajSliku = tk.Button(self.frame4, text="Ucitaj/Promijeni sliku", command=self.slike)
            self.botunMijenjajSliku.pack(side=tk.LEFT)

            self.botunCrtaj=tk.Button(self.frame4,text="Crtaj",command=self.odaberi)
            self.botunCrtaj.pack(side=tk.RIGHT)
            
            #Default slika
            self.filename = r"C:\Users\leoje\Desktop\Projekti\GUI program s Tkinterom\def.png" 

            self.slika = tk.PhotoImage(file=self.filename)
            self.zoom_level = 2
            self.slika_id=self.canvas.create_image(100,100,anchor="nw",image=self.slika)
            self.canvas.bind("<MouseWheel>",self.imagezoom)
            self.canvas.bind("<B1-Motion>",self.move)


        else:
            if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite poništiti canvas?"):
                self.canvas.destroy()
                self.botunMijenjajSliku.destroy()
                self.botunCrtaj.destroy()
                self.frame4.destroy()
            else:
                self.dodaci.Var2.set(1)
                return

    def odaberi(self):
        self.canvas.bind('<Button-1>', self.zapocni)
        self.canvas.bind("<B1-Motion>",self.crtaj)
        self.canvas.bind('<ButtonRelease-1>', self.stani)

    def imagezoom(self,event):

        if event.delta > 0 and self.zoom_level<=3:  # Zoom in

            if self.zoom_level == -2:
                self.zoom_level=2
            else:
                self.zoom_level += 1

            zoomed_image = self.slika.zoom(2, 2)
            self.canvas.itemconfig(self.slika_id, image=zoomed_image)

            self.slika = zoomed_image
            
        elif event.delta < 0 and self.zoom_level>=-3:  # Zoom out

            if self.zoom_level == 2 or self.zoom_level == 1:
                self.zoom_level=-2
            else:
                self.zoom_level -= 1
        
            zoomed_image = self.slika.subsample(2, 2)
            self.canvas.itemconfig(self.slika_id, image=zoomed_image)

            self.slika = zoomed_image

        else:
            return

        print(self.zoom_level)

        

    def zapocni(self,event):
        self.line_points.extend((event.x, event.y))
        self.nacrtano.extend((event.x, event.y))
        
    def crtaj(self,event):
        global line_id
        self.line_points.extend((event.x, event.y))
        self.nacrtano.extend((event.x, event.y))
        if self.line_id is not None:
            self.canvas.delete(line_id)
        line_id = self.canvas.create_line(self.line_points, **self.line_options)

    def stani(self,event=None):
        global line_id
        self.line_points.clear()
        line_id = None

    def move(self, event):
        self.canvas.coords(self.slika_id, event.x-150, event.y-150)

    def slike(self):
        self.canvas.bind("<B1-Motion>",self.move)
        self.filetypes = (('png datoteka', '*.png'),('jpg datoteka', '*.jpg'),('jpeg datoteka', '*.jpeg'))
        self.temp = filedialog.askopenfilename(title='Otvori datoteku',initialdir='/',filetypes=self.filetypes)
        if not self.temp:
            messagebox.showinfo(title='Odabrana datoteka', message="Niste odabrali datoteku.")
            return
        self.filename=self.temp
        messagebox.showinfo(title='Odabrana datoteka', message=self.filename)
        self.slika = tk.PhotoImage(file=self.filename)
        self.canvas.itemconfig(self.slika_id, image=self.slika)
    
    def izadi(self,event=None):
        self.sadrzaj=self.zadatak.get('1.0',tk.END)

        for widget in root.winfo_children():
            if widget==self.menubar:
                root.config(menu=menubar)
                continue
            widget.pack(pady=10)

        for widget in listaunosa:
            widget.zadatak.pack_forget()
            widget.dodajzad.pack_forget()

            widget.dodaci.MenuBttn.pack_forget()
            widget.dodaci.frame2.pack_forget()

            if widget.dodaci.Var1.get()==1:
                for j in widget.listabotuna:
                    j.pack_forget()
                widget.frame3.pack_forget()

            if widget.dodaci.Var2.get()==1:
                widget.canvas.pack_forget()
                widget.botunMijenjajSliku.pack_forget()
                widget.botunCrtaj.pack_forget()
                widget.frame4.pack_forget()
    
    def __del__(self):
        print("Destruktor se pozvao unos_zad")
        


# Function to add a task to the list
def add_task(event = None):
    task = task_entry.get().strip()
    if task:  # Add task only if it's non-empty
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)  # Clear the input field
    else:
        messagebox.showwarning("Greška u unosu", "Zadatak ne može biti prazan.")

# Function to remove the selected task
def remove_task(event=None):
    try:
        selected_task_index = tasks_listbox.curselection()[0] # Get selected task index
        if 0 <= selected_task_index and selected_task_index < len(listaunosa) and not listaunosa[selected_task_index].sadrzaj.strip():

            listaunosa[selected_task_index].zadatak.destroy()
            listaunosa[selected_task_index].dodajzad.destroy()
            listaunosa[selected_task_index].dodaci.frame2.destroy()
            listaunosa[selected_task_index].dodaci.MenuBttn.destroy()
            if listaunosa[selected_task_index].dodaci.Var1.get()==1:
                for j in listaunosa[selected_task_index].listabotuna:
                    j.destroy()
                listaunosa[selected_task_index].frame3.destroy()
            if listaunosa[selected_task_index].dodaci.Var2.get()==1:
                listaunosa[selected_task_index].canvas.destroy()
                listaunosa[selected_task_index].botunMijenjajSliku.destroy()
                listaunosa[selected_task_index].botunCrtaj.destroy()
                listaunosa[selected_task_index].frame4.destroy()
            listaunosa.remove(listaunosa[selected_task_index])

        tasks_listbox.delete(selected_task_index)  # Remove the task

    except IndexError:
        messagebox.showwarning("Greška u odabiru", "Nije odabran ni jedan zadatak.")

# Function to clear all tasks
def clear_tasks(event=None):
    if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite obrisati sve zadatke?"):
        for i in listaunosa:
            i.zadatak.destroy()
            i.dodajzad.destroy()
            i.dodaci.frame2.destroy()
            i.dodaci.MenuBttn.destroy()
            if i.dodaci.Var1.get()==1:
                for j in i.listabotuna:
                    j.destroy()
                i.frame3.destroy()
            if i.dodaci.Var2.get()==1:
                i.canvas.destroy()
                i.botunMijenjajSliku.destroy()
                i.botunCrtaj.destroy()
                i.frame4.destroy()
        listaunosa.clear()
        tasks_listbox.delete(0, tk.END)  # Remove all tasks

def on_double_click(event):
    selected_task_index = tasks_listbox.curselection()[0]
    selected_task = tasks_listbox.get(tasks_listbox.curselection()[0])

    for widget in root.winfo_children():
        if widget==menubar:
            root.config(menu="")
            continue
        widget.pack_forget()

    for i in listaunosa:
        if i.imezadatka==selected_task:
            i.dodaci.frame2.pack()
            i.dodaci.MenuBttn.pack()
            i.zadatak.pack(padx=10,pady=10)
            i.dodajzad.pack(pady=5)
            if i.dodaci.Var1.get()==1:
                i.frame3.pack()
                for j in i.listabotuna:
                    j.pack()
            if i.dodaci.Var2.get()==1:
                i.canvas.pack(pady = 10)
                i.frame4.pack()
                i.botunMijenjajSliku.pack(side=tk.LEFT)
                i.botunCrtaj.pack(side=tk.RIGHT)
            return
    messagebox.showinfo("Novi unos", f"Novi unos u: {selected_task}")
    listaunosa.insert(selected_task_index,unos_zadatka(root,selected_task,menubar))

def popupdodaj():
    dodati = tk.simpledialog.askstring(title="Unos", prompt="Dodajte zadatak:")
    if dodati:  # Add task only if it's non-empty
        tasks_listbox.insert(tk.END, dodati)
        task_entry.delete(0, tk.END)  # Clear the input field
    else:
        messagebox.showwarning("Greška u unosu", "Zadatak ne može biti prazan.")

def spremidatoteku():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".bin",  # Default file extension
        filetypes=[("Binarna datoteka", "*.bin"), ("Sve datoteke", "*.*")],  # Allowed file types
        title="Spremi datoteku"
    )
    if file_path:
        with open(file_path, "wb") as file:
            for i in listaunosa:
                prenesi={
                    "listboxime": i.imezadatka,

                    "unos": i.sadrzaj,

                    "Var1": 0,
                    "Var2": 0,

                    "listaStr": [],
                    "listaKrizanja": [],
                    "brbotuna": "",

                    "slikafile": "",
                    "slikazoomlvl": 1,
                    "slika_x": 0,
                    "slika_y": 0,

                    "listatocaka": []
                }

                if i.dodaci.Var1.get()==1:
                    prenesi["Var1"]=1
                    prenesi["brbotuna"]=i.brbotuna
                    for j in i.listaprovjeraStr:
                        prenesi["listaStr"].append(j)
                    for j in i.listaprovjeraVar:
                        prenesi["listaKrizanja"].append(j.get())

                if i.dodaci.Var2.get()==1:
                    prenesi["Var2"]=1
                    prenesi["slikafile"]=i.filename
                    prenesi["slikazoomlvl"]=i.zoom_level
                    koord=i.canvas.coords(i.slika_id)
                    prenesi["slika_x"]=koord[0]
                    prenesi["slika_y"]=koord[1]
                    for j in i.nacrtano:
                        prenesi["listatocaka"].append(j)

                pickle.dump(prenesi,file)

def otvoridatoteku():
    file_path = filedialog.askopenfilename(
        title="Otvori datoteku",
        filetypes=[("Binarna datoteka", "*.bin"), ("Sve datoteke", "*.*")],  # Filter file types
    )
    if file_path:
        #clear_tasks()
        with open(file_path, "rb") as file:
            while True:
                try:
                    preneseno = pickle.load(file)  # Load the next object from the file
                    tasks_listbox.insert(tk.END,preneseno["listboxime"])
                    novi=unos_zadatka(root,preneseno["listboxime"],menubar)
                    novi.zadatak.insert(tk.END, preneseno["unos"])

                    if preneseno["Var1"] == 1:
                        novi.dodaci.Var1.set(1)
                        novi.brbotuna=preneseno["brbotuna"]
                        for i in range(novi.brbotuna):
                            novi.listaprovjeraVar.append(tk.IntVar())
                            novi.listaprovjeraVar[i].set(preneseno["listaKrizanja"][i])
                            novi.listaprovjeraStr.append(preneseno["listaStr"][i])
                            fontYeah = font.Font(family="Helvetica", size=14)
                            fontYeah.configure(overstrike=preneseno["listaKrizanja"][i])
                            novi.listafontova.append(fontYeah)
                            checkbutton = tk.Checkbutton(novi.frame3, font=novi.listafontova[i],text=novi.listaprovjeraStr[i], variable=novi.listaprovjeraVar[i], command=lambda idx=i: novi.strikethrough(idx))
                            novi.listabotuna.append(checkbutton)
                    
                    if preneseno["Var2"] == 1:
                        novi.dodaci.Var2.set(1)
                        novi.stvoricanvas()
                        novi.filename=preneseno["slikafile"]                       
                        if preneseno["listatocaka"]:
                            novi.canvas.create_line(preneseno["listatocaka"])
                        novi.slika=tk.PhotoImage(file=novi.filename)
                        novi.zoom_level=preneseno["slikazoomlvl"]
                        zoom_slika=novi.slika
                        if novi.zoom_level<0:
                            zoom_slika=novi.slika.subsample(pow(2,abs(novi.zoom_level)-1),pow(2,abs(novi.zoom_level)-1))
                        elif novi.zoom_level>2:
                            zoom_slika=novi.slika.zoom(pow(2,novi.zoom_level-2),pow(2,novi.zoom_level-2))
                        novi.slika_id=novi.canvas.create_image(preneseno["slika_x"],preneseno["slika_y"],anchor="nw",image=zoom_slika)
                        novi.slika=zoom_slika

                    listaunosa.append(novi)
                    novi.izadi()

                except EOFError:
                    break

# Main application window
root = tk.Tk()
root.title("Voditelj popisa zadataka")
root.geometry("1920x1080")  # Set the window size

labela = tk.Label(root, text="Unesite zadatak:", font=("Arial", 16))
labela.pack(pady=10)

# Input field to add a task
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)
task_entry.bind("<Return>", add_task)
task_entry.tkraise()


# Add Task button
add_button = tk.Button(root, text="Dodaj zadatak (Enter)", command=add_task)
add_button.pack(pady=10)

# Tasks display area (Listbox)

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

tasks_listbox = tk.Listbox(frame, height=30, width=100)
tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
tasks_listbox.bind("<Double-Button-1>", on_double_click)
tasks_listbox.bind("<BackSpace>", remove_task)
tasks_listbox.bind("<Control-BackSpace>", clear_tasks)

scroll_bar = tk.Scrollbar(frame)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
tasks_listbox.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=tasks_listbox.yview)


# Remove Task button
remove_button = tk.Button(root, text="Ukloni zadatak (Backspace)", command=remove_task)
remove_button.pack(pady=10)

# Clear Tasks button
clear_button = tk.Button(root, text="Ukloni sve zadatke (Ctrl + Backspace)", command=clear_tasks)
clear_button.pack(pady=10)

listaunosa=[]

menubar = tk.Menu(root)

taskmenu = tk.Menu(menubar, tearoff=0)
taskmenu.add_command(label="Izbriši sve", command=clear_tasks)
taskmenu.add_command(label="Dodaj novi zadatak", command=popupdodaj)

filemenu=tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Spremi", command = spremidatoteku)
filemenu.add_command(label="Otvori", command = otvoridatoteku)

menubar.add_cascade(label="Zadatci", menu=taskmenu)
menubar.add_cascade(label="Datoteka", menu=filemenu)
root.config(menu=menubar)

# Run the application
root.mainloop()
