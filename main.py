# Импорт необходимых модулей
from tkinter import *
from auth import auth_func, reg_func

def main_func():
    # Функция для входа в систему
    def func_auth():
        # Скрывает главное окно
        main_panel.withdraw()
        # Вызывает функцию аутентификации
        auth_func(main_panel)

    # Функция для регистрации
    def func_reg():
        # Скрывает главное окно
        main_panel.withdraw()
        # Вызывает функцию регистрации
        reg_func(main_panel)

    # Создание главного окна
    main_panel = Tk()
    # Заголовок окна
    main_panel.title("Войти / Регистрация")
    # Размер окна
    main_panel.geometry("460x240")
    # Запрет на изменение размера окна
    main_panel.resizable(False, False)
    # Масштабирование элементов окна
    main_panel.tk.call('tk', 'scaling', 1.4)
    # Иконка окна
    main_panel.iconbitmap("pics/main_icon.ico")

    # Загрузка изображения для фона
    root_pic = PhotoImage(file="pics/first_page.png")
    # Установка фонового изображения
    root_background = Label(main_panel, image=root_pic)
    root_background.place(x=0, y=0)

    # Кнопка входа
    Button(main_panel, text="Войти", width=20, height=1, font=("Roboto", 14, "bold"), bg="#90EE90",
           borderwidth=2, relief="solid", command=lambda: func_auth()).place(x=107, y=100)

    # Кнопка регистрации
    Button(main_panel, text="Зарегистрироваться", width=20, height=1, font=("Roboto", 14, "bold"),
           bg="#90EE90", borderwidth=2, relief="solid", command=lambda: func_reg()).place(x=107, y=150)

    # Запуск основного цикла окна
    main_panel.mainloop()

# Вызов главной функции
main_func()
