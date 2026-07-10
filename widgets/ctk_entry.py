import customtkinter as ctk

def ThemedEntry(parent, **kwargs):
    kwargs.setdefault("fg_color", "#713f19")
    kwargs.setdefault("text_color", "#ffffff")
    kwargs.setdefault("placeholder_text_color", "#f4c296")
    kwargs.setdefault("border_color", "#713f19")
    return ctk.CTkEntry(parent, **kwargs)