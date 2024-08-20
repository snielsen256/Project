import tkinter as tk
from tkinter import ttk

# define starting window dimensions
page_width = 800
page_height = 600


class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SuppliCore - Nutrition and Supplement Database Manager")
        self.geometry(f"{page_width}x{page_height}")

        # Create the container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Make sure the container frame can expand to hold the frames
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, PageDataSelection, PageReportEditing, PageSettings, PageCreate, PageImportReport):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # Place all the frames in the same grid location
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        '''
        Show a frame for the given page name
        '''
        frame = self.frames[page_name]
        frame.tkraise()

def pack_common_buttons(page, controller):
    """
    Adds buttons that are common to every page.
    * Parameters:
           * page: The argument should always be "self" when called.
           * controller: controls page navigation
    * Returns: None 
    """
    
    # Home button
    ttk.Button(page, text="Home page", command=lambda: controller.show_frame("HomePage")).pack()

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Home Page").pack(side="top", fill="x", pady=10)

        # button - settings
        ttk.Button(self, text="Settings", command=lambda: controller.show_frame("PageSettings")).pack()
        # button - create
        ttk.Button(self, text="+ Create", command=lambda: controller.show_frame("PageCreate")).pack()
        # button - view database
        ttk.Button(self, text="View Database", command=lambda: controller.show_frame("PageDataSelection")).pack()
        # button - generate report
        ttk.Button(self, text="Generate Report", command=lambda: controller.show_frame("PageReportEditing")).pack()
        # button - import report
        ttk.Button(self, text="Import Report File", command=lambda: controller.show_frame("PageImportReport")).pack()

class PageCreate(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)
        

        label = ttk.Label(self, text="This is Page One").pack(side="top", fill="x", pady=10)

class PageDataSelection(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)
        

        label = ttk.Label(self, text="This is Page One").pack(side="top", fill="x", pady=10)


class PageReportEditing(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)

        label = ttk.Label(self, text="This is Page Two").pack(side="top", fill="x", pady=10)

class PageImportReport(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)

        label = ttk.Label(self, text="This is Page Two").pack(side="top", fill="x", pady=10)


class PageSettings(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)

        label = ttk.Label(self, text="Settings")
        label.pack(side="top", fill="x", pady=10)

        

        # apply button

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()