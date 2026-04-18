import customtkinter as ctk
import random
import string

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

history = []

def generate_passwords():
    length = length_var.get()
    count = int(count_var.get())
    chars = ""

    if upper_var.get():
        chars += string.ascii_uppercase
    if lower_var.get():
        chars += string.ascii_lowercase
    if digits_var.get():
        chars += string.digits
    if symbols_var.get():
        chars += string.punctuation

    if not chars:
        for lbl in password_labels:
            lbl.configure(text="Select at least one type!")
        return

    for i, lbl in enumerate(password_labels):
        if i < count:
            pwd = "".join(random.choice(chars) for _ in range(length))
            lbl.configure(text=pwd)
        else:
            lbl.configure(text="")

    score = sum([upper_var.get(), lower_var.get(), digits_var.get(), symbols_var.get()])
    colors = ["#ef4444", "#ef4444", "#eab308", "#22c55e", "#22c55e"]
    for i, dot in enumerate(dots):
        dot.configure(text_color=colors[score] if i < score else "#4a5568")

def copy_password(label):
    text = label.cget("text")
    if not text:
        return
    root.clipboard_clear()
    root.clipboard_append(text)
    label.configure(text_color="#22c55e")
    root.after(1000, lambda: label.configure(text_color="#e2e8f0"))

    history.append(text)
    history_text = "📋 Copied:  " + "   |   ".join(history[-3:])
    history_label.configure(text=history_text)

# Окно
root = ctk.CTk()
root.title("Password Generator")
root.geometry("820x650")
root.resizable(False, False)

# Заголовок
header = ctk.CTkFrame(root, corner_radius=0, fg_color="#1e2640")
header.pack(fill="x")
ctk.CTkLabel(header, text="🔒 Advanced Password Generator",
             font=("Helvetica", 22, "bold"), text_color="#a78bfa").pack(pady=(18, 4))
ctk.CTkLabel(header, text="Generate strong and secure passwords",
             font=("Helvetica", 12), text_color="#94a3b8").pack(pady=(0, 18))

# Основной фрейм
main = ctk.CTkFrame(root, fg_color="transparent")
main.pack(fill="both", expand=True, padx=20, pady=20)

# Левая колонка
left = ctk.CTkFrame(main, corner_radius=16, fg_color="#1e2640")
left.pack(side="left", fill="both", expand=True, padx=(0, 10))

ctk.CTkLabel(left, text="≡  Generation Settings",
             font=("Helvetica", 14, "bold"), text_color="#60a5fa").pack(anchor="w", padx=20, pady=(20, 10))

ctk.CTkLabel(left, text="Password Length:", font=("Helvetica", 12),
             text_color="#e2e8f0").pack(anchor="w", padx=20)
length_var = ctk.IntVar(value=16)
ctk.CTkSlider(left, from_=6, to=32, variable=length_var,
              width=240, button_color="#6366f1", button_hover_color="#4f46e5",
              progress_color="#6366f1").pack(padx=20, pady=5)
ctk.CTkLabel(left, textvariable=length_var, font=("Helvetica", 13, "bold"),
             text_color="#60a5fa").pack()

count_frame = ctk.CTkFrame(left, fg_color="transparent")
count_frame.pack(anchor="w", padx=20, pady=10)
ctk.CTkLabel(count_frame, text="🔑 Number of passwords:",
             font=("Helvetica", 12), text_color="#e2e8f0").pack(side="left")
count_var = ctk.StringVar(value="5")
ctk.CTkOptionMenu(count_frame, values=["1", "2", "3", "4", "5"],
                  variable=count_var, width=70,
                  fg_color="#2d3748", button_color="#6366f1").pack(side="left", padx=10)

ctk.CTkLabel(left, text="A  Character Types",
             font=("Helvetica", 14, "bold"), text_color="#60a5fa").pack(anchor="w", padx=20, pady=(15, 5))

upper_var = ctk.BooleanVar(value=True)
lower_var = ctk.BooleanVar(value=True)
digits_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)

for text, var in [("Uppercase letters (A-Z)", upper_var),
                  ("Lowercase letters (a-z)", lower_var),
                  ("Numbers (0-9)", digits_var),
                  ("Special characters (!@#$%)", symbols_var)]:
    ctk.CTkCheckBox(left, text=text, variable=var,
                    font=("Helvetica", 12), text_color="#e2e8f0",
                    checkmark_color="white", fg_color="#6366f1",
                    hover_color="#4f46e5").pack(anchor="w", padx=20, pady=4)

ctk.CTkButton(left, text="⟳  Generate", command=generate_passwords,
              font=("Helvetica", 14, "bold"), height=45,
              fg_color="#6366f1", hover_color="#4f46e5",
              corner_radius=12).pack(fill="x", padx=20, pady=20)

# Правая колонка
right = ctk.CTkFrame(main, corner_radius=16, fg_color="#1e2640")
right.pack(side="left", fill="both", expand=True)

password_labels = []
for i in range(5):
    lbl = ctk.CTkLabel(right, text="", font=("Courier", 13),
                       text_color="#e2e8f0", fg_color="#2d3748",
                       corner_radius=10, cursor="hand2",
                       width=300, height=45)
    lbl.pack(fill="x", padx=20, pady=5, ipady=5)
    lbl.bind("<Button-1>", lambda e, l=lbl: copy_password(l))
    password_labels.append(lbl)

bottom = ctk.CTkFrame(right, fg_color="transparent")
bottom.pack(fill="x", padx=20, pady=10)
ctk.CTkLabel(bottom, text="Strength:",
             font=("Helvetica", 12), text_color="#94a3b8").pack(side="left")

dots = []
for i in range(4):
    dot = ctk.CTkLabel(bottom, text="●", font=("Helvetica", 16),
                       text_color="#4a5568")
    dot.pack(side="left", padx=3)
    dots.append(dot)

# История
history_label = ctk.CTkLabel(root, text="", font=("Courier", 11),
                              text_color="#6c7086", wraplength=780)
history_label.pack(pady=(0, 10))

generate_passwords()
root.mainloop()