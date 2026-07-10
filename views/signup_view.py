import customtkinter as ctk
from tkinter import messagebox
from controllers.auth_controller import register
from widgets.ctk_entry import ThemedEntry

class SignupView(ctk.CTkFrame):
    def __init__(self, parent, on_success, on_back):
        super().__init__(parent, fg_color="#ffd5c7")
        self.on_success = on_success
        self.on_back = on_back
        self._build_ui()

    def _add_placeholder(self, entry, placeholder, show=""):
        entry.insert(0, placeholder)
        entry.configure(text_color="gray")
        entry._placeholder = placeholder
        entry._show = show

        def on_focus_in(event):
            if entry.get() == entry._placeholder:
                entry.delete(0, "end")
                entry.configure(text_color="white")
                if entry._show:
                    entry.configure(show=entry._show)

        def on_focus_out(event):
            if entry.get() == "":
                entry.configure(show="", text_color="gray")
                entry.insert(0, entry._placeholder)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _build_ui(self):
        ctk.CTkLabel(self, text="Create Account", font=("Arial", 28, "bold"),
                     text_color="#713f19").pack(pady=30)

        self.mobile_entry = ThemedEntry(self, width=250)
        self.mobile_entry.pack(pady=8)
        self._add_placeholder(self.mobile_entry, "Mobile Number")

        self.password_entry = ThemedEntry(self, width=250)
        self.password_entry.pack(pady=8)
        self._add_placeholder(self.password_entry, "Password")

        self.confirm_entry = ThemedEntry(self, width=250)
        self.confirm_entry.pack(pady=8)
        self._add_placeholder(self.confirm_entry, "Confirm Password", show="*")

        self.security_question_menu = ctk.CTkOptionMenu(
            self,
            width=250,
            fg_color="#713f19",
            button_color="#aa6f45",
            button_hover_color="#f4c296",
            text_color="#ffffff",
            dropdown_fg_color="#713f19",
            dropdown_hover_color="#f4c296",
            dropdown_text_color="#ffffff",
            values=[
                "What is your mother's maiden name?",
                "What was the name of your first pet?",
                "What city were you born in?",
                "What is your oldest sibling's name?",
            ]
        )
        self.security_question_menu.set("Select Security Question")
        self.security_question_menu.pack(pady=8)

        self.security_answer_entry = ThemedEntry(self, width=250)
        self.security_answer_entry.pack(pady=8)
        self._add_placeholder(self.security_answer_entry, "Security Answer")

        ctk.CTkButton(self, text="SIGN UP", fg_color="#713f19", hover_color="#aa6f45",
                      text_color="white", font=("Arial", 14, "bold"),
                      width=200, height=40, corner_radius=10,
                      command=self._handle_signup).pack(pady=20)

        ctk.CTkButton(self, text="Already have an account? Login",
                      fg_color="transparent", hover_color="#f4c296",
                      text_color="#713f19", font=("Arial", 11),
                      command=self.on_back).pack()

    def _get_value(self, entry):
        value = entry.get()
        return "" if value == entry._placeholder else value

    def _handle_signup(self):
        mobile   = self._get_value(self.mobile_entry)
        password = self._get_value(self.password_entry)
        confirm  = self._get_value(self.confirm_entry)
        question = self.security_question_menu.get()
        answer   = self._get_value(self.security_answer_entry).strip().lower()

        if question == "Select Security Question":
            messagebox.showwarning("Signup Error", "Please select a security question.")
            return

        success, message = register(mobile, password, confirm, question, answer)
        if success:
            messagebox.showinfo("Success", message)
            self.on_success()
        else:
            messagebox.showwarning("Signup Error", message)