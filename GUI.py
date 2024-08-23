import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from app import *


# Classes --------------------------

class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # define starting window dimensions
        page_width = 800
        page_height = 600

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

        create_scrollable(self)

        # header entries
        report_labels["header"]["name"] = ttk.Label(self.scrollable_frame, text="Patient Name:")
        report_entries["header"]["name"] = ttk.Entry(self.scrollable_frame)

        report_labels["header"]["sex"] = ttk.Label(self.scrollable_frame, text="Sex:")
        report_entries["header"]["sex"] = ttk.Entry(self.scrollable_frame)
        
        report_labels["header"]["MRN"] = ttk.Label(self.scrollable_frame, text="MRN:")
        report_entries["header"]["MRN"] = ttk.Entry(self.scrollable_frame)

        report_labels["header"]["DOB"] = ttk.Label(self.scrollable_frame, text="DOB:")
        report_entries["header"]["DOB"] = DateEntry(self.scrollable_frame)
    
        # self.scrollable_frame.age_box = ttk.Frame(canvas)
        # report_labels["header"]["age"] = ttk.Label(self.scrollable_frame.age_box, text="Age:")
        # report_entries["header"]["age"] = ttk.Spinbox(self.scrollable_frame.age_box, from_=0, to=255, textvariable=0, wrap=False)
        # report_entries["header"]["age"]

        report_labels["header"]["weight_kg"] = ttk.Label(self.scrollable_frame, text="Weight (kg):")
        report_entries["header"]["weight_kg"] = ttk.Spinbox(self.scrollable_frame, from_=0, to=1023, textvariable=1, wrap=False)

        report_labels["header"]["current_date"] = ttk.Label(self.scrollable_frame, text="Current Date:")
        report_entries["header"]["current_date"] = DateEntry(self.scrollable_frame)

        report_labels["header"]["feeding_schedule"] = ttk.Label(self.scrollable_frame, text="Feeding Schedule:")
        report_entries["header"]["feeding_schedule"] = tk.Text(self.scrollable_frame, height=4)

        report_labels["header"]["method_of_delivery"] = ttk.Label(self.scrollable_frame, text="Method of Delivery:")
        report_entries["header"]["method_of_delivery"] = tk.Text(self.scrollable_frame, height=4)

        report_labels["header"]["home_recipe"] = ttk.Label(self.scrollable_frame, text="Home Recipe:")
        report_entries["header"]["home_recipe"] = tk.Text(self.scrollable_frame, height=4)

        report_labels["header"]["fluids"] = ttk.Label(self.scrollable_frame, text="Fluids:")
        report_entries["header"]["fluids"] = tk.Text(self.scrollable_frame, height=3)

        report_labels["header"]["solids"] = ttk.Label(self.scrollable_frame, text="Solids:")
        report_entries["header"]["solids"] = tk.Text(self.scrollable_frame, height=3)

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

        settings_labels = {"main": {}}
        settings_entries = {"main": {}}

        create_scrollable(self)

        # entries
        settings_labels["main"]["user"] = ttk.Label(self.scrollable_frame, text="User:")
        settings_entries["main"]["user"] = ttk.Entry(self.scrollable_frame)

        settings_labels["main"]["password"] = ttk.Label(self.scrollable_frame, text="Password:")
        settings_entries["main"]["password"] = ttk.Entry(self.scrollable_frame)

        settings_labels["main"]["host"] = ttk.Label(self.scrollable_frame, text="Host:")
        settings_entries["main"]["host"] = ttk.Entry(self.scrollable_frame)

        settings_labels["main"]["port"] = ttk.Label(self.scrollable_frame, text="Port:")
        settings_entries["main"]["port"] = ttk.Entry(self.scrollable_frame)

        settings_labels["main"]["database"] = ttk.Label(self.scrollable_frame, text="Database:")
        settings_entries["main"]["database"] = ttk.Entry(self.scrollable_frame)

        # pack 
        for section_label_key in settings_labels:
            for label_key in settings_labels[section_label_key]:
                # Note: making the iteration variables in these loops the keys instead of the values makes it easier to align the dictionaries.
                settings_labels[section_label_key][label_key].pack(anchor=tk.W)
                settings_entries[section_label_key][label_key].pack(anchor=tk.W)

        # fill with data from config
        fill_settings(settings_entries)

        # apply and reset buttons
        ttk.Button(self, text="Reset", command=lambda: fill_settings(settings_entries)).pack()
        ttk.Button(self, text="Apply", command=lambda: apply_settings(settings_entries)).pack()


# Functions --------------------

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

def get_fields(report_entries):
    """
    Retrieve the data in the fields
    * Parameters:
        * report_entries: a dict of entry fields. Must be 2 deep
    * Returns: 
       * dict: the data that was in the fields
    """

    output_dict = {"header": {}}

    for section_label_key in report_entries:
        for label_key in report_entries[section_label_key]:
            report_entries[section_label_key][label_key] = report_entries[section_label_key][label_key].get()
        
    return output_dict

def create_scrollable(page):
    """
    Creates a scrollable frame, necessary for all windows.
    * Parameters:
           * page: The argument should always be "self" when called
    * Returns: none

    Note: Scrollable frame is referenced with "self.scrollable_frame", and should be the master for most interactive elements.
    """
    # configure canvas and frame for scrollbar
    canvas = tk.Canvas(page)
    scrollbar = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
    page.scrollable_frame = ttk.Frame(canvas)
    page.scrollable_frame.bind(
        "<Configure>",
        lambda i: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=page.scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def fill_settings(settings_entries):
    """
    Fill settings interface with values from config.json 
    Also used to refresh the settings page without applying changes
    * Parameters: 
        * settings_entries: dict of tk entries
    * Returns: none
    """
    config = load_config()
    for section_label_key in settings_entries:
        for label_key in settings_entries[section_label_key]:
            settings_entries[section_label_key][label_key].delete(0, "end")
            settings_entries[section_label_key][label_key].insert(0, config[label_key])

def apply_settings(settings_entries):
    """
    Replaces values in config.json with the values in the settings page
    * Parameters: 
        * settings_entries: dict of tk entries
    * Returns: none
    """ 

    settings_values = {}

    # convert entries into values
    for section_label_key in settings_entries:
        for label_key in settings_entries[section_label_key]:
            value = settings_entries[section_label_key][label_key].get()
            if label_key == "port": # convert port to int, everything else is a string
                value = int(value)
            settings_values[label_key] = value

    # update config file
    update_config(settings_values)

if __name__ == "__main__":
    # Run main() from app.py
    # The app is normally started by running app.py instead of this file.
    main()

