import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from app import *
from db_interface import raw_sql, create, read, update, delete, get_primary_key


# Classes --------------------------

class MultiPageApp(tk.Tk):
    def __init__(self, cnx):
        super().__init__()
        self.cnx = cnx

        # define starting window dimensions
        page_width = 800
        page_height = 600

        self.title("SuppliCore - Nutrition and Supplement Database Manager")
        self.geometry(f"{page_width}x{page_height}")

        # Create the container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Prevent the container from shrinking to fit the frames
        self.container.pack_propagate(False)

        # Dictionary to hold references to frames
        self.frames = {}
        for F in (HomePage, PageDatabase, PageReportEditing, PageSettings):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self, cnx=self.cnx)
            self.frames[page_name] = frame

            # Initially hide all frames
            frame.pack_forget()

        # Show the HomePage by default
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name.
        Hides the current frame and shows the requested one.
        """
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)

class HomePage(ttk.Frame):
    def __init__(self, parent, controller, cnx):
        super().__init__()

        ttk.Label(self, text="Home Page").pack(side="top", anchor=tk.N)

        pack_common_buttons(self, controller)

        homePageButtons = {}
        
        # button - view database
        homePageButtons["view"] = ttk.Button(self, text="Access Database", command=lambda: controller.show_frame("PageDatabase"))
        # button - generate report
        homePageButtons["generate"] = ttk.Button(self, text="Generate Report", command=lambda: controller.show_frame("PageReportEditing"))

        # pack buttons in dict
        for button in homePageButtons.values():
            button.pack()
       
class PageDatabase(ttk.Frame):
    def __init__(self, parent, controller, cnx):
        super().__init__()
        self.cnx = cnx

        pack_common_buttons(self, controller)

        # Page label
        ttk.Label(self, text="Navigate Database").pack(side="top", anchor=tk.N, pady=10)

        # Tables combobox
        ttk.Label(self, text="Table:").pack()
        self.table_combobox = ttk.Combobox(self, state="readonly")
        self.table_combobox.pack(side="top", padx=10, pady=5)
        self.table_combobox.bind("<<ComboboxSelected>>", self.on_table_selected)

        # Entries combobox
        ttk.Label(self, text="Entry:").pack()
        self.entry_combobox = ttk.Combobox(self, state="readonly")
        self.entry_combobox.pack(side="top", padx=10, pady=5)
        self.entry_combobox.bind("<<ComboboxSelected>>", self.on_entry_selected)

        # Frame for displaying entry details
        self.entry_display_frame = ttk.Frame(self)
        self.entry_display_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        self.add_view_fields()

        # Add and Remove buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(side="top", pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Entry", command=self.on_add_entry, state="disabled")
        self.add_button.pack(side="left", padx=5)

        self.remove_button = ttk.Button(self.button_frame, text="Delete Entry", command=self.on_remove_entry, state="disabled")
        self.remove_button.pack(side="left", padx=5)

    def add_view_fields(self):
        """
        Makes the widgets for viewing the database entries
        """       

        # Create Treeview for displaying entry details
        self.tree = ttk.Treeview(self.entry_display_frame, columns=("name", "value"), show='headings', height=10)
        self.tree.heading("name", text="Entry Name")
        self.tree.heading("value", text="Entry Content")
        self.tree.column("name", anchor=tk.W, width=200)
        self.tree.column("value", anchor=tk.W, width=200)
        self.tree.pack(side="left", fill="both", expand=True)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.entry_display_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Update tables
        self.update_tables()

    def update_tables(self):
        """
        Fetch all table names from the database and populate the table ComboBox.
        """
        tables = raw_sql(self.cnx, "SHOW TABLES")
        table_list = tables.iloc[:, 0].tolist()
        filtered_table_list = [table for table in table_list if '_has_' not in table]

        # Populate the ComboBox with table names
        self.table_combobox["values"] = filtered_table_list

    def update_entries(self, selected_table):
        """
        Update the entries combobox with entries from the selected table.
        * Parameters:
            * selected_table: The table from which to fetch the entries
        """
        # Fetch the first three columns of entries from the selected table
        query = f"SELECT * FROM {selected_table}"
        entries = raw_sql(self.cnx, query)

        # Check if the result contains data
        if not entries.empty:
            # Convert the DataFrame to a list of formatted strings
            # Assuming the first column is MRN and the second column is the first name
            entry_list = entries.iloc[:, :3].apply(lambda row: f"{row.iloc[0]} | {row.iloc[1]}", axis=1).tolist()

            # Populate the entry combobox
            self.entry_combobox["values"] = entry_list
            self.entry_combobox.set("")
        else:
            self.entry_combobox["values"] = []

    def on_table_selected(self, event):
        """
        Called when a table is selected. Update the state of the "Add" button.
        """
        selected_table = self.table_combobox.get()
        if selected_table:
            self.add_button["state"] = "normal"
            self.update_entries(selected_table)

    def on_entry_selected(self, event):
        """
        Called when an entry is selected. Update the state of the "Remove" button 
        and display the selected entry's details.
        """
        selected_table = self.table_combobox.get()  # Get the selected table
        selected_entry = self.entry_combobox.get()  # Get the selected entry ID

        if selected_entry:
            self.remove_button["state"] = "normal"

            # Extract the unique identifier (ID) from the entry (assuming the first column is the ID)
            selected_entry_id = selected_entry.split(" | ")[0]

            # Get the primary key for the selected table
            primary_key = get_primary_key(self.cnx, selected_table)

            # Display the details of the selected entry using the correct primary key
            self.display_entry(selected_table, primary_key, selected_entry_id)

    def display_entry(self, selected_table, primary_key, entry_id):
        """
        Display all columns of the selected entry from the selected table in a Treeview.
        * Parameters:
            * selected_table: The table from which to fetch the entry
            * selected_entry_id: The ID of the entry to fetch (or another unique identifier)
        """
        query = f"SELECT * FROM {selected_table} WHERE {primary_key} = '{entry_id}'"
        entry_details = pd.read_sql(query, self.cnx)

        # Clear the treeview and display the new entry details
        self.tree.delete(*self.tree.get_children())
        for column, value in entry_details.iloc[0].items():
            self.tree.insert("", "end", values=(column, value))
    
    def on_add_entry(self):
        """
        Called when the 'Add Entry' button is pressed. Show fields for adding a new entry.
        """
        selected_table = self.table_combobox.get()
        if not selected_table:
            return

        # Clear existing widgets in entry display frame
        for widget in self.entry_display_frame.winfo_children():
            widget.destroy()

        # Fetch the structure of the selected table to display fields
        columns = raw_sql(self.cnx, f"DESCRIBE {selected_table}")

        # For each non-auto-increment field, create an entry widget
        self.add_fields = {}
        for column in columns.itertuples():
            field_name = column.Field
            field_type = column.Type

            if "auto_increment" not in column.Extra or field_name == "patient_id":
                label = ttk.Label(self.entry_display_frame, text=f"{field_name}:")
                label.pack(side="top", anchor=tk.W)
                
                # Create appropriate input widgets based on field type
                if "date" in field_type:
                    entry = DateEntry(self.entry_display_frame, width=12)
                elif "int" in field_type:
                    entry = ttk.Spinbox(self.entry_display_frame, from_=0, to=1000)  # Example for integer field
                else:
                    entry = ttk.Entry(self.entry_display_frame)

                entry.pack(side="top", fill="x", padx=5, pady=2)
                self.add_fields[field_name] = entry

        # Add Submit button
        submit_button = ttk.Button(self.entry_display_frame, text="Submit", command=self.submit_new_entry)
        submit_button.pack(side="left", pady=10, padx=5)

        # Add Back button to return to the previous page
        back_button = ttk.Button(self.entry_display_frame, text="Back", command=self.go_back)
        back_button.pack(side="left", pady=10, padx=5)

    def on_remove_entry(self):
        """
        Triggered when the 'Remove Entry' button is pressed. Remove the selected entry.
        """
        selected_table = self.table_combobox.get()
        selected_entry = self.entry_combobox.get()

        if selected_table and selected_entry:
            # Extract the unique identifier (ID) from the entry (assuming the first part before '|' is the ID)
            selected_entry_id = selected_entry.split(" | ")[0]

            # Get the primary key for the selected table
            primary_key = get_primary_key(self.cnx, selected_table)

            # Call the delete CRUD function, passing the correct primary key and the entry ID
            delete(self.cnx, self, selected_table, selected_entry_id, primary_key)

            print(f"Entry {selected_entry_id} removed from {selected_table}")

    def submit_new_entry(self):
        """
        Called when the user submits the new entry.
        """
        selected_table = self.table_combobox.get()

        if not selected_table:
            return

        # Collect data from the entry fields
        field_data = {field: entry.get() for field, entry in self.add_fields.items()}

        # Use the create function to insert the new entry into the database
        create(self.cnx, self, selected_table, field_data)
        
        print(f"New entry added to {selected_table}")

    def go_back(self):
        """
        Navigates the user back to the database viewing page
        """
        # Clear existing widgets in entry display frame
        for widget in self.entry_display_frame.winfo_children():
            widget.destroy()
        
        # restore viewing widgets
        self.add_view_fields()

class PageReportEditing(ttk.Frame):
    def __init__(self, parent, controller, cnx):
        super().__init__()

        ttk.Label(self, text="Generate Report").pack(side="top", anchor=tk.N)

        pack_common_buttons(self, controller)

        report_labels = {"header": {}, 
                         "food_and_supplements": {},
                         "calculations": {
                             "Holliday-Segar": {}, 
                             "WHO_REE": {}}}
        report_entries = {"header": {}, 
                          "food_and_supplements": {},
                          "calculations": {}}

        create_scrollable(self)


        # header entries
        report_labels["header"]["MRN"] = ttk.Label(self.scrollable_frame, text="MRN:")
        report_entries["header"]["MRN"] = ttk.Entry(self.scrollable_frame)

        report_labels["header"]["name"] = ttk.Label(self.scrollable_frame, text="Patient Name:")
        report_entries["header"]["name"] = ttk.Entry(self.scrollable_frame)

        report_labels["header"]["sex"] = ttk.Label(self.scrollable_frame, text="Sex:")
        report_entries["header"]["sex"] = ttk.Entry(self.scrollable_frame)
        
        report_labels["header"]["DOB"] = ttk.Label(self.scrollable_frame, text="DOB:")
        report_entries["header"]["DOB"] = DateEntry(self.scrollable_frame, date_pattern='yyyy-mm-dd')

        report_labels["header"]["current_date"] = ttk.Label(self.scrollable_frame, text="Current Date:")
        report_entries["header"]["current_date"] = DateEntry(self.scrollable_frame, date_pattern='yyyy-mm-dd')

        report_labels["header"]["age"] = ttk.Label(self.scrollable_frame, text=f"   Age: (Not enough data)")

        report_labels["header"]["weight_kg"] = ttk.Label(self.scrollable_frame, text="Weight (kg):")
        report_entries["header"]["weight_kg"] = ttk.Spinbox(self.scrollable_frame, from_=0, to=1023, textvariable=1, wrap=False)

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

        # calculations

        report_labels["calculations"]["Holliday-Segar"]["title"] = ttk.Label(self.scrollable_frame, text=f"Holliday-Segar:")
        report_labels["calculations"]["Holliday-Segar"]["maintenance"] = ttk.Label(self.scrollable_frame, text=f"   Maintenance: (Not enough data)")
        report_labels["calculations"]["Holliday-Segar"]["sick_day"] = ttk.Label(self.scrollable_frame, text=f"   Sick Day: (Not enough data)")
        report_labels["calculations"]["WHO_REE"] = ttk.Label(self.scrollable_frame, text=f"WHO_REE: (Not enough data)")


        # pack
        pack_recursive(report_labels, report_labels, report_entries)      
    

        # Add fetch button                                          
        ttk.Button(
            self, text="Fetch patient details", command=lambda: fetch(cnx, report_labels, report_entries)).pack()
        
        def fetch(cnx, report_labels, report_entries):
            """
            Called when 'fetch patient details' button is pushed
            Parameters:
                * cnx: the connection to the database
                * report_labels: dict of tk labels
                * report_entries: dict of tk entries
            Returns:
                * dict: the report dict
            """

            # fill report fields
            report = fill_report(cnx, report_labels, report_entries)

            # calculate age
            age_dict = calculate_age(
                datetime.strptime(report_entries["header"]["DOB"].get(), date_format),
                datetime.strptime(report_entries["header"]["current_date"].get(), date_format))
            
            # fill age field
            report_labels["header"]["age"].config(text=f"       Age: {age_dict['age']} {age_dict['age_unit']}")

            return report
            
    
class PageSettings(ttk.Frame):
    def __init__(self, parent, controller, cnx):
        super().__init__()

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
        ttk.Button(self, text="Cancel", command=lambda: fill_settings(settings_entries)).pack()
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
    common_buttons["home"] = ttk.Button(page, text="Home", command=lambda: controller.show_frame("HomePage"))
    # settings
    common_buttons["settings"] = ttk.Button(page, text="Settings", command=lambda: controller.show_frame("PageSettings"))

    # pack buttons in dict
    for button in common_buttons.values():
        button.pack(anchor=tk.NW, side="left", padx=5, pady=10)

def pack_recursive(section, report_labels, report_entries):
    """
    Recursively pack the labels and entries from the dictionary, regardless of depth.
    * Parameters:
        * section - the current section of the dictionary to pack
        * report_labels - the dictionary containing labels
        * report_entries - the dictionary containing entry widgets
    """
    for key in section:
        # If the value is a dictionary, go deeper
        if isinstance(report_labels.get(key, {}), dict):
            # Ensure the key exists in report_entries, even if it's empty
            if key not in report_entries:
                report_entries[key] = {}
            pack_recursive(section[key], report_labels[key], report_entries[key])
        else:
            # Pack the label if exists
            if key in report_labels:
                report_labels[key].pack(anchor=tk.W)
            
            # Pack the entry if exists
            if key in report_entries:
                report_entries[key].pack(anchor=tk.W)

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
    page.bind_all("<MouseWheel>", lambda event: _on_mousewheel(event, canvas, page))

def _on_mousewheel(event, canvas, page):
    """
    Scrolls the page without needing to hover over the scrollbar. 
    Accommodates for different systems.
    Called by a binding made in create_scrollable()
    * Parameters: 
        * event: The scrolling event
        * canvas
        * page
    * Returns: none
    """
    if page.tk.call('tk', 'windowingsystem') == 'win32':
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif page.tk.call('tk', 'windowingsystem') == 'x11':
        canvas.yview_scroll(int(-1 * (event.delta)), "units")
    else:  # MacOS
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

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

def fill_report(cnx, report_labels, report_entries):
    """
    Fill report entries with values from database based on the MRN
    * Parameters:
        * cnx: connection to the database
        * report_labels: dict of tk labels
        * report_entries: dict of tk entries
    * Returns: 
        dict: the report dict
    """

    # get data from database
    mrn = report_entries["header"]["MRN"].get()
    #patient_data = read(cnx, "Patients", "*", f"MRN = '{mrn}'").iloc[0].to_dict()
    patient_report = generate_report(cnx, mrn)
    #print(patient_data)

    # erase current fields
    report_entries["header"]["name"].delete(0, "end")
    report_entries["header"]["DOB"].delete(0, "end")
    report_entries["header"]["sex"].delete(0, "end")
    report_entries["header"]["weight_kg"].delete(0, "end")

    # extract relevant data from patient_data
    report_entries["header"]["name"].insert(0, f"{patient_report['header']['name']}")
    report_entries["header"]["DOB"].insert(0, patient_report['header']["DOB"])
    report_entries["header"]["sex"].insert(0, patient_report['header']["sex"])
    report_entries["header"]["weight_kg"].insert(0, patient_report['header']["weight_kg"])

    # fill fields that depend on patient data
    report_labels["calculations"]["Holliday-Segar"]["maintenance"].config(text=f"   Maintenance: {patient_report['calculations']['Holliday-Segar']['maintenance']}")
    report_labels["calculations"]["Holliday-Segar"]["sick_day"].config(text=f"   Sick Day: {patient_report['calculations']['Holliday-Segar']['sick_day']}")
    report_labels["calculations"]["WHO_REE"].config(text=f"WHO_REE: {patient_report['calculations']['WHO_REE']}")

    return patient_report

def confirm_commit_popup(parent_window=None):
    """
    Shows a confirmation popup for committing database changes.

    * Parameters:
        * parent_window - (Optional) the parent window for the popup
    * Returns: 
        * bool - True if confirmed, False otherwise
    """
    return messagebox.askyesno("Commit Changes", "Are you sure you want to commit these changes?", parent=parent_window)

def show_db_error_popup(error_type, err=None):
    """
    Shows GUI popups based on the error type during database connection.

    * Parameters:
        * error_type: str - The type of error to handle ('access_denied', 'unknown_db', or 'generic')
        * err: Exception - The optional SQLAlchemy error to display (default: None)
    * Returns:
        * bool: Indicates user choice in case of Yes/No dialog, otherwise None
    """
    
    if error_type == "access_denied":
        messagebox.showerror("Error", "Something is wrong with your user name or password.")
    elif error_type == "unknown_db":
        return messagebox.askyesno("Create Database", "Database does not exist. Create new?")
    elif error_type == "generic" and err:
        messagebox.showerror("Database Error", f"An error occurred: {str(err)}")

if __name__ == "__main__":
    # Run main() from app.py
    # The app is normally started by running app.py instead of this file.
    main()
    