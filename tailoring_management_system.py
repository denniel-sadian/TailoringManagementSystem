#! python3
# Denniel Luis Saway Sadian
# July ‎15, ‎2018

from tkinter import *
from tkinter import ttk, font, messagebox
from about_dialog import AboutDialog
import sqlite3
import os


class TailoringManagementSystem(ttk.Frame):

    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.master = master
        # styles
        self.heading = font.Font(family='Kristen ITC', size=18, weight='bold')
        self.style = ttk.Style()
        self.text = font.Font(size=11)
        self.style.configure('TLabel', font=self.text, padding=5)
        self.style.configure('TButton', font=self.text)
        # connecting to the database
        if os.path.exists(f"{os.getcwd()}/tailoring_management_database.db"):
            self.database = sqlite3.connect("tailoring_management_database.db")
            self.cursor = self.database.cursor()
        else:
            self.database = sqlite3.connect("tailoring_management_database.db")
            self.cursor = self.database.cursor()
            self.cursor.execute("CREATE TABLE clients (name string)")
            self.cursor.execute("""
                CREATE TABLE properties (
                    whose string, property string, value string)""")
        self.all_clients = []
        # widgets
        self.client_data_frame = ttk.LabelFrame(
            self, text="Client's Clothes Data", padding=5)
        self.all_clients_frame = ttk.LabelFrame(
            self, text="All Clients", padding=5)
        self.client_name = StringVar()
        self.property = StringVar()
        self.value = StringVar()
        self.temp_properties = []
        self.property_list = StringVar()
        self.property_listbox = Listbox(self.client_data_frame,
                                        listvariable=self.property_list,
                                        width=40, font=self.text)
        self.property_s1 = ttk.Scrollbar(
            self.client_data_frame, orient=VERTICAL,
            command=self.property_listbox.yview)
        self.property_s2 = ttk.Scrollbar(
            self.client_data_frame, orient=HORIZONTAL,
            command=self.property_listbox.xview)
        self.property_listbox['xscrollcommand'] = self.property_s2.set
        self.property_listbox['yscrollcommand'] = self.property_s1.set
        self.client_list = StringVar()
        self.client_listbox = Listbox(self.all_clients_frame,
                                      font=self.text,
                                      listvariable=self.client_list, width=40)
        self.client_s1 = ttk.Scrollbar(
            self.all_clients_frame, orient=VERTICAL,
            command=self.client_listbox.yview)
        self.client_s2 = ttk.Scrollbar(
            self.all_clients_frame, orient=HORIZONTAL,
            command=self.client_listbox.xview)
        self.client_listbox['xscrollcommand'] = self.client_s2.set
        self.client_listbox['yscrollcommand'] = self.client_s1.set
        self.clients_number = IntVar()
        # responsiveness
        for row in range(12):  # rows
            self.rowconfigure(row, weight=1)
            if row < 11 and row is not 8:
                self.client_data_frame.rowconfigure(row, weight=1)
                self.all_clients_frame.rowconfigure(row, weight=1)
        for col in range(7):  # columns
            if col is not 3:
                self.columnconfigure(col, weight=1)
            if col < 3 and col is not 2:
                self.client_data_frame.columnconfigure(col, weight=1)
                self.all_clients_frame.columnconfigure(col, weight=1)
        # creating widgets
        self.create_widgets()
        # calling first update
        self.update_app()
        # events
        self.master.bind('<F1>', self.show_about)
        self.property_listbox.bind('<<ListboxSelect>>', self.show_property)
        self.client_listbox.bind('<<ListboxSelect>>', self.show_client)

    def show_about(self, *args):
        window = AboutDialog(
            self, window_title='About Tailoring Management System',
            about_title='Tailoring Management System',
            content='Developed and written by:\n'
                    '\tDenniel Luis Saway Sadian '
                    '(https://denniel-sadian.github.io)\n\n'
                    'Date of creation:\n'
                    '\tJuly ‎15, ‎2018\n\n'
                    'Description:\n'
                    "\tThis application's purpose is to be used in shops that "
                    "stitch clothes. They don't have to use papers to write down "
                    "their clients' information",
            image='tms.png')
        window.wm_iconbitmap('tms.ico')
        window.mainloop()
        return args

    def add_or_modify_property(self):
        if self.client_name.get() and self.property.get() and self.value.get():
            self.temp_properties.append([self.property.get(), self.value.get()])
            self.update_app()

    def delete_property(self):
        if self.client_name.get() and self.property.get() in \
                self.property_list.get():
            for i in self.temp_properties:
                if i[0] == self.property.get():
                    del self.temp_properties[self.temp_properties.index(i)]
                    break
            self.update_app()

    def show_property(self, *args):
        if len(self.property_listbox.curselection()) == 1:
            index = self.property_listbox.curselection()[0]
            p = self.temp_properties[index][0]
            v = self.temp_properties[index][1]
            self.property.set(p)
            self.value.set(v)
        return args

    def show_client(self, *args):
        if len(self.client_listbox.curselection()) == 1:
            index = self.client_listbox.curselection()[0]
            self.client_name.set(self.all_clients[index])
            self.temp_properties = self.cursor.execute(
                "SELECT property, value FROM properties WHERE whose=?",
                (self.client_name.get(),)).fetchall()
            self.update_app()
        return args

    def update_app(self):
        self.temp_properties = sorted(self.temp_properties, key=lambda p: p[0])
        self.all_clients = []
        for i in self.cursor.execute(
                "SELECT DISTINCT name FROM clients").fetchall():
            self.all_clients.append(i[0])
        self.all_clients = sorted(self.all_clients)
        self.client_list.set(self.all_clients)
        self.property_list.set(list(dict(self.temp_properties)))
        self.clients_number.set(len(self.all_clients))
        self.clear_property_and_value()
        for i in range(0, len(self.temp_properties), 2):
            self.property_listbox.itemconfigure(i, background="#f0f0ff")
        for i in range(0, self.client_listbox.size(), 2):
            self.client_listbox.itemconfigure(i, background="#f0f0ff")

    def clear_property_and_value(self):
        self.property.set('')
        self.value.set('')

    def add_or_modify_client_data(self):
        if self.client_name.get() and len(self.temp_properties):
            if self.client_name.get() not in self.all_clients:
                self.cursor.execute("INSERT INTO clients VALUES (?)",
                                    (self.client_name.get(),))
            self.cursor.execute("DELETE FROM properties WHERE whose=?",
                                (self.client_name.get(),))
            for i in self.temp_properties:
                i = [self.client_name.get()] + list(i)
                self.cursor.execute(
                    "INSERT INTO properties VALUES (?, ?, ?)", i)
            self.database.commit()
            self.temp_properties = []
            self.client_name.set('')
            self.update_app()

    def delete_client(self):
        if self.client_name.get() in self.all_clients:
            if self.client_name.get() and \
                    messagebox.askyesno("Question",
                                        "Do you really want to delete the "
                                        f"record of {self.client_name.get()}"):
                self.cursor.execute("DELETE FROM clients WHERE name=?",
                                    (self.client_name.get(),))
                self.cursor.execute("DELETE FROM properties WHERE whose=?",
                                    (self.client_name.get(),))
                self.database.commit()
                self.client_name.set('')
                self.clear_property_and_value()
                self.temp_properties = []
                self.update_app()
        else:
            messagebox.showinfo('Info',
                                f'{self.client_name.get()} is not in the list.')

    def wipe_database(self):
        if messagebox.askyesno("Warning",
                               "Do you really want to wipe your database out? "
                               "If you do so, all data of your clients will be "
                               "deleted completely. Do you want to proceed?"):
            self.cursor.execute("DROP TABLE clients")
            self.cursor.execute("DROP TABLE properties")
            self.cursor.execute("CREATE TABLE clients (name string)")
            self.cursor.execute("""
                            CREATE TABLE properties (
                                whose string, property string, value string)""")
            self.database.commit()
            self.update_app()

    def create_widgets(self):
        ttk.Label(self, text="Tailoring Management System", font=self.heading) \
            .grid(column=0, row=0, columnspan=8)
        ttk.Separator(self, orient=HORIZONTAL).grid(
            column=0, row=1, sticky='WE', columnspan=8, pady=5)
        self.client_data_frame.grid(column=0, row=2, sticky='NEWS',
                                    columnspan=3, rowspan=10)
        ttk.Label(self.client_data_frame, text="Client's Name:").grid(
            column=0, row=0, sticky='E')
        ttk.Entry(self.client_data_frame, textvariable=self.client_name,
                  font=self.text).grid(
            column=1, row=0, columnspan=2, sticky='NEWS', pady=1)
        ttk.Label(self.client_data_frame, text="Property:").grid(
            column=0, row=1, sticky='E')
        ttk.Entry(self.client_data_frame, textvariable=self.property,
                  font=self.text).grid(
            column=1, row=1, columnspan=2, sticky='NEWS', pady=1)
        ttk.Label(self.client_data_frame, text="Value:").grid(
            column=0, row=2, sticky='E')
        ttk.Entry(self.client_data_frame, textvariable=self.value,
                  font=self.text).grid(
            column=1, row=2, columnspan=2, sticky='NEWS', pady=1)
        ttk.Button(self.client_data_frame, text="Add or Modify Property",
                   command=self.add_or_modify_property).grid(
            column=0, row=3, columnspan=3, sticky='NEWS')
        ttk.Button(self.client_data_frame, text="Delete Property",
                   command=self.delete_property).grid(
            column=0, row=4, columnspan=3, sticky='NEWS')
        self.property_listbox.grid(column=0, row=5, columnspan=2, rowspan=3,
                                   sticky='NEWS')
        self.property_s1.grid(column=2, row=5, rowspan=3, sticky='NSW')
        self.property_s2.grid(column=0, row=8, columnspan=2, sticky='WNE')
        ttk.Button(self.client_data_frame, text="Add or Modify Client Data",
                   command=self.add_or_modify_client_data).grid(
            column=0, row=9, columnspan=3, sticky='NEWS')
        ttk.Button(self.client_data_frame, command=self.delete_client,
                   text="Delete Client").grid(
            column=0, row=10, columnspan=3, sticky='NEWS')
        ttk.Separator(self, orient=VERTICAL).grid(
            column=3, row=2, sticky='NS', rowspan=10, padx=10)
        self.all_clients_frame.grid(column=4, row=2, columnspan=3, rowspan=11,
                                    sticky='NEWS')
        self.client_listbox.grid(column=0, row=0, sticky='NEWS', columnspan=2,
                                 rowspan=8)
        self.client_s1.grid(column=2, row=0, sticky='WNS', rowspan=8)
        self.client_s2.grid(column=0, row=8, sticky='WNE', columnspan=2)
        ttk.Label(self.all_clients_frame, text="All Clients:").grid(
            column=0, row=9)
        ttk.Label(self.all_clients_frame, textvariable=self.clients_number).grid(
            column=1, row=9, columnspan=2)
        ttk.Button(self.all_clients_frame, text="Wipe Database",
                   command=self.wipe_database).grid(
            column=0, row=10, columnspan=3, sticky='NEWS')


if __name__ == '__main__':
    root = Tk()
    app = TailoringManagementSystem(root, padding=5)
    app.grid(column=0, row=0, sticky='NEWS')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title('Tailoring Management System')
    root.wm_iconbitmap('tms.ico')
    root.mainloop()
