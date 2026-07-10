import customtkinter as ctk
from database.db import init_db
from views.login_view import LoginView
from views.signup_view import SignupView
from views.home_view import HomeView
from views.forgot_password_view import ForgotPasswordView
from session import save_session, load_session, clear_session
import ctypes

def set_title_bar_color(app, color_hex):
    color_hex = color_hex.lstrip("#")
    r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
    colorref = r | (g << 8) | (b << 16) 
    hwnd = ctypes.windll.user32.GetParent(app.winfo_id())
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(colorref)), 4)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

def main():
    init_db()
    app = ctk.CTk()
    app.title("iMatter")
    app.geometry("500x750")
    app.resizable(True, True)
    app.after(100, lambda: set_title_bar_color(app, "#713f29"))
    app.iconbitmap("")

    def clear_screen():
        for widget in app.winfo_children():
            widget.pack_forget()

    def show_home(user_id):
        clear_screen()
        HomeView(app, on_logout=show_login, user_id=user_id).pack(fill="both", expand=True)

    def show_signup():
        clear_screen()
        SignupView(app, on_success=show_login, on_back=show_login).pack(fill="both", expand=True)

    def show_forgot_password():
        clear_screen()
        ForgotPasswordView(app, on_back=show_login).pack(fill="both", expand=True)

    def show_login():
        clear_screen()
        LoginView(
            app,
            on_success=show_home,
            on_signup=show_signup,
            on_forgot_password=show_forgot_password
        ).pack(fill="both", expand=True)

    session = load_session()
    if session and session[1]:
        show_home(session[1])
    else:
        show_login()

    app.mainloop()

if __name__ == "__main__":
    main()