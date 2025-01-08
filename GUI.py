import tkinter as tk
import tkinter.font as tkFont
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

        # Define starting window dimensions
        page_width = 800
        page_height = 900

        self.title("SuppliCore - Nutrition and Supplement Database Manager")
        self.geometry(f"{page_width}x{page_height}")
        self.state('zoomed')

        # Create the container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Prevent the container from shrinking to fit the frames
        self.container.pack_propagate(False)

        # Dictionary to hold references to frames
        self.frames = {}
        for F in (HomePage, PageDatabase, PageReportEditing, PageSettings):
            page_name = F.__name__
            # Pass None for `cnx` if it's not available
            frame = F(parent=self.container, controller=self, cnx=self.cnx if self.cnx else None)
            self.frames[page_name] = frame

            # Initially hide all frames
            frame.pack_forget()

        # Show the HomePage by default
        self.show_frame("HomePage")

        # Notify the user if running in limited mode
        if self.cnx is None:
            show_limited_mode_message() 

    def handle_access_database(self, controller, source, destination):
        """
        Checks if database is accessible, shows error if it is not.
        """
        try:
            self.cnx
            controller.show_frame(destination)
        except:
            controller.show_frame(source)
            show_limited_mode_message()

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
        super().__init__(parent)
        self.cnx = cnx
        font_type = "Helvetica"

        # Configure the grid layout for the frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        #Add styles for buttons
        style = ttk.Style()

        #Style home and settings buttons
        style.configure(
            "TopLeft.TButton",
            font=(font_type, 11),
            padding=4,
            relief="flat",
            width=7
        )

        #Style menu buttons
        style.configure(
            "Menu.TButton",
            font=(font_type, 16),
            padding=15,
            relief="flat",
            width=15
        )

        # Home and Settings buttons
        top_left_frame = ttk.Frame(self)
        top_left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        home_button = ttk.Button(
            top_left_frame,
            text="Home",
            command=lambda: controller.show_frame("HomePage"),
            style="TopLeft.TButton"
        )
        settings_button = ttk.Button(
            top_left_frame,
            text="Settings",
            command=lambda: controller.show_frame("PageSettings"),
            style="TopLeft.TButton"
        )

        home_button.pack(side="left", padx=5)
        settings_button.pack(side="left", padx=5)

        # Title
        title_font = tkFont.Font(family=font_type, size=20, weight="bold", underline=1)
        title_label = ttk.Label(self, text="Home Page", font=title_font)        
        title_label.grid(row=0, column=0, pady=(50, 20), sticky="n")

        # Menu buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, pady=20)

        access_db_button = ttk.Button(
            button_frame,
            text="Access Database",
            command=lambda: controller.handle_access_database(controller, source="HomePage", destination="PageDatabase"),
            style="Menu.TButton"
        )

        generate_report_button = ttk.Button(
            button_frame,
            text="Generate Report",
            command= lambda: controller.show_frame("PageReportEditing"),
            style="Menu.TButton"
        )

        access_db_button.pack(pady=5)
        generate_report_button.pack(pady=5)
        
            
       
class PageDatabase(ttk.Frame):
    def __init__(self, parent, controller, cnx):
        super().__init__(parent)
        self.cnx = cnx
        font_type = "Calibri"

        # Configure the grid layout for the frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # Add styles for buttons
        style = ttk.Style()
        style.configure(
            "TopLeft.TButton",
            font=(font_type, 12),
            padding=(5, 5),
            relief="flat"
        )

        # Home and Settings buttons
        top_left_frame = ttk.Frame(self)
        top_left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        home_button = ttk.Button(
            top_left_frame,
            text="Home",
            command=lambda: controller.show_frame("HomePage"),
            style="TopLeft.TButton"
        )
        settings_button = ttk.Button(
            top_left_frame,
            text="Settings",
            command=lambda: controller.show_frame("PageSettings"),
            style="TopLeft.TButton"
        )

        home_button.pack(side="left", padx=5)
        settings_button.pack(side="left", padx=5)

        # Title
        title_font = tkFont.Font(family=font_type, size=20, weight="bold", underline=1)
        title_label = ttk.Label(self, text="Navigate Database", font=title_font)
        title_label.grid(row=0, column=0, pady=(50, 20), sticky="n")

        # Tables combobox
        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, pady=10)

        ttk.Label(table_frame, text="Table:", font=(font_type, 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.table_combobox = ttk.Combobox(table_frame, state="readonly")
        self.table_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.table_combobox.bind("<<ComboboxSelected>>", self.on_table_selected)

        # Entries combobox
        ttk.Label(table_frame, text="Entry:", font=(font_type, 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_combobox = ttk.Combobox(table_frame, state="readonly")
        self.entry_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_combobox.bind("<<ComboboxSelected>>", self.on_entry_selected)

        # Frame for displaying entry details
        self.entry_display_frame = ttk.Frame(self, borderwidth=1, relief="solid")
        self.entry_display_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.add_view_fields()

        # Add and Remove buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, pady=20)

        self.add_button = ttk.Button(
            button_frame,
            text="Add Entry",
            command=self.on_add_entry,
            state="disabled",
            style="TopLeft.TButton",
            width=len("Add Entry") + 2
        )
        self.add_button.pack(side="left", padx=10, pady=5)

        self.update_button = ttk.Button(
            button_frame,
            text="Update Entry",
            command=self.on_update_entry,
            state="disabled",
            style="TopLeft.TButton",
            width=len("Update Entry") + 2
        )
        self.update_button.pack(side="left", padx=10, pady=5)

        self.remove_button = ttk.Button(
            button_frame,
            text="Delete Entry",
            command=self.on_remove_entry,
            state="disabled",
            style="TopLeft.TButton",
            width=len("Delete Entry") + 2
        )
        self.remove_button.pack(side="left", padx=10, pady=5)

    def add_view_fields(self):
        """
        Add fields to the entry display frame
        """
        ttk.Label(self.entry_display_frame, text="Entry Details", font=("Calibri", 12, "italic")).pack()

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
        Called when an entry is selected. Updates the state of the 'Delete Entry' and 'Update Entry' buttons
        and displays the selected entry's details.
        """
        selected_table = self.table_combobox.get()  # Get the selected table
        selected_entry = self.entry_combobox.get()  # Get the selected entry ID

        if selected_entry:
            self.remove_button["state"] = "normal"  # Enable the 'Delete Entry' button
            self.update_button["state"] = "normal"  # Enable the 'Update Entry' button

            # Extract the unique identifier (ID) from the entry (assuming the first column is the ID)
            selected_entry_id = selected_entry.split(" | ")[0]

            # Get the primary key for the selected table
            primary_key = get_primary_key(self.cnx, selected_table)

            # Display the details of the selected entry using the correct primary key
            self.display_entry(selected_table, primary_key, selected_entry_id)
        else:
            # Disable buttons if no entry is selected
            self.remove_button["state"] = "disabled"
            self.update_button["state"] = "disabled"

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
    
    def on_add_entry(self, update_mode=False, entry_details=None, primary_key=None, entry_id=None):
        """
        Show fields for adding or updating an entry, with dropdowns for ENUM fields.
        """
        selected_table = self.table_combobox.get()
        if not selected_table:
            return

        # Clear existing widgets in the entry display frame
        for widget in self.entry_display_frame.winfo_children():
            widget.destroy()

        # Fetch the structure of the selected table to display fields
        columns = raw_sql(self.cnx, f"DESCRIBE {selected_table}")

        # Create a label at the top
        label_text = "Update Entry" if update_mode else "Add New Entry"
        label = ttk.Label(self.entry_display_frame, text=label_text, font=("Calibri", 14, "bold"))
        label.pack(pady=10)

        # Create form fields
        self.add_fields = {}
        for column in columns.itertuples():
            field_name = column.Field
            field_type = column.Type

            if "auto_increment" not in column.Extra:
                field_label = ttk.Label(self.entry_display_frame, text=f"{field_name}:")
                field_label.pack(anchor="w", padx=5, pady=2)

                # Detect ENUM type and create a dropdown list
                if "enum" in field_type.lower():
                    # Extract ENUM values (strip "enum(" and ")")
                    enum_values = field_type[5:-1].replace("'", "").split(",")
                    field_entry = ttk.Combobox(self.entry_display_frame, values=enum_values, state="readonly")

                    # Set default value if updating
                    if entry_details and field_name in entry_details:
                        field_entry.set(entry_details[field_name])
                else:
                    # Default to Entry for other types
                    field_entry = ttk.Entry(self.entry_display_frame)
                    if entry_details and field_name in entry_details:
                        field_entry.insert(0, entry_details[field_name])
                
                field_entry.pack(fill="x", padx=5, pady=2)
                self.add_fields[field_name] = field_entry

        # Buttons for submit and back
        button_frame = ttk.Frame(self.entry_display_frame)
        button_frame.pack(pady=10)

        submit_button = ttk.Button(
            button_frame,
            text="Submit",
            command=lambda: self.submit_entry(update_mode, selected_table, primary_key, entry_id)
        )
        submit_button.pack(side="left", padx=10, ipadx=10)

        back_button = ttk.Button(
            button_frame,
            text="Back",
            command=self.go_back
        )
        back_button.pack(side="left", padx=10, ipadx=10)
    
    def on_update_entry(self):
        """
        Triggered when the 'Update Entry' button is pressed.
        Prepares the form with the selected entry's data.
        """
        selected_table = self.table_combobox.get()
        selected_entry = self.entry_combobox.get()

        if selected_table and selected_entry:
            # Extract the unique identifier (ID) from the entry
            selected_entry_id = selected_entry.split(" | ")[0]

            # Get the primary key for the selected table
            primary_key = get_primary_key(self.cnx, selected_table)

            # Fetch the entry data
            query = f"SELECT * FROM {selected_table} WHERE {primary_key} = '{selected_entry_id}'"
            entry_details = pd.read_sql(query, self.cnx).iloc[0].to_dict()

            # Populate the form
            self.on_add_entry(update_mode=True, entry_details=entry_details, primary_key=primary_key, entry_id=selected_entry_id)

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

    def submit_entry(self, update_mode, table, primary_key=None, entry_id=None):
        """
        Collect field data and submit to the database
        """
        try:
            field_data = {field: entry.get() for field, entry in self.add_fields.items()}

            # Handle nullable or optional fields (like JSON fields)
            columns = raw_sql(self.cnx, f"DESCRIBE {table}")
            for column in columns.itertuples():
                field_name = column.Field
                if "json" in column.Type.lower() and field_name in field_data:
                    # Set nullable JSON fields to None if empty
                    if not field_data[field_name].strip():
                        field_data[field_name] = None

            if update_mode:
                update(self.cnx, self, table, entry_id, field_data)
                messagebox.showinfo("Success", f"Entry successfully updated in {table}.")
            else:
                create(self.cnx, self, table, field_data)
                messagebox.showinfo("Success", f"New entry successfully added to {table}.")

            self.go_back()
        except Exception as e:
            print(f"Error during submission: {e}")
            messagebox.showerror("Error", str(e))

    def submit_new_entry(self):
        """
        Collects field data and submits it to the database.
        """
        selected_table = self.table_combobox.get()
        if not selected_table:
            messagebox.showerror("Error", "No table selected.")
            return

        try:
            # Gather data from input fields
            field_data = {field: entry.get() for field, entry in self.add_fields.items()}

            # Debug: Print the raw collected data
            print(f"Collected field data: {field_data}")

            # Convert date fields to the correct format
            if "DOB" in field_data:
                try:
                    dob = field_data["DOB"]
                    # Convert to MySQL-compatible format
                    dob_formatted = datetime.strptime(dob, "%m/%d/%y").strftime("%Y-%m-%d")
                    field_data["DOB"] = dob_formatted
                except ValueError:
                    messagebox.showerror("Invalid Date", f"Invalid date format for 'DOB': {dob}. Expected MM/DD/YY.")
                    return

            # Debug: Print the prepared field data
            print(f"Final field data (after formatting): {field_data}")

            # Call the `create` function to insert data into the database
            create(self.cnx, self, selected_table, field_data)
            
            # Check if commit was successful
            messagebox.showinfo("Success", f"New entry successfully added to {selected_table}.")

            # Return to the database view page
            self.go_back()

        except Exception as e:
            # Debug: Print detailed error
            print(f"Error during submission: {e}")
            messagebox.showerror("Error", f"An error occurred while adding the entry: {str(e)}")

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
        super().__init__(parent)

        font_type = "Helvetica"

        # Configure the grid layout for the frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Add styles for buttons
        style = ttk.Style()

        # Style home and settings buttons
        style.configure(
            "TopLeft.TButton",
            font=(font_type, 11),
            padding=4,
            relief="flat",
            width=7
        )

        # Title style
        title_font = tkFont.Font(family=font_type, size=20, weight="bold", underline=1)

        # Home and Settings buttons
        top_left_frame = ttk.Frame(self)
        top_left_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        home_button = ttk.Button(
            top_left_frame,
            text="Home",
            command=lambda: controller.show_frame("HomePage"),
            style="TopLeft.TButton"
        )
        settings_button = ttk.Button(
            top_left_frame,
            text="Settings",
            command=lambda: controller.show_frame("PageSettings"),
            style="TopLeft.TButton"
        )

        home_button.pack(side="left", padx=5)
        settings_button.pack(side="left", padx=5)

        # Title
        title_label = ttk.Label(self, text="Generate Report", font=title_font)
        title_label.grid(row=0, column=0, pady=(50, 20), sticky="n")

        # Scrollable content area
        content_frame = ttk.Frame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Create scrollable frame
        self.scrollable_frame = self.create_scrollable(content_frame)

        # Initialize report_labels correctly
        report_labels = {
            "header": {},
            "calculations": {
                "Holliday-Segar": {},
                "WHO_REE": {}
            }
        }
        report_entries = {"header": {}, "calculations": {}}

        # Populate the GUI
        self.create_entry("header", "MRN", "MRN:", report_labels=report_labels, report_entries=report_entries)
        self.create_entry("header", "name", "Patient Name:", report_labels=report_labels, report_entries=report_entries)
        self.create_entry("header", "sex", "Sex:", report_labels=report_labels, report_entries=report_entries)
        self.create_entry("header", "DOB", "DOB:", report_labels=report_labels, report_entries=report_entries)
        self.create_label("header", "age", label_text="Age:", report_labels=report_labels)
        self.create_entry("header", "current_date", "Current Date:", report_labels=report_labels, report_entries=report_entries)
        self.create_entry("header", "weight_kg", "Weight (kg):", entry_type="spinbox", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "condition", "Medical Condition:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "feeding_schedule", "Feeding Schedule:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "method_of_delivery", "Method of Delivery:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "home_recipe", "Home Recipe:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "fluids", "Fluids:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "solids", "Solids:", report_labels=report_labels, report_entries=report_entries)
        self.create_text_entry("header", "medications", "Medications and Supplements:", report_labels=report_labels, report_entries=report_entries)
        self.create_label("calculations", "Holliday-Segar", "maintenance", label_text="Holliday-Segar - Maintenance:", report_labels=report_labels)
        self.create_label("calculations", "Holliday-Segar", "sick_day", label_text="Holliday-Segar - Sick Day:", report_labels=report_labels)
        self.create_label("calculations", "WHO_REE", label_text="WHO REE:", report_labels=report_labels)


        # Add Fetch and Save buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, pady=20)

        fetch_button = ttk.Button(
            button_frame,
            text="Fetch patient details",
            command=lambda: self.fetch(cnx, report_labels, report_entries)
        )
        save_to_computer_button = ttk.Button(
            button_frame,
            text="Save to Computer",
            command=lambda: save_report_JSON(self.get_report_input(cnx, report_labels, report_entries))
        )
        save_to_database_button = ttk.Button(
            button_frame,
            text="Save to Database",
            command=lambda: self.save_to_db(cnx, self.get_report_input(cnx, report_labels, report_entries))
        )

        fetch_button.pack(side="left", padx=10)
        save_to_computer_button.pack(side="left", padx=10)
        save_to_database_button.pack(side="left", padx=10)

    def save_to_db(self, cnx, report_export):
        """
        Saves the report to the database. Helps to format the call to create() correctly.
        Parameters:
            * cnx: the connection to the database
            * report_export: dict, as given by get_report_input()
        """
        create(cnx, self, "reports", {
            "MRN": int(report_export["MRN"]),
            "date": datetime.strptime(report_export["current_date"], "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S"),
            "report": json.dumps(report_export)
        })

        save_info_popup(info_text=f"Saved to database")

    def create_scrollable(self, parent):
        """
        Creates a scrollable frame inside the given parent widget.
        """
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def create_entry(self, section, field_name, label_text, entry_type="entry", report_labels=None, report_entries=None):
        """
        Creates entry widgets for each report section.
        """
        # Create the label for the entry field
        report_labels[section][field_name] = ttk.Label(self.scrollable_frame, text=label_text)
        
        # Create the entry widget
        if entry_type == "entry":
            report_entries[section][field_name] = ttk.Entry(self.scrollable_frame)
        elif entry_type == "spinbox":
            report_entries[section][field_name] = ttk.Spinbox(self.scrollable_frame, from_=0, to=1023)
        
        # Pack the label and entry
        report_labels[section][field_name].pack(anchor=tk.W, pady=5)
        report_entries[section][field_name].pack(anchor=tk.W, pady=5)

    def create_label(self, *keys, label_text, report_labels):
        """
        Creates labels without corresponding input fields, for display-only data.
        Ensures that nested keys exist in the dictionary before adding the label.

        Parameters:
            - *keys: str - The hierarchical keys leading to the label location.
            - label_text: str - The text to display in the label.
            - report_labels: dict - The dictionary holding references to labels.
        """
        # Navigate or create nested dictionary structure
        current_level = report_labels
        for key in keys[:-1]:  # Traverse all keys except the last
            current_level = current_level.setdefault(key, {})

        # Ensure the final key exists
        field_name = keys[-1]
        current_level.setdefault(field_name, None)

        # Create and pack the label
        current_level[field_name] = ttk.Label(self.scrollable_frame, text=label_text)
        current_level[field_name].pack(anchor=tk.W, pady=5)

    def create_text_entry(self, section, field_name, label_text, report_labels=None, report_entries=None):
        """
        Creates text widgets for each report section.
        """
        # Create the label for the text field
        report_labels[section][field_name] = ttk.Label(self.scrollable_frame, text=label_text)
        
        # Create the text widget
        report_entries[section][field_name] = tk.Text(self.scrollable_frame, height=3)
        
        # Pack the label and text widget
        report_labels[section][field_name].pack(anchor=tk.W, pady=5)
        report_entries[section][field_name].pack(anchor=tk.W, pady=5)

    def fetch(self, cnx, report_labels, report_entries):
        """
        Fetch patient details and fill the report.
        
        Parameters:
            - cnx: Database connection
            - report_labels: Dictionary of Tkinter label widgets
            - report_entries: Dictionary of Tkinter entry widgets
        
        Returns:
            - dict: The filled report.
        """
        try:
            # Fetch the MRN and generate the report
            report = fill_report(cnx, report_labels, report_entries)

            # Validate and parse the current_date field
            current_date = report_entries["header"]["current_date"].get().strip()
            if not current_date:
                # Use today's date as a default
                current_date = datetime.now().strftime("%Y-%m-%d")
                report_entries["header"]["current_date"].delete(0, "end")
                report_entries["header"]["current_date"].insert(0, current_date)
            
            # Ensure the date format is correct
            current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")

            # Validate and parse the DOB field
            dob = report_entries["header"]["DOB"].get().strip()
            if not dob:
                raise ValueError("Date of Birth (DOB) is missing.")
            dob_obj = datetime.strptime(dob, "%Y-%m-%d")

            # Calculate age and update the label
            age_dict = calculate_age(dob_obj, current_date_obj)
            report_labels["header"]["age"].config(
                text=f"Age: {age_dict['age']} {age_dict['age_unit']}"
            )

            return report

        except ValueError as e:
            # Display an error message for invalid date formats or missing dates
            messagebox.showerror("Invalid Input", str(e))
            print(f"Error: {e}")


    def get_report_input(self, cnx, report_labels, report_entries):
        """
        Gets information that the user input into the report, and puts it into a dictionary. 
        Parameters:
            * cnx: the connection to the database
            * report_labels: dict of tk labels
            * report_entries: dict of tk entries
        Returns:
            * dict: the report dict
        """
        export_dict = {}

        export_dict["MRN"] = report_entries["header"]["MRN"].get()
        export_dict["name"] = report_entries["header"]["name"].get()
        export_dict["sex"] = report_entries["header"]["sex"].get()
        export_dict["DOB"] = report_entries["header"]["DOB"].get()
        export_dict["current_date"] = report_entries["header"]["current_date"].get()
        export_dict["age"] = report_labels["header"]["age"].cget("text")
        export_dict["weight_kg"] = report_entries["header"]["weight_kg"].get()

        export_dict["feeding_schedule"] = report_entries["header"]["feeding_schedule"].get(1.0, "end-1c")
        export_dict["method_of_delivery"] = report_entries["header"]["method_of_delivery"].get(1.0, "end-1c")
        export_dict["home_recipe"] = report_entries["header"]["home_recipe"].get(1.0, "end-1c")
        export_dict["fluids"] = report_entries["header"]["fluids"].get(1.0, "end-1c")
        export_dict["solids"] = report_entries["header"]["solids"].get(1.0, "end-1c")

        export_dict["Holliday-Segar_m"] = report_labels["calculations"]["Holliday-Segar"]["maintenance"].cget("text")
        export_dict["Holliday-Segar_s"] = report_labels["calculations"]["Holliday-Segar"]["sick_day"].cget("text")
        export_dict["WHO_REE"] = report_labels["calculations"]["WHO_REE"].cget("text")

        # clean dict
        cleaned_content = {}
        for key, value in export_dict.items():
            cleaned_key = key.replace(":", "").replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
            cleaned_content[cleaned_key] = value.strip() if isinstance(value, str) else value

        return cleaned_content

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
    Fills report entries with values from the database based on the MRN.
    
    Parameters:
        - cnx: Database connection
        - report_labels: Dictionary of Tkinter label widgets
        - report_entries: Dictionary of Tkinter entry widgets
    
    Returns:
        - dict: The generated report
    """
    mrn = report_entries["header"]["MRN"].get()
    patient_report = generate_report(cnx, mrn)

    # Fill header fields
    for field in ["name", "DOB", "sex", "weight_kg"]:
        report_entries["header"][field].delete(0, "end")
        report_entries["header"][field].insert(0, patient_report["header"].get(field, ""))

    # Age Label
    age_text = f"Age: {patient_report['header'].get('age', 'N/A')} {patient_report['header'].get('age_unit', '')}"
    report_labels["header"]["age"].config(text=age_text)

    # Calculations
    hs_maintenance = patient_report["calculations"]["Holliday-Segar"]["maintenance"]
    hs_sick_day = patient_report["calculations"]["Holliday-Segar"]["sick_day"]
    who_ree = patient_report["calculations"]["WHO_REE"]

    report_labels["calculations"]["Holliday-Segar"]["maintenance"].config(text=f"Maintenance: {hs_maintenance}")
    report_labels["calculations"]["Holliday-Segar"]["sick_day"].config(text=f"Sick Day: {hs_sick_day}")
    report_labels["calculations"]["WHO_REE"].config(text=f"WHO REE: {who_ree}")

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

def save_info_popup(parent_window=None, info_text=""):
    """
    Shows a popup showing information about where a file was saved.

    * Parameters:
        * parent_window - (Optional) the parent window for the popup
        * info_text - The text shown in the popup
    * Returns: 
        * bool - True if confirmed, False otherwise
    """
    return messagebox.showinfo("Saved", info_text, parent=parent_window)

def show_limited_mode_message():
            """
            Notify the user that the application is running without a database connection.
            """
            messagebox.showwarning(
                "Limited Mode",
                "Can't connect to the database. Reports can still be made, but autofill is disabled."
            )

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
    