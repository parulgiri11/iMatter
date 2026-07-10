import customtkinter as ctk
from widgets.ctk_dialog import showinfo, showwarning, askyesno, pick_contact
import webbrowser
import random
from controllers import contact_controller
from widgets.sos_button import SOSButton
from session import clear_session
from widgets.ctk_entry import ThemedEntry

class HomeView(ctk.CTkFrame):
    def __init__(self, parent, on_logout, user_id):
        super().__init__(parent, fg_color="#ffd5c7")
        self.on_logout = on_logout
        self.user_id = user_id
        self._contact_ids = []
        self._editing_id = None
        self._build_ui()
        self.refresh_contacts()

    def _build_ui(self):
        # Scrollable main container
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="#ffd5c7")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure for centering
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # --- Welcome ---
        welcome_label = ctk.CTkLabel(
            self.scrollable_frame,
            text="Welcome to iMatter",
            font=("Times New Roman", 24, "bold"),
            text_color="#713f19",
        )
        welcome_label.pack(pady=20)
        
        # --- SOS Button (Centered) ---
        # Create a container frame to center the SOS button
        sos_wrapper = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        sos_wrapper.pack(pady=16, fill="x")
        
        # Center the button
        sos_center = ctk.CTkFrame(sos_wrapper, fg_color="transparent")
        sos_center.pack(anchor="center")
        
        # Your original SOS button - completely unchanged
        self.sos_button = SOSButton(sos_center, command=self._send_sos, bg="#ffd5c7")
        self.sos_button.pack()
        
        # --- Action Buttons with Responsive Layout ---
        # Row 1: Location & Maps
        row1 = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        row1.pack(pady=6, fill="x", padx=20)
        row1.grid_columnconfigure(0, weight=1)
        row1.grid_columnconfigure(1, weight=1)
        
        live_loc_btn = ctk.CTkButton(
            row1, text="📍 Live Location", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white",
            font=("Arial", 11, "bold"), height=45,
            corner_radius=10, command=self._live_location
        )
        live_loc_btn.grid(row=0, column=0, padx=6, sticky="ew")
        
        maps_btn = ctk.CTkButton(
            row1, text="🗺️ Google Maps", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white",
            font=("Arial", 11, "bold"), height=45,
            corner_radius=10, command=self._open_maps
        )
        maps_btn.grid(row=0, column=1, padx=6, sticky="ew")
        
        # Row 2: Fake Call & Defense Tips
        row2 = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        row2.pack(pady=6, fill="x", padx=20)
        row2.grid_columnconfigure(0, weight=1)
        row2.grid_columnconfigure(1, weight=1)
        
        fake_call_btn = ctk.CTkButton(
            row2, text="📞 Fake Call", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white",
            font=("Arial", 11, "bold"), height=45,
            corner_radius=10, command=self._fake_call
        )
        fake_call_btn.grid(row=0, column=0, padx=6, sticky="ew")
        
        tips_btn = ctk.CTkButton(
            row2, text="🥊 Defense Tips", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white",
            font=("Arial", 11, "bold"), height=45,
            corner_radius=10, command=self._show_tips
        )
        tips_btn.grid(row=0, column=1, padx=6, sticky="ew")
        
        # --- Contacts Section ---
        contacts_title = ctk.CTkLabel(
            self.scrollable_frame,
            text="Emergency Contacts",
            font=("Arial", 18, "bold"),
            text_color="#713f19",
        )
        contacts_title.pack(pady=(20, 8))
        
        # --- Table Container ---
        table_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        table_container.pack(padx=20, pady=(0, 10), fill="x", expand=True)
        
        # Create table with even column distribution
        self._create_table(table_container)
        
        # --- Form Section ---
        self._create_form()
        
        # --- Logout Button ---
        logout_btn = ctk.CTkButton(
            self.scrollable_frame, text="Logout", fg_color="#791f1f",
            hover_color="#a22966", text_color="#d7daf8",
            font=("Arial", 20, "bold"), height=38,
            border_width=0, command=self._logout
        )
        logout_btn.pack(pady=(40, 12))
    
    def _create_table(self, parent):
        """Create the contacts table with fixed column widths for straight divider"""
        # Table frame with border
        self.table_frame = ctk.CTkFrame(parent, fg_color="#aaaaaa", corner_radius=4)
        self.table_frame.pack(fill="x", expand=True)
        
        # Get screen width for responsive but fixed column widths
        name_width = 175
        phone_width = 175
        
        # Configure grid columns with FIXED widths (not weights)
        self.table_frame.grid_columnconfigure(0, minsize=name_width, weight=0)  # Name column - fixed
        self.table_frame.grid_columnconfigure(1, minsize=2, weight=0)  # Divider - fixed tiny width
        self.table_frame.grid_columnconfigure(2, minsize=phone_width, weight=1)  # Phone column - takes remaining space
        
        # Header
        header = ctk.CTkFrame(self.table_frame, fg_color="#713f19", corner_radius=0)
        header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=1, pady=(1, 0))
        
        name_header = ctk.CTkLabel(
            header, text="Name", font=("Arial", 12, "bold"),
            text_color="white", anchor="center", width=name_width
        )
        name_header.grid(row=0, column=0, pady=10, padx=12, sticky="ew")
        
        # Vertical divider in header (FIXED position)
        divider_header = ctk.CTkFrame(header, fg_color="#ffffff", width=2, height=30,
                                    corner_radius=0)
        divider_header.grid(row=0, column=1, sticky="ns", padx=0)
        
        phone_header = ctk.CTkLabel(
            header, text="Phone", font=("Arial", 12, "bold"),
            text_color="white", anchor="center"
        )
        phone_header.grid(row=0, column=2, pady=10, padx=12, sticky="ew")
        
        # Header bottom border
        ctk.CTkFrame(self.table_frame, fg_color="#aaaaaa", height=2,
                    corner_radius=0).grid(row=1, column=0, columnspan=3, sticky="ew")
        
        # Data rows (5 rows)
        self.table_rows = []
        row_bg = "#f9f9f9"
        
        for i in range(5):
            # Row frame
            row_frame = ctk.CTkFrame(self.table_frame, fg_color=row_bg, corner_radius=0)
            row_frame.grid(row=i + 2, column=0, columnspan=3, sticky="ew", padx=1, pady=0)
            
            # Name label with FIXED width
            name_lbl = ctk.CTkLabel(
                row_frame, text="", font=("Arial", 12), text_color="#713f19",
                fg_color=row_bg, height=38, width=name_width, anchor="w"
            )
            name_lbl.grid(row=0, column=0, padx=12, pady=0, sticky="w")
            
            # Vertical divider (FIXED position - straight line)
            divider = ctk.CTkFrame(row_frame, fg_color="#aaaaaa", width=2, height=38,
                                corner_radius=0)
            divider.grid(row=0, column=1, sticky="ns", padx=0)
            
            # Phone label (takes remaining space)
            phone_lbl = ctk.CTkLabel(
                row_frame, text="", font=("Arial", 12), text_color="#713f19",
                fg_color=row_bg, height=38, width=phone_width, anchor="w"
            )
            phone_lbl.grid(row=0, column=2, padx=12, pady=0, sticky="ew")
            
            # Row divider (horizontal line between rows)
            if i < 4:
                ctk.CTkFrame(self.table_frame, fg_color="#aaaaaa", height=2,
                            corner_radius=0).grid(row=i + 3, column=0, columnspan=3, sticky="ew")
            
            # Bind click events for row selection
            name_lbl.bind("<Button-1>", lambda e, idx=i: self._select_row(idx))
            phone_lbl.bind("<Button-1>", lambda e, idx=i: self._select_row(idx))
            
            # Bind hover events
            name_lbl.bind("<Enter>", lambda e, n=name_lbl, p=phone_lbl, bg=row_bg: 
                        self._row_hover(n, p, True, bg))
            name_lbl.bind("<Leave>", lambda e, n=name_lbl, p=phone_lbl, bg=row_bg: 
                        self._row_hover(n, p, False, bg))
            phone_lbl.bind("<Enter>", lambda e, n=name_lbl, p=phone_lbl, bg=row_bg: 
                        self._row_hover(n, p, True, bg))
            phone_lbl.bind("<Leave>", lambda e, n=name_lbl, p=phone_lbl, bg=row_bg: 
                        self._row_hover(n, p, False, bg))
            
            self.table_rows.append((name_lbl, phone_lbl, row_bg))
        
        # Bottom border of table
        ctk.CTkFrame(self.table_frame, fg_color="#aaaaaa", height=2,
                    corner_radius=0).grid(row=7, column=0, columnspan=3, sticky="ew")
        
    def _create_form(self):
        """Create the contact form"""
        # Form label
        self.form_label = ctk.CTkLabel(
            self.scrollable_frame, text="New Contact",
            font=("Arial", 13, "bold"), text_color="#713f19"
        )
        self.form_label.pack(pady=(14, 4))
        
        # Name entry
        self.contact_name_entry = ThemedEntry(
            self.scrollable_frame, width=300,
            placeholder_text="Contact Name"
        )
        self.contact_name_entry.pack(pady=4)
        
        # Phone entry
        self.contact_phone_entry = ThemedEntry(
            self.scrollable_frame, width=300,
            placeholder_text="Phone e.g. +911234567890"
        )
        self.contact_phone_entry.pack(pady=4)
        
        # Validation label
        self.validation_label = ctk.CTkLabel(
            self.scrollable_frame, text="",
            text_color="#e63946", font=("Arial", 11)
        )
        self.validation_label.pack()
        
        # Buttons row
        form_btn_row = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        form_btn_row.pack(pady=8)
        
        self.save_btn = ctk.CTkButton(
            form_btn_row, text="Save Contact", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white", width=140,
            height=36, corner_radius=8, command=self._save_contact
        )
        self.save_btn.grid(row=0, column=0, padx=6)
        
        self.update_btn = ctk.CTkButton(
            form_btn_row, text="Update", fg_color="#713f19",
            hover_color="#aa6f45", text_color="white", width=100,
            height=36, corner_radius=8, command=self._save_edit
        )
        self.update_btn.grid(row=0, column=1, padx=6)
        self.update_btn.grid_remove()
        
        self.delete_btn = ctk.CTkButton(
            form_btn_row, text="Delete", fg_color="#791f1f",
            hover_color="#a22966", text_color="white", border_width=1,
            border_color="#e63946", width=100, height=36,
            corner_radius=8, command=self._delete_contact, state="disabled"
        )
        self.delete_btn.grid(row=0, column=2, padx=6)
        
        self.cancel_btn = ctk.CTkButton(
            form_btn_row, text="Cancel", fg_color="#54626F",
            hover_color="#aa6f45", text_color="white", border_width=1,
            border_color="#54626F", width=100, height=36,
            corner_radius=8, command=self._cancel_edit
        )
        self.cancel_btn.grid(row=0, column=3, padx=6)
        self.cancel_btn.grid_remove()
    
    # All your existing methods remain exactly the same
    def _open_maps(self):
        webbrowser.open("https://www.google.com/maps")


    def refresh_contacts(self):
        self._contact_ids = []
        contacts = contact_controller.fetch_contacts(self.user_id)

        for i, (name_lbl, phone_lbl, bg) in enumerate(self.table_rows):
            if i < len(contacts):
                row = contacts[i]
                self._contact_ids.append(row[0]) 
                name_lbl.configure(text=row[2])   
                phone_lbl.configure(text=row[3])  
            else:
                name_lbl.configure(text="")
                phone_lbl.configure(text="")

        self.update_idletasks()
    
    def _send_sos(self):
        showinfo(self, "SOS Alert", "Emergency SOS Alert Sent Successfully!")
    
    
    def _live_location(self):
        contacts = contact_controller.fetch_contacts(self.user_id)
        if not contacts:
            showinfo(self, "Live Location", "No contacts saved. Add a contact first.")
            return
        name = pick_contact(self, contacts)
        if name:
            showinfo(self, "Live Location", f"📍 Live location shared with {name} successfully!")

    def _fake_call(self):
        contacts = contact_controller.fetch_contacts(self.user_id)
        if not contacts:
            showinfo(self, "Incoming Call", "No contacts saved. Add a contact first.")
            return
        name = pick_contact(self, contacts)
        if name:
            showinfo(self, "Incoming Call", f"📞 {name} Calling...")

    def _show_tips(self):
        tips = (
            "1. Palm Strike\n"
            "2. Elbow Attack\n"
            "3. Knee Strike\n"
            "4. Escape Wrist Grab\n"
            "5. Use Loud Voice\n"
            "6. Stay Alert in Public Areas"
        )
        showinfo(self, "Self Defense Techniques", tips)
    
    def _row_hover(self, name_lbl, phone_lbl, entering, original_bg):
        color = "#f4c296" if entering else original_bg
        name_lbl.configure(fg_color=color)
        phone_lbl.configure(fg_color=color)
    
    def _select_row(self, idx):
        if idx >= len(self._contact_ids):
            return
        cid = self._contact_ids[idx]
        name_lbl, phone_lbl, bg = self.table_rows[idx]
        name = name_lbl.cget("text")
        phone = phone_lbl.cget("text")
        
        self._editing_id = cid
        
        for i, (n, p, bg_color) in enumerate(self.table_rows):
            n.configure(fg_color="#f4c296" if i == idx else bg_color)
            p.configure(fg_color="#f4c296" if i == idx else bg_color)
        
        self.contact_name_entry.delete(0, "end")
        self.contact_name_entry.insert(0, name)
        self.contact_phone_entry.delete(0, "end")
        self.contact_phone_entry.insert(0, phone)
        self.form_label.configure(text=f"Editing: {name}")
        self._set_error("")
        
        self.save_btn.grid_remove()
        self.update_btn.grid()
        self.cancel_btn.grid()
        self.delete_btn.configure(state="normal")
    
    def _cancel_edit(self):
        self._editing_id = None
        self.contact_name_entry.delete(0, "end")
        self.contact_phone_entry.delete(0, "end")
        self.form_label.configure(text="New Contact")
        self._set_error("")
        
        for n, p, bg in self.table_rows:
            n.configure(fg_color=bg)
            p.configure(fg_color=bg)
        
        self.save_btn.grid()
        self.update_btn.grid_remove()
        self.cancel_btn.grid_remove()
        self.delete_btn.configure(state="disabled")
    
    def _validate_form(self):
        name = self.contact_name_entry.get().strip()
        phone = self.contact_phone_entry.get().strip()
        if not name:
            self._set_error("Name cannot be empty.")
            return False
        if not phone:
            self._set_error("Phone cannot be empty.")
            return False
        if not phone.lstrip("+").isdigit():
            self._set_error("Phone must contain digits only.")
            return False
        if len(phone) < 7 or len(phone) > 15:
            self._set_error("Phone must be 7-15 digits.")
            return False
        self._set_error("")
        return True
    
    def _set_error(self, msg):
        self.validation_label.configure(text=msg)
    

    def _save_contact(self):
        if not self._validate_form():
            return
        name = self.contact_name_entry.get().strip()
        phone = self.contact_phone_entry.get().strip()
        success, message = contact_controller.add_contact(self.user_id, name, phone)
        if success:
            self.contact_name_entry.delete(0, "end")
            self.contact_phone_entry.delete(0, "end")
            self._set_error("")
            self.refresh_contacts()
        else:
            self._set_error(message)
    
    def _save_edit(self):
        if not self._validate_form():
            return
        name = self.contact_name_entry.get().strip()
        phone = self.contact_phone_entry.get().strip()
        success, message = contact_controller.modify_contact(self._editing_id, name, phone)
        if success:
            self._cancel_edit()
            self.refresh_contacts()
        else:
            self._set_error(message)
    
    def _delete_contact(self):
        if askyesno(self, "Delete", "Delete this contact?"):
            contact_controller.remove_contact(self._editing_id)
            self._cancel_edit()
            self.refresh_contacts()
    
    def _logout(self):
        if askyesno(self, "Logout", "Are you sure you want to logout?"):
            clear_session()
            self.pack_forget()
            self.on_logout()