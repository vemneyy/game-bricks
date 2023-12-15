import os
import re
import sqlite3
from tkinter import *
from game import main_game
import hashlib

# Глобальная переменная для хранения пола пользователя (используется в регистрации)
gender = 10


# Функция для хеширования пароля с использованием SHA-256
def hash_password(password):
    """
    Возвращает хэш SHA-256 от переданного пароля.
    """
    return hashlib.sha256(password.encode()).hexdigest()


# Функция для проверки, пустое ли переданное поле
def is_field_empty(field):
    """
    Проверяет, пустое ли поле.
    """
    return field.strip() == ""


# Функция для проверки, существует ли пользователь с таким логином или email
def user_exists(username, email):
    """
    Проверяет, существует ли уже пользователь с данным логином или email.
    """
    # Здесь используются неопределенные переменные `sql`, возможно, они определены глобально
    user_with_username = sql.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    user_with_email = sql.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()

    if user_with_username or user_with_email:
        return True
    return False


# Функция для проверки, соответствует ли введенный email формату электронной почты
def is_valid_email(email):
    """
    Проверяет, соответствует ли введенный email формату {name}@{domain}.{region}.
    """
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


# Функция для проверки, соответствует ли пароль определенным требованиям
def is_valid_password(password):
    """
    Проверяет, соответствует ли пароль требованиям:
    - не менее 8 символов
    - минимум одна цифра
    - минимум одна буква
    """
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isalpha() for char in password):
        return False
    return True


# Путь до базы данных и подключение
db_path = os.path.join("data/users.db")
connection = sqlite3.connect(db_path)
sql = connection.cursor()

# Создание таблицы пользователей в базе данных, если она еще не существует
sql.execute("CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL,email TEXT NOT NULL,password TEXT NOT NULL, "
            "gender INTEGER NOT NULL, wins INTEGER NOT NULL, games INTEGER NOT NULL );")
connection.commit()


# Функция для авторизации пользователя
def auth_func(main_panel):
    auth_page = Toplevel(main_panel)  # Изменено на Toplevel
    auth_page.title("Авторизация")
    auth_page.geometry("460x280")
    auth_page.resizable(False, False)
    auth_page.tk.call('tk', 'scaling', 1.4)
    auth_page.iconbitmap("pics/main_icon.ico")

    # Функция для перехода к игре
    def back():
        auth_page.destroy()
        main_panel.deiconify()

    # Финальная функция перехода в игру
    def func_auth_success(username_to_game, gender_to_game):
        auth_page.withdraw()
        main_game(username_to_game, main_panel, gender_to_game)

    def login():
        input_identifier = username.get()
        input_password = hash_password(password.get())

        # Поиск пользователя в базе данных
        user = sql.execute("SELECT username, gender FROM users WHERE username = ? AND password = ?",
                           (input_identifier, input_password)).fetchone()

        # Проверка на пустые поля
        if is_field_empty(input_identifier) or is_field_empty(input_password):
            Label(auth_page, text="Все поля должны быть заполнены", fg="#ff0000", bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            return  # Выходим из функции, не продолжая регистрацию

        if user:
            # Если пользователь найден, извлекаем gender и передаем его в функцию func_auth_success
            user_gender = user[1]  # Индекс 1, так как предполагается, что gender следует после username в выборке
            func_auth_success(input_identifier, user_gender)
        else:
            # Если пользователь не найден, очищаем поля ввода
            username.delete(0, END)
            password.delete(0, END)
            Label(auth_page, text="Неверный логин или пароль", fg="#ff0000", bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)

    # Элементы интерфейса окна авторизации: лейблы, поля ввода, кнопки
    # Белый фон
    Label(auth_page, bg="#ffffff", height=300, width=300).place(x=0, y=0)

    # Заголовочный текст
    Label(auth_page, text="АВТОРИЗАЦИЯ", bg="#ffffff", height=1, width=20, font=("Roboto", 26, "bold"), borderwidth=0,
          relief="solid").place(x=5, y=5)

    # Поле логина
    Label(auth_page, text="Логин:", bg="#ffffff", height=1, width=20, font=("Roboto", 12), borderwidth=0,
          relief="solid").place(x=48, y=75)

    username = Entry(auth_page, width=25, font=("Roboto", 12), borderwidth=2, relief="solid", bg="#ffffff",
                     justify="left")
    username.place(x=115, y=100)

    # Поле пароля
    Label(auth_page, text="Пароль:", bg="#ffffff", height=1, width=20, font=("Roboto", 12), borderwidth=0,
          relief="solid").place(x=55, y=135)
    password = Entry(auth_page, show="*", width=25, font=("Roboto", 12), borderwidth=2, relief="solid", bg="#ffffff",
                     justify="left")
    password.place(x=115, y=160)

    # Кнопка для входа
    enter_button = Button(auth_page, text="Войти", width=12, height=1, font=("Roboto", 14, "bold"), bg="#90EE90",
                          borderwidth=2, relief="solid", command=login)
    enter_button.place(x=150, y=210)

    # Кнопка назад
    Button(auth_page, text="<", width=2, height=1, font=("Roboto", 14, "bold"),
           bg="#FF0000", borderwidth=2, relief="solid", command=back).place(x=2, y=0)


def reg_func(main_panel):
    reg_page = Toplevel(main_panel)  # Изменено на Toplevel
    # Установка параметров окна регистрации
    reg_page.title("Регистрация")
    reg_page.geometry("460x360")
    reg_page.resizable(False, False)
    reg_page.tk.call('tk', 'scaling', 1.4)
    reg_page_pic = PhotoImage(file="pics/reg_page.png", master=reg_page)
    reg_page_background = Label(reg_page, image=reg_page_pic)
    reg_page_background.place(x=0, y=0)
    reg_page.iconbitmap("pics/main_icon.ico")

    var = IntVar()
    var.set(10)

    # Кнопка "Назад"
    def back():
        reg_page.destroy()
        main_panel.deiconify()

    # Функция для успешного запуска игры и передачи имени пользователя
    def func_reg_success():
        input_username = username.get()
        reg_page.withdraw()
        main_game(input_username, main_panel, gender)

    # Функция обработки регистрации
    def final():
        global gender
        username_final = username_var.get()
        email_final = email_var.get()
        password_final_wout_hash = password_var.get()
        password_final = hash_password(password_var.get())
        gender_final = var.get()

        # Проверяем, не пустые ли поля
        if is_field_empty(username_final) or is_field_empty(email_final) or is_field_empty(password_final):
            Label(reg_page, text="Все поля должны быть заполнены", fg="#ff0000", bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            return  # Выходим из функции, не продолжая регистрацию

        # Проверяем, выбран ли пол
        if gender_final not in [0, 1]:
            Label(reg_page, text="Пожалуйста, выберите пол", fg="#ff0000", bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            return  # Выходим из функции, не продолжая регистрацию

        if gender_final == 0:
            gender = 0
        elif gender_final == 1:
            gender = 1

        # Функция проверки уже существующего пользователя
        if user_exists(username_final, email_final):
            Label(reg_page, text="Существующий пользователь", fg="#ff0000", bg="#ffffff",
                  height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            return  # Выходим из функции, не продолжая регистрацию

        # Проверяем, соответствует ли введенный email формату
        if not is_valid_email(email_final):
            Label(reg_page, text="Введён неверный формат e-mail.", fg="#ff0000", bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            email.delete(0, END)  # Очищаем поле ввода email
            return  # Выходим из функции, не продолжая регистрацию

        if not is_valid_password(password_final_wout_hash):
            Label(reg_page, text="Слабый пароль", fg="#ff0000",
                  bg="#ffffff", height=1, width=30,
                  font=("Roboto", 12, "bold"), borderwidth=0, relief="solid").place(x=80, y=50)
            password.delete(0, END)  # Очищаем поле ввода пароля
            return  # Выходим из функции, не продолжая регистрацию

        # Выполнение SQL-команды для вставки данных
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                    (username_final, email_final, password_final, gender, 0, 0))

        # Сохранение изменений в базе данных
        connection.commit()

        return func_reg_success()

    # Белый фон
    Label(reg_page, bg="#ffffff", height=300, width=300).place(x=0, y=0)

    # Заголовочный текст
    Label(reg_page, text="РЕГИСТРАЦИЯ", bg="#ffffff", height=1, width=20, font=("Roboto", 26, "bold"), borderwidth=0,
          relief="solid").place(x=10, y=5)

    # Поле логина
    Label(reg_page, text="Логин:", bg="#ffffff", height=1, width=20, font=("Roboto", 12), borderwidth=0,
          relief="solid").place(x=48, y=75)
    username_var = StringVar()
    username = Entry(reg_page, width=25, font=("Roboto", 12), textvariable=username_var, borderwidth=2, relief="solid",
                     bg="#ffffff", justify="left")
    username.place(x=115, y=100)

    # Поле почты
    Label(reg_page, text="Электронная почта:", bg="#ffffff", height=1, width=20, font=("Roboto", 12),
          borderwidth=0, relief="solid").place(x=100, y=135)
    email_var = StringVar()
    email = Entry(reg_page, width=25, font=("Roboto", 12), borderwidth=2, textvariable=email_var, relief="solid",
                  bg="#ffffff", justify="left")
    email.place(x=115, y=160)

    # Поле пароля
    Label(reg_page, text="Пароль:", bg="#ffffff", height=1, width=20, font=("Roboto", 12), borderwidth=0,
          relief="solid").place(x=55, y=195)
    password_var = StringVar()
    password = Entry(reg_page, width=25, font=("Roboto", 12), borderwidth=2, textvariable=password_var, relief="solid",
                     bg="#ffffff", justify="left", show="*")
    password.place(x=115, y=220)

    # Поле выбора пола
    male = Radiobutton(reg_page, text="Мужчина", variable=var, value=0, font=("Roboto", 12), bg="#ffffff")
    female = Radiobutton(reg_page, text="Женщина", variable=var, value=1, font=("Roboto", 12), bg="#ffffff")
    male.place(x=117, y=260)
    female.place(x=235, y=260)

    # Кнопка регистрации
    Button(reg_page, text="Зарегистрироваться", width=18, height=1, font=("Roboto", 14, "bold"),
           bg="#90EE90", borderwidth=2, relief="solid", command=final).place(x=115, y=300)

    # Кнопка "Назад"
    Button(reg_page, text="<", width=2, height=1, font=("Roboto", 14, "bold"),
           bg="#FF0000", borderwidth=2, relief="solid", command=back).place(x=2, y=0)
