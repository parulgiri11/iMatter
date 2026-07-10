import customtkinter as ctk
from tkinter import messagebox
from controllers.auth_controller import verify_security_answer, reset_password
from widgets.ctk_entry import ThemedEntry


class ForgotPasswordView(ctk.CTkFrame):
    def __init__(self, parent, on_back):
        super().__init__(parent, fg_color="#ffd5c7")
        self.on_back = on_back
        self.verified_mobile = None
        self._build_lookup_ui()

    # ------------------------------------------------------------------ #
    #  Placeholder helper                                                 #
    # ------------------------------------------------------------------ #

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

    def _get_value(self, entry):
        value = entry.get()
        return "" if value == entry._placeholder else value

    # ------------------------------------------------------------------ #
    #  Step 1 — look up account by mobile                                 #
    # ------------------------------------------------------------------ #

    def _build_lookup_ui(self):
        self._clear()

        ctk.CTkLabel(self, text="Forgot Your Password", font=("Arial", 28, "bold"),
                     text_color="#713f19").pack(pady=30)

        self.mobile_entry = ThemedEntry(self, width=250)
        self.mobile_entry.pack(pady=8)
        self._add_placeholder(self.mobile_entry, "Enter your registered Mobile Number")

        ctk.CTkButton(self, text="NEXT", fg_color="#713f19", hover_color="#aa6f45",
                      text_color="white", font=("Arial", 14, "bold"),
                      width=200, height=40, corner_radius=10,
                      command=self._handle_lookup).pack(pady=20)

        ctk.CTkButton(self, text="Back to Login",
                      fg_color="transparent", hover_color="#f4c296",
                      text_color="#713f19", font=("Arial", 11),
                      command=self.on_back).pack()

    # ------------------------------------------------------------------ #
    #  Step 2 — answer security question                                  #
    # ------------------------------------------------------------------ #

    def _build_security_ui(self, question):
        self._clear()

        ctk.CTkLabel(self, text="Security Check", font=("Arial", 28, "bold"),
                     text_color="#713f19").pack(pady=30)

        ctk.CTkLabel(self, text=question, font=("Arial", 12),
                     text_color="#713f19", wraplength=280).pack(pady=(0, 4))

        self.answer_entry = ThemedEntry(self, width=250)
        self.answer_entry.pack(pady=8)
        self._add_placeholder(self.answer_entry, "Enter your answer")

        ctk.CTkButton(self, text="VERIFY", fg_color="#713f19", hover_color="#aa6f45",
                      text_color="white", font=("Arial", 14, "bold"),
                      width=200, height=40, corner_radius=10,
                      command=self._handle_verify).pack(pady=20)

        ctk.CTkButton(self, text="Back",
                      fg_color="transparent", hover_color="#f4c296",
                      text_color="#713f19", font=("Arial", 11),
                      command=self._build_lookup_ui).pack()

    # ------------------------------------------------------------------ #
    #  Step 3 — set new password                                          #
    # ------------------------------------------------------------------ #

    def _build_reset_ui(self):
        self._clear()

        ctk.CTkLabel(self, text="Reset Password", font=("Arial", 28, "bold"),
                     text_color="#713f19").pack(pady=30)

        self.new_password_entry = ThemedEntry(self, width=250)
        self.new_password_entry.pack(pady=8)
        self._add_placeholder(self.new_password_entry, "New Password")

        self.confirm_entry = ThemedEntry(self, width=250)
        self.confirm_entry.pack(pady=8)
        self._add_placeholder(self.confirm_entry, "Confirm New Password", show="*")

        ctk.CTkButton(self, text="RESET PASSWORD", fg_color="#713f19", hover_color="#aa6f45",
                      text_color="white", font=("Arial", 14, "bold"),
                      width=200, height=40, corner_radius=10,
                      command=self._handle_reset).pack(pady=20)

    # ------------------------------------------------------------------ #
    #  Handlers                                                           #
    # ------------------------------------------------------------------ #

    def _handle_lookup(self):
        mobile = self._get_value(self.mobile_entry).strip()
        if not mobile:
            messagebox.showwarning("Error", "Please enter your mobile number.")
            return
        success, result = verify_security_answer(mobile, fetch_only=True)
        if success:
            self.verified_mobile = mobile
            self._build_security_ui(question=result)
        else:
            messagebox.showwarning("Not Found", result)

    def _handle_verify(self):
        answer = self._get_value(self.answer_entry).strip().lower()
        success, message = verify_security_answer(self.verified_mobile, answer=answer)
        if success:
            self._build_reset_ui()
        else:
            messagebox.showwarning("Incorrect", message)

    def _handle_reset(self):
        new_password = self._get_value(self.new_password_entry)
        confirm      = self._get_value(self.confirm_entry)
        success, message = reset_password(self.verified_mobile, new_password, confirm)
        if success:
            messagebox.showinfo("Success", "Password reset! Please log in.")
            self.on_back()
        else:
            messagebox.showwarning("Error", message)

    # ------------------------------------------------------------------ #
    #  Helpers                                                            #
    # ------------------------------------------------------------------ #

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()