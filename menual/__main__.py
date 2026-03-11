import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

from menual.ui import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
