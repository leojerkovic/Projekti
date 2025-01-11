"""import tkinter as tk
from tkinter import messagebox

class MyGUI:
    def __init__(self):

        self.root=tk.Tk()
        self.root.title("To-Do List Manager")
        self.root.geometry("1920x1080")

        self.menubar=tk.Menu(self.root)

        self.filemenu=tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close",command=self.on_closing)
    
        self.menubar.add_cascade(label="File",menu=self.filemenu)

        self.root.config(menu=self.menubar)

        self.mainlabel=tk.Label(self.root,text="To-Do List Manager",font=('Arial',18))
        self.mainlabel.pack(padx=10,pady=10)

        self.check_state=tk.IntVar()
        self.button=tk.Button(self.root,text="Dodaj novi zadatak!",font=('Arial',18),command=self.new_task)
        self.button.pack(padx=10,pady=10)

        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.mainloop()

    def new_task(self):
        self.button.pack_forget()

        self.textbox=tk.Text(self.root,height=5,font=('Arial',16))
        self.textbox.bind("<KeyPress>",self.keyboard_entry)
        self.textbox.pack(padx=10,pady=10)

        self.setbtn=tk.Button(self.root,text="Potvrdi unos",font=('Arial',18),command=self.button_entry)
        self.setbtn.pack(padx=10,pady=10)

        self.clearbtn=tk.Button(self.root,text="Očisti unos",font=('Arial',18),command=self.clear)
        self.clearbtn.pack(padx=10,pady=10)
        
    def keyboard_entry(self, event):
        if event.state== 12 and event.keysym=="Return":
            self.content=self.textbox.get('1.0',tk.END)

            self.textbox.pack_forget()
            self.clearbtn.pack_forget()
            self.setbtn.pack_forget()
            self.button.pack()

            output_box = tk.Text(self.root,height=5,width=30,font=('Arial',16))
            output_box.insert("1.0", self.content)
            output_box.config(state="disabled")
            output_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

    def on_closing(self):
        if messagebox.askyesno(title="Izlaz?",message="Je li stvarno želite izac?"):
            self.root.destroy()

    def button_entry(self):
        self.content = self.textbox.get('1.0', tk.END)

        self.textbox.pack_forget()
        self.clearbtn.pack_forget()
        self.setbtn.pack_forget()
        self.button.pack()

        output_box = tk.Text(self.root,height=5,width=30,font=('Arial',16))
        output_box.insert("1.0", self.content)
        output_box.config(state="disabled")
        output_box.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

    def clear(self):
        self.textbox.delete('1.0',tk.END)
        
MyGUI()"""

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class unos_zadatka:
    def __init__(self,root,ime,menubar):
        self.menubar=menubar
        self.imezadatka=ime
        self.sadrzaj=""
        self.zadatak=tk.Text(root,height=10,font=('Arial',16))
        self.zadatak.pack(padx=10,pady=10)
        self.zadatak.bind("<Control-Return>",self.izadi)
        if not (self.sadrzaj.strip()):
            self.zadatak.insert("1.0",self.sadrzaj)
        self.dodajzad = tk.Button(root, text="Izađi (Ctrl+Enter)", command=self.izadi)
        self.dodajzad.pack(pady=5)

    def izadi(self,event=None):
        self.sadrzaj=self.zadatak.get('1.0',tk.END)
        for widget in root.winfo_children():
            if widget==self.menubar:
                root.config(menu=menubar)
                continue
            widget.pack()
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
        if 0 <= selected_task_index and selected_task_index < len(listaunosa):
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

# Input field to add a task
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=10)
task_entry.bind("<Return>", add_task)

# Add Task button
add_button = tk.Button(root, text="Dodaj zadatak (Enter)", command=add_task)
add_button.pack(pady=5)

# Tasks display area (Listbox)
tasks_listbox = tk.Listbox(root, height=15, width=40)
tasks_listbox.pack(pady=10)
tasks_listbox.bind("<Double-Button-1>", on_double_click)
tasks_listbox.bind("<BackSpace>", remove_task)
tasks_listbox.bind("<Control-BackSpace>", clear_tasks)

# Remove Task button
remove_button = tk.Button(root, text="Ukloni zadatak (Backspace)", command=remove_task)
remove_button.pack(pady=5)

# Clear Tasks button
clear_button = tk.Button(root, text="Ukloni sve zadatke (Ctrl + Backspace)", command=clear_tasks)
clear_button.pack(pady=5)

listaunosa=[]

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Izbriši sve", command=clear_tasks)
filemenu.add_command(label="Dodaj novi zadatak", command=popupdodaj)
menubar.add_cascade(label="Zadatci", menu=filemenu)
root.config(menu=menubar)

# Run the application
root.mainloop()
