import customtkinter as ctk
from security import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

init_db()
create_default_user()

app = ctk.CTk()
app.geometry("900x550")
app.title("SecureAuth System")
app.configure(fg_color="#0f172a")

current_user = None


# ================= LEFT SIDE =================

left_frame = ctk.CTkFrame(app, fg_color="#0f172a")
left_frame.pack(side="left", fill="both", expand=True)

logo = ctk.CTkLabel(
    left_frame,
    text="🔐",
    font=ctk.CTkFont(size=80)
)
logo.pack(pady=(140, 20))

brand = ctk.CTkLabel(
    left_frame,
    text="SecureAuth",
    font=ctk.CTkFont(size=32, weight="bold")
)
brand.pack()

subtitle = ctk.CTkLabel(
    left_frame,
    text="Enterprise Grade Login Security",
    text_color="#94a3b8"
)
subtitle.pack(pady=10)


# ================= RIGHT SIDE =================

right_frame = ctk.CTkFrame(app, fg_color="#0f172a")
right_frame.pack(side="right", fill="both", expand=True)

card = ctk.CTkFrame(
    right_frame,
    width=380,
    height=420,
    corner_radius=25,
    fg_color="#1e293b"
)
card.place(relx=0.5, rely=0.5, anchor="center")
card.pack_propagate(False)

title = ctk.CTkLabel(
    card,
    text="Sign In",
    font=ctk.CTkFont(size=24, weight="bold")
)
title.pack(pady=(50, 25))

username_entry = ctk.CTkEntry(
    card,
    placeholder_text="Username",
    width=230,
    height=45,
    corner_radius=15
)
username_entry.pack(pady=12)

password_entry = ctk.CTkEntry(
    card,
    placeholder_text="Password",
    show="*",
    width=230,
    height=45,
    corner_radius=15
)
password_entry.pack(pady=12)

status_label = ctk.CTkLabel(
    card,
    text="",
    text_color="#f87171"
)
status_label.pack(pady=8)


def login():
    global current_user

    username = username_entry.get()
    password = password_entry.get()

    success, message, attempts = verify_user(username, password)

    if success:
        current_user = username
        show_dashboard(attempts)
    else:
        status_label.configure(text=message)


login_button = ctk.CTkButton(
    card,
    text="Sign In",
    width=160,
    height=42,
    corner_radius=20,
    fg_color="#3b82f6",
    hover_color="#2563eb",
    command=login
)

login_button.pack(pady=25)

# ================= DASHBOARD =================

dashboard_frame = ctk.CTkFrame(app, fg_color="#0f172a")

welcome_label = ctk.CTkLabel(
    dashboard_frame,
    font=ctk.CTkFont(size=28, weight="bold")
)

info_card = ctk.CTkFrame(
    dashboard_frame,
    width=500,
    height=200,
    corner_radius=20,
    fg_color="#1e293b"
)

info_label = ctk.CTkLabel(
    info_card,
    text_color="#94a3b8",
    font=ctk.CTkFont(size=14)
)

footer_label = ctk.CTkLabel(
    dashboard_frame,
    text="© 2026 Esraa Codes",
    text_color="#64748b",
    font=ctk.CTkFont(size=12)
)


def show_dashboard(previous_attempts=0):
    left_frame.pack_forget()
    right_frame.pack_forget()

    dashboard_frame.pack(fill="both", expand=True)

    welcome_label.configure(text=f"Welcome, {current_user} 👋")
    welcome_label.pack(pady=(80, 30))

    attempts, last_login = get_user_info(current_user)

    info_text = f"""
Failed Attempts Before Success: {previous_attempts}

Last Login:
{last_login}
"""

    info_label.configure(text=info_text)

    info_card.pack(pady=20)
    info_label.place(relx=0.5, rely=0.5, anchor="center")

    button_frame = ctk.CTkFrame(dashboard_frame, fg_color="#0f172a")
    button_frame.pack(pady=30)

    ctk.CTkButton(
        button_frame,
        text="Change Password",
        width=200,
        height=45,
        corner_radius=15,
        command=change_pass
    ).pack(side="left", padx=20)

    ctk.CTkButton(
        button_frame,
        text="Logout",
        width=200,
        height=45,
        corner_radius=15,
        fg_color="#ef4444",
        hover_color="#dc2626",
        command=logout
    ).pack(side="right", padx=20)

    footer_label.pack(side="bottom", pady=20)


def logout():
    dashboard_frame.pack_forget()
    left_frame.pack(side="left", fill="both", expand=True)
    right_frame.pack(side="right", fill="both", expand=True)


def change_pass():
    popup = ctk.CTkToplevel(app)
    popup.geometry("400x250")
    popup.title("Change Password")

    label = ctk.CTkLabel(popup, text="Enter New Password")
    label.pack(pady=20)

    entry = ctk.CTkEntry(popup, width=260)
    entry.pack(pady=10)

    def update():
        change_password(current_user, entry.get())
        popup.destroy()

    ctk.CTkButton(popup, text="Update Password", command=update).pack(pady=20)


app.mainloop()
