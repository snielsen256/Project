import tkinter as tk
from tkinter import ttk
from app import *

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

    common_buttons = {}
    
    # Home button
    common_buttons["home"] = ttk.Button(page, text="Home page", command=lambda: controller.show_frame("HomePage"))
    # settings
    common_buttons["settings"] = ttk.Button(page, text="Settings", command=lambda: controller.show_frame("PageSettings"))

    # pack buttons in dict
    for button in common_buttons.values():
        button.pack(anchor=tk.NW, side="left", padx=5, pady=10)

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Home Page").pack(side="top", anchor=tk.N)

        pack_common_buttons(self, controller)

        homePageButtons = {}
        
        # button - create
        homePageButtons["create"] = ttk.Button(self, text="+ Create", command=lambda: controller.show_frame("PageCreate"))
        # button - view database
        homePageButtons["view"] = ttk.Button(self, text="View Database", command=lambda: controller.show_frame("PageDataSelection"))
        # button - generate report
        homePageButtons["generate"] = ttk.Button(self, text="Generate Report", command=lambda: controller.show_frame("PageReportEditing"))
        # button - import report
        homePageButtons["import"] = ttk.Button(self, text="Import Report File", command=lambda: controller.show_frame("PageImportReport"))

        # pack buttons in dict
        for button in homePageButtons.values():
            button.pack()

class PageCreate(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        pack_common_buttons(self, controller)

        report_labels = {"header": {}}
        report_entries = {"header": {}}

        #header entries

        report_labels["header"]["name"] = ttk.Label(self, text="Patient Name:")
        report_entries["header"]["name"] = ttk.Entry(self)

        report_labels["header"]["sex"] = ttk.Label(self, text="Sex:")
        report_entries["header"]["sex"] = ttk.Entry(self)
        
        report_labels["header"]["MRN"] = ttk.Label(self, text="MRN:")
        report_entries["header"]["MRN"] = ttk.Entry(self)

        report_labels["header"]["DOB"] = ttk.Label(self, text="DOB:")
        report_entries["header"]["DOB"] = ttk.Entry(self)

        report_labels["header"]["age"] = ttk.Label(self, text="Age:")
        report_entries["header"]["age"] = ttk.Entry(self)

        report_labels["header"]["weight_kg"] = ttk.Label(self, text="Weight (kg):")
        report_entries["header"]["weight_kg"] = ttk.Entry(self)

        report_labels["header"]["current_date"] = ttk.Label(self, text="Current Date:")
        report_entries["header"]["current_date"] = ttk.Entry(self)

        report_labels["header"]["feeding_schedule"] = ttk.Label(self, text="Feeding Schedule:")
        report_entries["header"]["feeding_schedule"] = tk.Text(self, height=4)

        report_labels["header"]["method_of_delivery"] = ttk.Label(self, text="Method of Delivery:")
        report_entries["header"]["method_of_delivery"] = tk.Text(self, height=4)

        report_labels["header"]["home_recipe"] = ttk.Label(self, text="Home Recipe:")
        report_entries["header"]["home_recipe"] = tk.Text(self, height=4)

        report_labels["header"]["fluids"] = ttk.Label(self, text="Fluids:")
        report_entries["header"]["fluids"] = tk.Text(self, height=3)

        report_labels["header"]["solids"] = ttk.Label(self, text="Solids:")
        report_entries["header"]["solids"] = tk.Text(self, height=3)

        # pack header
        for section_label_key in report_labels:
            for label_key in report_labels[section_label_key]:
                # Note: making the iteration variables in these loops the keys instead of the values makes it easier to align the dictionaries.
                report_labels[section_label_key][label_key].pack(anchor=tk.W)
                report_entries[section_label_key][label_key].pack(anchor=tk.W)



        

class PageDataSelection(ttk.Frame):#
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
    # Run main() from app.py
    # The app is normally started by running app.py instead of this file.
    main()