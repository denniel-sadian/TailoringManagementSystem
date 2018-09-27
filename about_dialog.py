from tkinter import *
from tkinter import ttk


class AboutDialog(Toplevel):

    def __init__(self, master, window_title: str, about_title: str,
                 content: str, bg='lightgray', image=None):
        self.window_title = window_title
        self.about_title = about_title
        self.content = content
        self.bg = bg
        self.image = image
        if self.image:
            self.image = PhotoImage(file=image)
        Toplevel.__init__(self, master)
        self.geometry("+%d+%d" % (
            master.winfo_rootx() + 30,
            master.winfo_rooty() + 30))
        self.resizable(height=False, width=False)
        self.title(self.window_title)
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.focus()
        self.master = master
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        self.create_widgets()

    def ok(self, *args):
        self.destroy()
        return args

    def create_widgets(self):
        frame = Frame(self, borderwidth=2, relief=SUNKEN, bg=self.bg)
        frame.grid(column=0, row=0, sticky='NEWS', pady=5, padx=5)
        # Title
        if self.image:
            Label(frame, image=self.image, bg=self.bg).grid(
                column=0, row=0, pady='5 0')
        Label(frame, text=self.about_title, bg=self.bg,
              font=('courier', 24, 'bold')).grid(
            column=0, row=1)
        ttk.Separator(frame, orient=HORIZONTAL).grid(
            column=0, row=2, sticky='WE', padx=5)
        Label(frame, text=self.content, bg=self.bg, justify='left',
              wraplength=400).grid(
            column=0, row=3, pady=5, padx=5)
        Button(self, text='Ok', command=self.ok).grid(
            column=0, row=4, sticky='WE', pady='0 5', padx=5)


if __name__ == '__main__':
    root = Tk()
    AboutDialog(root, window_title="Window Title",
                about_title="About Title",
                content="This about_dialog.py is written by "
                        "Denniel Luis Saway Sadian. The appearance "
                        "is copied from the IDLE's about dialog.",
                image='py.png').mainloop()
    root.mainloop()