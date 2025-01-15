import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
from tkinter import filedialog

import pickle
from functools import partial

class odabirdodataka:
    def __init__(self,root,checklista,stvoricanvas,izadi):
        
        self.frame2 = ttk.Frame(root)
        self.frame2.pack()
        
        self.MenuBttn = ttk.Menubutton(self.frame2, text = "Dodaci")
        self.dodajzad = ttk.Button(self.frame2, text="Izađi (Esc)", command=izadi)
        self.dodajzad.pack(side=tk.RIGHT)
        
        self.Var1 = tk.IntVar()
        self.Var2 = tk.IntVar()
        
        self.Menu1 = tk.Menu(self.MenuBttn, tearoff = 0)
        
        self.Menu1.add_checkbutton(label = "Check lista", variable = self.Var1, command=checklista)
        self.Menu1.add_checkbutton(label = "Canvas", variable = self.Var2, command=stvoricanvas)
        
        self.MenuBttn["menu"] = self.Menu1

        self.MenuBttn.pack(side=tk.LEFT)

    def __del__(self):
        print("Destruktor se pozvao dodatci")

#################################################################################################################

class unos_zadatka:
    def __init__(self,root,ime,menubar):

        root.bind("<Escape>",self.izadi)
        self.dodaci=odabirdodataka(root,self.checklista,self.stvoricanvas,self.izadi)

        self.menubar=menubar
        self.imezadatka=ime
        self.sadrzaj=""

        self.zadatak=tk.Text(root,height=10,font=('Arial',16))
        self.zadatak.pack(padx=10,pady=10)
        self.zadatak.bind("<Control-Return>",self.izadi)

        if not (self.sadrzaj.strip()):
            self.zadatak.insert("1.0",self.sadrzaj)

        self.listaprovjeraVar=[]
        self.listaprovjeraStr=[]
        self.listabotuna=[]

        self.checklistaon=0

        self.skupina=[]
        self.opcije=[]

        


    def checklista(self):
        if self.dodaci.Var1.get()==1:
            
            self.frame3 = ttk.Frame(root)
            self.frame3.pack()
            
            self.brbotuna=0

            if(self.dodaci.Var2.get()==1):
                print("yea")
                self.frame3.pack_forget()

                self.canvas.pack_forget()
                self.frame4.pack_forget()
                self.frame5.pack_forget()
                    
                self.frame3.pack()

                self.canvas.pack(pady=10)
                self.frame4.pack()
                self.frame5.pack()

            if self.checklistaon == 0:
                self.dodatibr = tk.simpledialog.askinteger(title="Unos", prompt="Unesite broj 'check' marki:")
                if self.dodatibr==None or self.dodatibr <= 0:
                    if self.dodatibr != None:
                        messagebox.showinfo(title='Loš odabir', message="Loš broj ste unijeli.")
                    self.dodaci.Var1.set(0)
                    return

                self.brbotuna=self.dodatibr
                for i in range(self.dodatibr):

                    self.dodati = tk.simpledialog.askstring(title="Unos", prompt=f"Unesite tekst za {i+1}. 'kutiju':")
                    self.listaprovjeraStr.append(self.dodati)

                    self.listaprovjeraVar.append(tk.IntVar())

                    checkbutton = ttk.Checkbutton(self.frame3, text=self.listaprovjeraStr[i], variable=self.listaprovjeraVar[i], command=partial(self.strikethrough,i))
                    checkbutton.configure(style="O.TCheckbutton")
                    self.listabotuna.append(checkbutton)          
                    self.listabotuna[i].pack()

                

        else:
            if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite poništiti check listu?"):
                self.frame3.destroy()

                self.listaprovjeraVar.clear()
                self.listaprovjeraStr.clear()
                self.listabotuna.clear()
                
                self.brbotuna=0
            else:
                self.dodaci.Var1.set(1)
                return
    
    def strikethrough(self,i):

        print(self.listaprovjeraVar[i].get())
        if self.listaprovjeraVar[i].get():
            self.listabotuna[i].config(style="X.TCheckbutton")  
        else:
            self.listabotuna[i].config(style="O.TCheckbutton")

    def stvoricanvas(self):
        if self.dodaci.Var2.get()==1:
            
            self.canvas = tk.Canvas(root, width=1000, height=500, bg='white')
            self.canvas.pack(pady = 10)

            self.line_id = None
            self.line_points = []
            self.line_options = {
                "fill":"black",
                "width": 2
            }
            
            self.frame4 = ttk.Frame(root)
            self.frame4.pack()

            self.frame5=ttk.Frame(root)
            self.frame5.pack()

            self.botunOcistiCanvas = ttk.Button(self.frame5, text="Očisti canvas", command=self.ocisti)
            self.botunOcistiCanvas.pack(side=tk.BOTTOM)

            self.botunMijenjajSliku = ttk.Button(self.frame5, text="Učitaj/Promijeni sliku", command=self.slike)
            self.botunMijenjajSliku.pack(side=tk.BOTTOM)
            
            self.blista=["Crna","Crvena","Zelena","Plava"]
            self.boja = ttk.Combobox(self.frame5, values = self.blista, state="readonly")
            self.boja.set("Odaberi boju")
            self.boja.pack(side=tk.RIGHT,padx=25)
            self.boja.bind("<<ComboboxSelected>>",self.odabirboje)

            self.skala=ttk.Scale(self.frame5, from_=1, to=5)
            self.skala.pack(side=tk.RIGHT)
            self.skala.bind("<ButtonRelease-1>",self.odabirdebljine)

            self.skalaime=ttk.Label(self.frame5,text="Debljina crte:")
            self.skalaime.pack(side=tk.RIGHT)

            self.botunCrtaj=ttk.Button(self.frame4,text="Crtaj",command=partial(self.odaberi,1))
            self.botunCrtaj.pack(side=tk.RIGHT)

            self.botunSlika=ttk.Button(self.frame4,text="Pomicanje slike", command=partial(self.odaberi,2))
            self.botunSlika.pack(side=tk.LEFT)
            
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
                self.frame4.destroy()
                self.frame5.destroy()
                self.skupina.clear()
                self.opcije.clear()
            else:
                self.dodaci.Var2.set(1)
                return

    def ocisti(self):
        if messagebox.askyesno("Potvrda", "Jeste li sigurni da želite očistiti canvas?"):
            self.canvas.delete("all")
            self.slika_id=self.canvas.create_image(100,100,anchor="nw",image=None)
            self.zoom_level=2
        else:
            return

    def odabirboje(self,event):
        if self.boja.get()=="Crna":
            self.line_options["fill"]="black"
        elif self.boja.get()=="Crvena":
            self.line_options["fill"]="red"
        elif self.boja.get()=="Zelena":
            self.line_options["fill"]="green"
        elif self.boja.get()=="Plava":
            self.line_options["fill"]="blue"

    def odabirdebljine(self,event):
        self.line_options["width"]=self.skala.get()

    def odaberi(self,br):
        if br==1:
            self.canvas.bind('<Button-1>', self.zapocni)
            self.canvas.bind("<B1-Motion>",self.crtaj)
            self.canvas.bind('<ButtonRelease-1>', self.stani)
        else:
            self.canvas.bind("<B1-Motion>",self.move)

    def imagezoom(self,event):

        if event.delta > 0 and self.zoom_level<=3:

            if self.zoom_level == -2:
                self.zoom_level=2
            else:
                self.zoom_level += 1

            zoomed_image = self.slika.zoom(2, 2)
            self.canvas.itemconfig(self.slika_id, image=zoomed_image)

            self.slika = zoomed_image
            
        elif event.delta < 0 and self.zoom_level>=-3:

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
        
    def crtaj(self,event):
        global line_id
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.canvas.delete(line_id)
        line_id = self.canvas.create_line(self.line_points, fill=self.line_options["fill"], width=self.line_options["width"])

    def stani(self,event=None):
        global line_id
        self.skupina.append(self.line_points)
        dodaj={
            "fill":self.line_options["fill"],
            "width":self.line_options["width"]
        }
        self.opcije.append(dodaj)
        self.line_points=[]
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
        root.bind("<Escape>",zatvori)

        for widget in root.winfo_children():
            if widget==self.menubar:
                root.config(menu=menubar)
                continue
            widget.pack(pady=10)

        for widget in listaunosa:

            widget.zadatak.pack_forget()
            widget.dodaci.frame2.pack_forget()

            if widget.dodaci.Var1.get()==1:
                widget.frame3.pack_forget()

            if widget.dodaci.Var2.get()==1:
                widget.canvas.pack_forget()
                widget.frame4.pack_forget()
                widget.frame5.pack_forget()
    
    def __del__(self):
        print("Destruktor se pozvao unos_zad")
        
#########################################################################################################


def add_task(event = None):
    task = task_entry.get().strip()
    if task:
        tasks_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Greška u unosu", "Zadatak ne može biti prazan.")


def remove_task(event=None):
    try:
        selected_task_index = tasks_listbox.curselection()[0]
        if 0 <= selected_task_index and selected_task_index < len(listaunosa) and not listaunosa[selected_task_index].sadrzaj.strip():

            listaunosa[selected_task_index].zadatak.destroy()
            listaunosa[selected_task_index].dodaci.frame2.destroy()
            if listaunosa[selected_task_index].dodaci.Var1.get()==1:
                listaunosa[selected_task_index].frame3.destroy()
            if listaunosa[selected_task_index].dodaci.Var2.get()==1:
                listaunosa[selected_task_index].canvas.destroy()
                listaunosa[selected_task_index].frame4.destroy()
                listaunosa[selected_task_index].frame5.destroy()
            listaunosa.remove(listaunosa[selected_task_index])

        tasks_listbox.delete(selected_task_index)

    except IndexError:
        messagebox.showwarning("Greška u odabiru", "Nije odabran ni jedan zadatak.")

def clear_tasks(event=None):
    if messagebox.askyesno("Potvrda", "Obrisati sve zadatke?"):
        for i in listaunosa:
            i.zadatak.destroy()
            i.dodaci.frame2.destroy()
            if i.dodaci.Var1.get()==1:
                i.frame3.destroy()
            if i.dodaci.Var2.get()==1:
                i.canvas.destroy()
                i.frame4.destroy()
                i.frame5.destroy()
        listaunosa.clear()
        tasks_listbox.delete(0, tk.END)

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
            i.zadatak.pack(padx=10,pady=10)
            if i.dodaci.Var1.get()==1:
                i.frame3.pack()
                for j in i.listabotuna:
                    j.pack()
            if i.dodaci.Var2.get()==1:
                i.canvas.pack(pady = 10)
                i.frame4.pack()
                i.frame5.pack()
            root.bind("<Escape>",i.izadi)
            return
    messagebox.showinfo("Novi unos", f"Novi unos u: {selected_task}")
    listaunosa.insert(selected_task_index,unos_zadatka(root,selected_task,menubar))

def popupdodaj():
    dodati = tk.simpledialog.askstring(title="Unos", prompt="Dodajte zadatak:")
    if dodati:
        tasks_listbox.insert(tk.END, dodati)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Greška u unosu", "Zadatak ne može biti prazan.")

def spremidatoteku(event=None):
    if not trenutnifile:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Binarna datoteka", "*.bin"), ("Sve datoteke", "*.*")],
            title="Spremi datoteku"
        )
    else:
        file_path=trenutnifile[0]

    if file_path:
        if (file_path==trenutnifile[0]):
            messagebox.showinfo("Uspješno spremanje", "Datoteka je spremljena.")
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

                    "listatocaka": [],
                    "opcije": []
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
                    for j in i.skupina:
                        prenesi["listatocaka"].append(j)
                    prenesi["opcije"]=i.opcije

                pickle.dump(prenesi,file)

def otvoridatoteku(event=None):
    file_path = filedialog.askopenfilename(
        title="Otvori datoteku",
        filetypes=[("Binarna datoteka", "*.bin"), ("Sve datoteke", "*.*")],
    )
    if file_path:
        trenutnifile.clear()
        trenutnifile.append(file_path)
        clear_tasks()
        with open(file_path, "rb") as file:
            while True:
                try:
                    preneseno = pickle.load(file)
                    tasks_listbox.insert(tk.END,preneseno["listboxime"])
                    novi=unos_zadatka(root,preneseno["listboxime"],menubar)
                    novi.zadatak.insert(tk.END, preneseno["unos"])

                    if preneseno["Var1"] == 1:
                        novi.dodaci.Var1.set(1)
                        novi.checklistaon=1
                        novi.checklista()
                        novi.brbotuna=preneseno["brbotuna"]
                        for i in range(novi.brbotuna):
                            novi.listaprovjeraVar.append(tk.IntVar(value=preneseno["listaKrizanja"][i]))
                            novi.listaprovjeraStr.append(preneseno["listaStr"][i])
                            checkbutton = ttk.Checkbutton(novi.frame3, text=novi.listaprovjeraStr[i], variable=novi.listaprovjeraVar[i], command=partial(novi.strikethrough,i))
                            if novi.listaprovjeraVar[i].get()==1:
                                checkbutton.configure(style="X.TCheckbutton")
                            else:
                                checkbutton.configure(style="O.TCheckbutton")
                            novi.listabotuna.append(checkbutton)
                        novi.checklistaon=0
                    
                    if preneseno["Var2"] == 1:
                        novi.dodaci.Var2.set(1)
                        novi.stvoricanvas()
                        novi.filename=preneseno["slikafile"]                       
                        if preneseno["listatocaka"]:   
                            novi.skupina=preneseno["listatocaka"]
                            novi.opcije=preneseno["opcije"]
                            for temp,i in enumerate(preneseno["listatocaka"]):
                                if(len(i)==2):
                                    continue
                                novi.line_id = novi.canvas.create_line(i,fill=preneseno["opcije"][temp]["fill"],width=preneseno["opcije"][temp]["width"])
                                novi.line_id = None
                                        
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

def zatvori(event=None):
    temp=messagebox.askyesnocancel(title="Zatvaranje",message="Želite li spremiti prije nego što izađete iz programa?")
    if temp==1:
        spremidatoteku()
        root.destroy()
    elif temp==0:
        root.destroy()
    else:
        return

###################################################################################################

root = tk.Tk()
root.title("Voditelj popisa zadataka")
root.geometry("1920x1080")
root.bind("<Escape>",zatvori)
root.bind("<Control-s>",spremidatoteku)
root.bind("<Control-o>",otvoridatoteku)
root.protocol("WM_DELETE_WINDOW",zatvori)

style=ttk.Style()
fontYeah = font.Font(family="Arial", size=16, overstrike=True)
fontNo = font.Font(family="Arial", size=16, overstrike=False)
style.configure("X.TCheckbutton", font=fontYeah)
style.configure("O.TCheckbutton", font=fontNo)

labela = ttk.Label(root, text="Unesite zadatak:", font=("Arial", 16))
labela.pack(pady=10)

trenutnifile=[]

task_entry = ttk.Entry(root, width=40)
task_entry.pack(pady=5)
task_entry.bind("<Return>", add_task)
task_entry.tkraise()

add_button = ttk.Button(root, text="Dodaj zadatak (Enter)", command=add_task)
add_button.pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=10, padx=10)

tasks_listbox = tk.Listbox(frame, height=30, width=100)
tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
tasks_listbox.bind("<Double-Button-1>", on_double_click)
tasks_listbox.bind("<BackSpace>", remove_task)
tasks_listbox.bind("<Control-BackSpace>", clear_tasks)

scroll_bar = ttk.Scrollbar(frame)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
tasks_listbox.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=tasks_listbox.yview)

remove_button = ttk.Button(root, text="Ukloni zadatak (Backspace)", command=remove_task)
remove_button.pack(pady=10)

clear_button = ttk.Button(root, text="Ukloni sve zadatke (Ctrl + Backspace)", command=clear_tasks)
clear_button.pack(pady=10)

listaunosa=[]

menubar = tk.Menu(root)

taskmenu = tk.Menu(menubar, tearoff=0)
taskmenu.add_command(label="Izbriši sve", command=clear_tasks)
taskmenu.add_command(label="Dodaj novi zadatak", command=popupdodaj)

filemenu=tk.Menu(menubar,tearoff=0)
filemenu.add_command(label="Spremi (Ctrl+S)", command = spremidatoteku)
filemenu.add_command(label="Otvori (Ctrl+O)", command = otvoridatoteku)

menubar.add_cascade(label="Zadatci", menu=taskmenu)
menubar.add_cascade(label="Datoteka", menu=filemenu)
root.config(menu=menubar)

root.mainloop()
