import customtkinter as ctk

class CTkDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, mode="info"):
        super().__init__(parent)
        self.result = False
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.attributes("-topmost", True)

        # Size & center over parent
        w, h = 420, 240
        px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        # Mode config — text icon + accent color
        modes = {
            "info":     ("INFO",     "#713f19", "#aa6f45"),
            "warning":  ("WARNING",  "#713f19", "#aa6f45"),
            "error":    ("ERROR",    "#713f19", "#aa6f45"),
            "question": ("CONFIRM",  "#713f19", "#aa6f45"),
        }
        label, accent, accent_dark = modes.get(mode, modes["info"])

        # Colored top accent bar
        accent_bar = ctk.CTkFrame(self, fg_color=accent, height=6, corner_radius=0)
        accent_bar.pack(fill="x")

        # Mode badge
        ctk.CTkLabel(self, text=label,
                     font=("Arial", 10, "bold"),
                     text_color=accent).pack(pady=(14, 0))

        # Title
        ctk.CTkLabel(self, text=title,
                     font=("Arial", 15, "bold")).pack(pady=(4, 0))

        # Message
        ctk.CTkLabel(self, text=message,
                     font=("Arial", 12),
                     wraplength=360,
                     justify="left",
                     anchor="w").pack(pady=(8, 20), padx=30, fill="x")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        if mode == "question":
            ctk.CTkButton(btn_frame, text="Yes", width=110,
                          fg_color="#713f19", hover_color="#aa6f45",
                          corner_radius=8,
                          command=self._yes).pack(side="left", padx=8)
            ctk.CTkButton(btn_frame, text="No", width=110,
                          fg_color="transparent", hover_color="#f8d7da",
                          text_color="#e63946", border_width=1,
                          border_color="#e63946", corner_radius=8,
                          command=self._no).pack(side="left", padx=8)
        else:
            ctk.CTkButton(btn_frame, text="OK", width=140,
                          fg_color=accent, hover_color=accent_dark,
                          corner_radius=8,
                          command=self._ok).pack()

        self.protocol("WM_DELETE_WINDOW", self._no)
        self.wait_window()

    def _ok(self):
        self.result = True
        self.destroy()

    def _yes(self):
        self.result = True
        self.destroy()

    def _no(self):
        self.result = False
        self.destroy()


def showinfo(parent, title, message):
    CTkDialog(parent, title, message, mode="info")

def showwarning(parent, title, message):
    CTkDialog(parent, title, message, mode="warning")

def showerror(parent, title, message):
    CTkDialog(parent, title, message, mode="error")

def askyesno(parent, title, message):
    d = CTkDialog(parent, title, message, mode="question")
    return d.result


class CTkContactPicker(ctk.CTkToplevel):
    def __init__(self, parent, contacts):
        super().__init__(parent)
        self.result = None
        self.title("Select Contact")
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.attributes("-topmost", True)

        w, h = 360, 320
        px = parent.winfo_rootx() + (parent.winfo_width() - w) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - h) // 2
        self.geometry(f"{w}x{h}+{px}+{py}")

        # Accent bar
        ctk.CTkFrame(self, fg_color="#713f19", height=6, corner_radius=0).pack(fill="x")

        ctk.CTkLabel(self, text="SELECT CONTACT",
                     font=("Arial", 10, "bold"),
                     text_color="#713f19").pack(pady=(14, 0))

        ctk.CTkLabel(self, text="Choose a contact",
                     font=("Arial", 15, "bold")).pack(pady=(4, 12))

        if not contacts:
            ctk.CTkLabel(self, text="No contacts saved yet.",
                         font=("Arial", 12),
                         text_color="#888888").pack(pady=20)
            ctk.CTkButton(self, text="OK", width=140,
                          fg_color="#713f19", hover_color="#aa6f45",
                          corner_radius=8,
                          command=self.destroy).pack(pady=(0, 20))
        else:
            # Scrollable contact list
            scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", height=160)
            scroll.pack(fill="x", padx=20)

            for contact in contacts:
                name = contact[2]
                phone = contact[3]
                btn = ctk.CTkButton(
                    scroll,
                    text=f"{name}  |  {phone}",
                    fg_color="#f0faf4",
                    hover_color="#f4c296",
                    text_color="#1b4332",
                    font=("Arial", 12),
                    anchor="w",
                    corner_radius=6,
                    border_width=1,
                    border_color="#b7e4c7",
                    command=lambda n=name: self._pick(n)
                )
                btn.pack(fill="x", pady=3)

            ctk.CTkButton(self, text="Cancel", width=140,
                          fg_color="transparent", hover_color="#f8d7da",
                          text_color="#e63946", border_width=1,
                          border_color="#e63946", corner_radius=8,
                          command=self.destroy).pack(pady=(12, 20))

        self.wait_window()

    def _pick(self, name):
        self.result = name
        self.destroy()


def pick_contact(parent, contacts):
    d = CTkContactPicker(parent, contacts)
    return d.result