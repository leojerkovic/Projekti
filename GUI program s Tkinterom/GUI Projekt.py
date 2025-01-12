import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class dodaci:
    def __init__(self,root,doit):
        self.frame2 = tk.Frame(root)
        self.frame2.pack()
        
        self.MenuBttn = tk.Menubutton(self.frame2, text = "Dodaci", relief = tk.RAISED)
        
        self.Var1 = tk.IntVar()
        
        self.Menu1 = tk.Menu(self.MenuBttn, tearoff = 0)
        
        self.Menu1.add_checkbutton(label = "Check lista", variable = self.Var1, command=doit)
        
        self.MenuBttn["menu"] = self.Menu1

        self.MenuBttn.pack()
        
    
    def set(self):
        return self.Var1.get()

    def __del__(self):
        print("Destruktor se pozvao dodatci")


class unos_zadatka:
    def __init__(self,root,ime,menubar):
        
        self.dodaci=dodaci(root,self.doit)

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

        print(self.dodaci.Var1.get())

    def doit(self):
            self.frame3 = tk.Frame(root)
            self.frame3.pack()
            
            self.Var1 = tk.IntVar()
            self.Var2 = tk.IntVar()
            
            self.ChkBttn = tk.Checkbutton(self.frame3, width = 15, variable = self.Var1)
            self.ChkBttn.pack(padx = 5, pady = 5)
            
            self.ChkBttn2 = tk.Checkbutton(self.frame3, width = 15, variable = self.Var2)
            self.ChkBttn2.pack(padx = 5, pady = 5)

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
            i.zadatak.pack(padx=10,pady=10)
            i.dodajzad.pack(pady=5)
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

# Main application window
root = tk.Tk()
root.title("Voditelj popisa zadataka")
root.geometry("800x600")  # Set the window size

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

tasks_listbox = tk.Listbox(frame, height=15, width=40)
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
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Izbriši sve", command=clear_tasks)
filemenu.add_command(label="Dodaj novi zadatak", command=popupdodaj)
menubar.add_cascade(label="Zadatci", menu=filemenu)
root.config(menu=menubar)

# Run the application
root.mainloop()
