# Импорт необходимых модулей
from tkinter import *
from auth import auth_func, reg_func


def main_func():
    def func_auth():
        main_panel.withdraw()
        auth_func(main_panel)

    def func_reg():
        main_panel.withdraw()
        reg_func(main_panel)

    main_panel = Tk()
    main_panel.title("Войти / Регистрация")
    main_panel.geometry("460x240")
    main_panel.resizable(False, False)
    main_panel.tk.call('tk', 'scaling', 1.4)
    main_panel.iconbitmap("pics/main_icon.ico")

    root_pic = PhotoImage(file="pics/first_page.png")
    root_background = Label(main_panel, image=root_pic)
    root_background.place(x=0, y=0)

    Button(main_panel, text="Войти", width=20, height=1, font=("Roboto", 14, "bold"), bg="#90EE90",
           borderwidth=2, relief="solid", command=lambda: func_auth()).place(x=107, y=100)

    Button(main_panel, text="Зарегистрироваться", width=20, height=1, font=("Roboto", 14, "bold"),
           bg="#90EE90", borderwidth=2, relief="solid", command=lambda: func_reg()).place(x=107, y=150)

    main_panel.mainloop()


main_func()
