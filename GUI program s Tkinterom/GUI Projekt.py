import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import font
from tkinter import filedialog
from tkinter.colorchooser import askcolor

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

################################################################################################################################

class unos_zadatka:
    def __init__(self,root,ime,krit,menubar):

        root.bind("<Escape>",self.izadi)
        self.dodaci=odabirdodataka(root,self.checklista,self.stvoricanvas,self.izadi)

        self.menubar=menubar
        self.imezadatka=ime
        self.kriticnost=krit
        self.sadrzaj=""

        self.textframe=tk.Frame(root)
        self.textframe.pack()

        self.zadatak=tk.Text(self.textframe,height=10,font=('Arial',16),width=110)
        self.zadatak.pack(side=tk.LEFT)
        self.zadatak.bind("<Control-Return>",self.izadi)

        self.text_scrb = ttk.Scrollbar(self.textframe)
        self.text_scrb.pack(side=tk.RIGHT, fill=tk.Y)
        self.zadatak.config(yscrollcommand=self.text_scrb.set)
        self.text_scrb.config(command=self.zadatak.yview)

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

            self.zadatak.config(height=5)
            
            self.frame3 = ttk.Frame(root)
            self.frame3.pack()
            
            self.brbotuna=0

            if(self.dodaci.Var2.get()==1):
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
                    self.zadatak.config(height=10)
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
                
                self.zadatak.config(height=10)
                self.brbotuna=0
            else:
                self.dodaci.Var1.set(1)
                return
    
    def strikethrough(self,i):
        if self.listaprovjeraVar[i].get():
            self.listabotuna[i].config(style="X.TCheckbutton")  
        else:
            self.listabotuna[i].config(style="O.TCheckbutton")

    def stvoricanvas(self):
        if self.dodaci.Var2.get()==1:
            
            self.canvas = tk.Canvas(root, width=1500, height=300, bg='white')
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
            
            self.blista=["Crna","Crvena","Zelena","Plava","Odaberi sam"]
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
            self.botunSlika.configure(style="Select.TButton")
            
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
        elif self.boja.get()=="Odaberi sam":
            self.line_options["fill"]=askcolor(title="Odabir boje")[1]

    def odabirdebljine(self,event):
        self.line_options["width"]=self.skala.get()

    def odaberi(self,br):
        if br==1:
            self.botunSlika.configure(style="")
            self.botunCrtaj.configure(style="Select.TButton")
            self.canvas.bind('<Button-1>', self.zapocni)
            self.canvas.bind("<B1-Motion>",self.crtaj)
            self.canvas.bind('<ButtonRelease-1>', self.stani)
        else:
            self.botunSlika.configure(style="Select.TButton")
            self.botunCrtaj.configure(style="")
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

        

    def zapocni(self,event):
        self.line_points.extend((event.x, event.y))
        
    def crtaj(self,event):
        self.line_points.extend((event.x, event.y))
        if self.line_id is not None:
            self.canvas.delete(self.line_id)
        self.line_id = self.canvas.create_line(self.line_points, fill=self.line_options["fill"], width=self.line_options["width"])

    def stani(self,event=None):
        
        self.skupina.append(self.line_points)
        dodaj={
            "fill":self.line_options["fill"],
            "width":self.line_options["width"]
        }
        self.opcije.append(dodaj)
        self.line_points=[]
        self.line_id=None

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
            if widget==0:
                continue

            widget.textframe.pack_forget()
            widget.dodaci.frame2.pack_forget()

            if widget.dodaci.Var1.get()==1:
                widget.frame3.pack_forget()

            if widget.dodaci.Var2.get()==1:
                widget.canvas.pack_forget()
                widget.frame4.pack_forget()
                widget.frame5.pack_forget()
    
    def __del__(self):
        print("Destruktor se pozvao unos_zad")
        
################################################################################################################################

def tagret(boja):
    if boja=="VISOKA":
        return "red"
    elif boja=="NISKA":
        return "green"
    else:
        return ""

def add_task(event = None):
    task = task_entry.get().strip()
    if task:
        for zad in lista_zadataka.get_children():
            if lista_zadataka.item(zad)["values"][0]==task:
                messagebox.showwarning("Greška u odabiru", "Ne možete odabrati iskorišteno ime!")
                return
        lista_zadataka.insert('', tk.END, values=(task, trenutnavr[0]),tags=tagret(trenutnavr[0]))
        prazan.append(True)
        listaunosa.append(0)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Greška u unosu", "Zadatak ne može biti prazan.")

def remove_task(event=None):
    try:
        selected_task_index = lista_zadataka.index(lista_zadataka.selection())
        selected_task=lista_zadataka.focus()

        #if 0 <= selected_task_index and selected_task_index < len(listaunosa) and not listaunosa[selected_task_index].sadrzaj.strip():

        if listaunosa[selected_task_index] != 0:

            listaunosa[selected_task_index].textframe.destroy()
            listaunosa[selected_task_index].dodaci.frame2.destroy()
            if listaunosa[selected_task_index].dodaci.Var1.get()==1:
                listaunosa[selected_task_index].frame3.destroy()
            if listaunosa[selected_task_index].dodaci.Var2.get()==1:
                listaunosa[selected_task_index].canvas.destroy()
                listaunosa[selected_task_index].frame4.destroy()
                listaunosa[selected_task_index].frame5.destroy()

        listaunosa.remove(listaunosa[selected_task_index])

        prazan[selected_task_index]="del"
        prazan.remove("del")
        lista_zadataka.delete(selected_task)

    except IndexError:
        messagebox.showwarning("Greška u odabiru", "Nije odabran ni jedan zadatak.")

def clear_tasks(event=None,yea=None):
    if yea==1 or messagebox.askyesno("Potvrda", "Obrisati sve zadatke?"):
        for i in listaunosa:
            if i==0:
                continue
            i.textframe.destroy()
            i.dodaci.frame2.destroy()
            if i.dodaci.Var1.get()==1:
                i.frame3.destroy()
            if i.dodaci.Var2.get()==1:
                i.canvas.destroy()
                i.frame4.destroy()
                i.frame5.destroy()
        listaunosa.clear()
        prazan.clear()
        for zadatak in lista_zadataka.get_children():
            lista_zadataka.delete(zadatak)

def on_double_click(event):
    if not lista_zadataka.selection():
        messagebox.showwarning("Greška u odabiru", "Nije odabran ni jedan zadatak.")
        return
        
    selected_task_index = lista_zadataka.index(lista_zadataka.selection())
    selected_task = lista_zadataka.focus()

    for widget in root.winfo_children():
        if widget==menubar:
            root.config(menu="")
            continue
        widget.pack_forget()

    for i in listaunosa:
        if i==0:
            continue
        if i.imezadatka==lista_zadataka.item(selected_task)["values"][0]:
            i.dodaci.frame2.pack()
            i.textframe.pack()
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

    messagebox.showinfo("Novi unos", f"Novi unos u: {lista_zadataka.item(selected_task)["values"][0]}")
    listaunosa[selected_task_index]=unos_zadatka(root,lista_zadataka.item(selected_task)["values"][0],lista_zadataka.item(selected_task)["values"][1],menubar)
    prazan[selected_task_index]=False

def popupdodaj():
    dodati = tk.simpledialog.askstring(title="Unos", prompt="Dodajte zadatak:")
    if dodati:
        for zad in lista_zadataka.get_children():
            if lista_zadataka.item(zad)["values"][0]==dodati:
                messagebox.showwarning("Greška u odabiru", "Ne možete odabrati iskorišteno ime!")
                return
        lista_zadataka.insert('', tk.END, values=(dodati, trenutnavr[0]), tags=tagret(trenutnavr[0]))
        listaunosa.append(0)
        prazan.append(True)
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
        if trenutnifile:
            messagebox.showinfo("Uspješno spremanje", "Datoteka je spremljena.")
        with open(file_path, "wb") as file:
            
            for ind in range(len(prazan)):
                if prazan[ind]==True:
                    prenesi={
                        "prazan": True,
                        "treeime":lista_zadataka.item(lista_zadataka.get_children()[ind])["values"][0],
                        "treekrit":lista_zadataka.item(lista_zadataka.get_children()[ind])["values"][1]
                    }
                    pickle.dump(prenesi,file)
                    continue

                i=listaunosa[ind]
        
                prenesi={
                    "prazan": False,

                    "treeime": i.imezadatka,
                    "treekrit": i.kriticnost,

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
        clear_tasks(None,1)
        with open(file_path, "rb") as file:
            while True:
                try:
                    preneseno = pickle.load(file)
                    if preneseno["prazan"]==True:
                        listaunosa.append(0)
                        lista_zadataka.insert('', tk.END, values=(preneseno["treeime"], preneseno["treekrit"]),tags=tagret(preneseno["treekrit"]))
                        prazan.append(True)
                        continue
                    lista_zadataka.insert('', tk.END, values=(preneseno["treeime"], preneseno["treekrit"]),tags=tagret(preneseno["treekrit"]))
                    prazan.append(False)
                    novi=unos_zadatka(root,preneseno["treeime"],preneseno["treekrit"],menubar)
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

def vraticombo(event):
    trenutnavr.clear()
    trenutnavr.append(zadatakvaznost.get())

####################################################################################################################################

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
style.configure("Select.TButton",foreground="#9a53b2")

trenutnifile=[]

labela = ttk.Label(root, text="Unesite zadatak:", font=("Arial", 20, "bold"), foreground="#333333")
labela.pack(pady=20)

framemain=ttk.Frame(root)
framemain.pack(pady=5)

task_entry = ttk.Entry(framemain, width=40)
task_entry.pack(side=tk.LEFT)
task_entry.bind("<Return>", add_task)

trenutnavr=["SREDNJA"]

vaznosti=["NISKA","SREDNJA","VISOKA"]
zadatakvaznost=ttk.Combobox(framemain,values=vaznosti,state="readonly")
zadatakvaznost.set("Odaberite važnost")
zadatakvaznost.pack(side=tk.RIGHT,padx=5)
zadatakvaznost.bind("<<ComboboxSelected>>",vraticombo)

prazan=[]

add_button = ttk.Button(root, text="Dodaj zadatak (Enter)", command=add_task)
add_button.pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=10, padx=10)

redci=["Ime_zad","Prior"]
lista_zadataka=ttk.Treeview(frame,columns=redci,show="headings",height=20)
lista_zadataka.heading("Ime_zad",text="Ime zadatka")
lista_zadataka.heading("Prior",text="Prioritet")
lista_zadataka.pack(side=tk.LEFT)
lista_zadataka.bind("<Double-Button-1>", on_double_click)
lista_zadataka.bind("<BackSpace>", remove_task)
lista_zadataka.bind("<Control-BackSpace>", clear_tasks)
lista_zadataka.tag_configure("red", foreground="red")
lista_zadataka.tag_configure("green", foreground="green")

scroll_bar = ttk.Scrollbar(frame)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
lista_zadataka.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=lista_zadataka.yview)

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