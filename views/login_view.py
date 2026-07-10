import customtkinter as ctk
from session import save_session
from controllers.auth_controller import login
from widgets.ctk_dialog import showinfo, showwarning, showerror, askyesno
from widgets.ctk_entry import ThemedEntry


class LoginView(ctk.CTkFrame):

    def __init__(self, parent, on_success, on_signup, on_forgot_password):
        super().__init__(parent, fg_color="#ffd5c7")
        self.on_success = on_success
        self.on_signup = on_signup
        self.on_forgot_password = on_forgot_password
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(content_frame, text="iMatter", font=("Times New Roman", 32, "bold"),
                     text_color="#713f19").pack(pady=(30, 0))

        ctk.CTkLabel(content_frame, text="Every Life Matters", font=("Arial", 15),
                     text_color="#713f19").pack(pady=(0, 20))

        self.mobile_entry = ThemedEntry(content_frame, width=250, placeholder_text="Mobile Number")
        self.mobile_entry.pack(pady=10)

        self.password_entry = ThemedEntry(content_frame, width=250, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(content_frame, text="LOGIN", fg_color="#713f19", hover_color="#aa6f45",
                      text_color="white", font=("Arial", 14, "bold"),
                      width=200, height=40, corner_radius=10,
                      command=self._handle_login).pack(pady=20)

        ctk.CTkButton(content_frame, text="Don't have an account? Sign Up",
                      fg_color="transparent", hover_color="#f4c296",
                      text_color="#713f19", font=("Arial", 11),
                      command=self.on_signup).pack()

        ctk.CTkButton(content_frame, text="Forgot Password?",
                      fg_color="transparent", hover_color="#f4c296",
                      text_color="#713f19", font=("Arial", 11),
                      command=self.on_forgot_password).pack(pady=(4, 0))

        self._add_emergency_buttons(content_frame)

    def _add_emergency_buttons(self, parent):
        emergency_frame = ctk.CTkFrame(parent, fg_color="transparent")
        emergency_frame.pack(pady=(30, 10), fill="x")

        # Row 1: Police and Fire Department
        row1_frame = ctk.CTkFrame(emergency_frame, fg_color="transparent")
        row1_frame.pack(pady=5)

        self.police_btn = ctk.CTkButton(
            row1_frame,
            text="🚔 POLICE",
            fg_color="#1e3a8a",
            hover_color="#1e40af",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=120,
            height=40,
            corner_radius=8,
            command=lambda: self._show_emergency_dialog("POLICE", "100")
        )
        self.police_btn.pack(side="left", padx=10)

        self.fire_btn = ctk.CTkButton(
            row1_frame,
            text="🔥 FIRE DEPARTMENT",
            fg_color="#dc2626",
            hover_color="#b91c1c",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=120,
            height=40,
            corner_radius=8,
            command=lambda: self._show_emergency_dialog("FIRE DEPARTMENT", "101")
        )
        self.fire_btn.pack(side="left", padx=10)

        # Row 2: Women Helpline + Emergency Number
        row2_frame = ctk.CTkFrame(emergency_frame, fg_color="transparent")
        row2_frame.pack(pady=5)


        self.emergency_btn = ctk.CTkButton(
            row2_frame,
            text="🚨 EMERGENCY (112)",
            fg_color="#b45309",
            hover_color="#92400e",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=150,
            height=40,
            corner_radius=8,
            command=lambda: self._show_emergency_dialog("EMERGENCY", "112")
        )
        self.emergency_btn.pack(side="left", padx=10)


        self.women_btn = ctk.CTkButton(
            row2_frame,
            text="👩 WOMEN HELPLINE",
            fg_color="#9d174d",
            hover_color="#831843",
            text_color="white",
            font=("Arial", 12, "bold"),
            width=150,
            height=40,
            corner_radius=8,
            command=lambda: self._show_emergency_dialog("WOMEN HELPLINE", "1091")
        )
        self.women_btn.pack(side="left", padx=10)

    def _show_emergency_dialog(self, department, phone_number):
        confirm = askyesno(
            self,
            f"Call {department}",
            f"Are you sure you want to call {department}?\n\n📞 Number: {phone_number}"
        )
        if confirm:
            showinfo(
                self,
                "Call Initiated",
                f"Calling {department} at {phone_number}\n\nStay safe! 🚨"
            )

    def _handle_login(self):
        mobile = self.mobile_entry.get()
        password = self.password_entry.get()
        success, message, user_id = login(mobile, password)

        if success:
            save_session(mobile, user_id)
            self.pack_forget()
            self.on_success(user_id)
        else:
            showerror(self, "Login Error", message)