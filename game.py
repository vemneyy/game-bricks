# Импорт необходимых модулей
from random import randint
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3

# Глобальные переменные для подсчета побед пользователя и компьютера
user_win_count = 0
computer_win_count = 0


def main_game(input_username, main_panel, gender):
    # Создание главного окна Tkinter
    game = Toplevel()
    game.title(f'Игра "Кирпичи": {input_username}')  # Установка заголовка окна
    game.geometry("960x660")  # Установка размеров окна
    game.resizable(False, False)  # Запрет изменения размеров окна
    game.tk.call('tk', 'scaling', 1.4)  # Установка коэффициента масштабирования окна

    # Загрузка изображения фона и установка его в качестве фона окна
    bg = PhotoImage(file="pics/background.png")
    background = Label(game, image=bg)
    background.place(x=0, y=0)

    # Глобальные переменные для использования в функциях
    global hello_phrase
    # Установка иконки окна
    game.iconbitmap("pics/bricks.ico")

    # Создание различных элементов интерфейса (меток и кнопок)
    computer_take = Label(game, text="0", bg="#ffffff", height=2, width=4, font=("Roboto", 30, "bold"), borderwidth=2,
                          relief="solid")
    computer_take.place(x=150, y=280)

    computer_count = Label(game, text="0", bg="#ffffff", height=1, width=2, font=("Roboto", 20, "bold"), borderwidth=2,
                           relief="solid")
    computer_count.place(x=60, y=392)

    user_take = Label(game, text="0", bg="#ffffff", height=2, width=4, font=("Roboto", 30, "bold"), borderwidth=2,
                      relief="solid")
    user_take.place(x=700, y=280)

    user_count = Label(game, text="0", bg="#ffffff", height=1, width=2, font=("Roboto", 20, "bold"), borderwidth=2,
                       relief="solid")
    user_count.place(x=865, y=392)

    ammount = Label(game, text="0", bg="#ffffff", height=2, width=4, font=("Roboto", 30, "bold"), borderwidth=2,
                    relief="solid")
    ammount.place(x=390, y=195)

    btn1 = Button(game, text="Взять 1 кирпич", width=14, height=7, font=("Roboto", 14, "bold"), bg="#CD5C5C",
                  borderwidth=2, relief="solid", command=lambda: user_choice_func(1))
    btn1.place(x=160, y=445)

    btn2 = Button(game, text="Взять 2 кирпича", width=14, height=7, font=("Roboto", 14, "bold"), bg="#ADFF2F",
                  borderwidth=2, relief="solid", command=lambda: user_choice_func(2))
    btn2.place(x=385, y=445)

    btn3 = Button(game, text="Взять 3 кирпича", width=14, height=7, font=("Roboto", 14, "bold"), bg="#00FFFF",
                  borderwidth=2, relief="solid", command=lambda: user_choice_func(3))
    btn3.place(x=610, y=445)

    # Кнопка смены аккаунта
    account_change = Button(game, text="Сменить аккаунт", width=16, height=1, font=("Roboto", 12, "bold"), bg="#90EE90",
                            borderwidth=2, relief="solid", command=lambda: back())
    account_change.place(x=0, y=2)

    # Кнопка перезапуска игры
    restart = Button(game, text="Перезапуск", width=12, height=1, font=("Roboto", 12, "bold"), bg="#90EE90",
                     borderwidth=2, relief="solid", command=lambda: restart_game())
    restart.place(x=165, y=2)

    # Кнопка перехода на страницу с рейтингом
    rate = Button(game, text="Рейтинг", width=12, height=1, font=("Roboto", 12, "bold"), bg="#90EE90",
                  borderwidth=2, relief="solid", command=lambda: show_statistics_window())
    rate.place(x=290, y=2)

    # Кнопка сохранения статистики
    save_stat = Button(game, text="Сохранить статистику", width=19, height=1, font=("Roboto", 12, "bold"), bg="#90EE90",
                       borderwidth=2, relief="solid", command=lambda: save_statistics())
    save_stat.place(x=415, y=2)

    # Кнопка закрытия игры
    quit_btn = Button(game, text="Закрыть игру", width=12, height=1, font=("Roboto", 12, "bold"), bg="#ff0000",
                      borderwidth=2, relief="solid", command=lambda: quit())
    quit_btn.place(x=830, y=2)

    hello_phrase = Label(game, text=f"Удачной игры, {input_username}!", bg="#fffffe", height=2, width=28,
                         font=("Roboto", 16, "bold"),
                         borderwidth=2,
                         relief="solid")
    hello_phrase.place(x=295, y=60)

    # Функции для работы с базой данных и обновления интерфейса
    def connect_db():
        # Подключение к базе данных
        return sqlite3.connect('data/users.db')

    def update_statistics(username, is_win):
        # Обновление статистики пользователя
        conn = connect_db()
        cursor = conn.cursor()

        # Увеличение количества игр
        cursor.execute('UPDATE users SET games = games + 1 WHERE username = ?', (username,))

        # Увеличение количества побед, если пользователь выиграл
        if is_win:
            cursor.execute('UPDATE users SET wins = wins + 1 WHERE username = ?', (username,))

        conn.commit()
        conn.close()

    def fetch_users_statistics():
        conn = sqlite3.connect('data/users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, wins, games FROM users")
        users_data = [(row[0], row[1], row[2], calculate_points(row[1], row[2])) for row in cursor.fetchall()]
        conn.close()
        return users_data

    def calculate_points(wins, games):
        return round((wins / games) * 100) if games > 0 else 0

    def sort_by_column(tree, col, reverse):
        data_list = [(tree.set(k, col), k) for k in tree.get_children('')]
        data_list.sort(reverse=reverse)

        for i, (val, k) in enumerate(data_list):
            tree.move(k, '', i)

        tree.heading(col, command=lambda: sort_by_column(tree, col, not reverse))

    def show_statistics_window():
        stats_window = Toplevel()
        stats_window.title("Рейтинг пользователей")
        stats_window.geometry("600x400")
        stats_window.iconbitmap("pics/bricks.ico")

        columns = ("username", "wins", "games", "points")
        tree = ttk.Treeview(stats_window, columns=columns, show='headings')
        tree.heading("username", text="Имя пользователя", command=lambda: sort_by_column(tree, "username", False))
        tree.heading("wins", text="Выигрыши", command=lambda: sort_by_column(tree, "wins", False))
        tree.heading("games", text="Игры", command=lambda: sort_by_column(tree, "games", False))
        tree.heading("points", text="Очки", command=lambda: sort_by_column(tree, "points", False))

        tree.column("username", width=150)
        tree.column("wins", width=100, anchor=tk.CENTER)
        tree.column("games", width=100, anchor=tk.CENTER)
        tree.column("points", width=100, anchor=tk.CENTER)

        # Заполнение таблицы данными
        for user in fetch_users_statistics():
            tree.insert('', tk.END, values=user)

        tree.pack(expand=True, fill='both')

    # Функции для логики игры
    # Функция отключения и смена цвета кнопок
    def update_button_state():
        ammount_of_bricks = int(ammount['text'])
        if ammount_of_bricks == 2:
            btn3.config(state="disabled", bg="#2fc3c3")
        elif ammount_of_bricks == 1:
            btn2.config(state="disabled", bg="#94c34b")
            btn3.config(state="disabled", bg="#2fc3c3")
        elif ammount_of_bricks == 0:
            btn1.config(state="disabled", bg="#a66565")
            btn2.config(state="disabled", bg="#94c34b")
            btn3.config(state="disabled", bg="#2fc3c3")
        else:
            btn1.config(state="normal", bg="#cd5c5c")
            btn2.config(state="normal", bg="#adff2f")
            btn3.config(state="normal", bg="#00ffff")

    # Функция для возвращения кнопок во включённое состояние
    def restart_button_state():
        btn1.config(state="normal", bg="#cd5c5c")
        btn2.config(state="normal", bg="#adff2f")
        btn3.config(state="normal", bg="#00ffff")
        update_button_state()

    def user_choice_func(userChoice):
        global user_win
        global user_win_count
        user_take['text'] = userChoice
        ammount_of_bricks = int(ammount['text'])  # Получение текущего количества кирпичей

        if ammount_of_bricks == userChoice:
            ammount['text'] = 0

            if 'hello_phrase' in globals():
                hello_phrase.destroy()

            if gender == 0:
                user_win = Label(game, text=f"{input_username} победил", bg="#98FB98", height=2, width=25,
                                 font=("Roboto", 14, "bold"),
                                 borderwidth=3,
                                 relief="solid")
                user_win.place(x=330, y=60)
            elif gender == 1:
                user_win = Label(game, text=f"{input_username} победила", bg="#98FB98", height=2, width=25,
                                 font=("Roboto", 14, "bold"),
                                 borderwidth=3,
                                 relief="solid")
                user_win.place(x=330, y=60)
            user_win_count += 1
            user_count['text'] = user_win_count
            update_button_state()
            update_statistics(input_username, True)
        else:
            ammount_of_bricks -= userChoice
            ammount['text'] = ammount_of_bricks
            pc_func(ammount_of_bricks)

    def pc_turn_final():
        global computer_win
        global computer_win_count
        ammount_of_bricks = int(ammount['text'])

        # Выбор количества кирпичей для взятия компьютером
        computer_choice = min(ammount_of_bricks, 3)

        # Обновление состояния игры
        update_game_state(computer_choice)

    def update_game_state(computer_choice):
        global computer_win
        global computer_win_count
        # Вычитание выбранного количества и обновление интерфейса
        ammount_of_bricks = int(ammount['text']) - computer_choice
        ammount['text'] = 0

        # Отображение сообщения о победе компьютера, если это его последний ход
        if ammount_of_bricks == 0:
            if 'hello_phrase' in globals():
                hello_phrase.destroy()

            computer_win = Label(game, text="Компьютер победил", bg="#FF0033", height=2, width=25,
                                 font=("Roboto", 14, "bold"),
                                 borderwidth=3,
                                 relief="solid")
            computer_win.place(x=330, y=60)
            computer_win_count += 1
            computer_count['text'] = computer_win_count
            update_button_state()
            update_statistics(input_username, False)

    # Функция определения хода компьютера
    def pc_func(ammount_of_bricks):
        if ammount_of_bricks <= 3:
            return pc_turn_final()
        else:
            ammount_of_bricks = int(ammount['text'])
            computerChoice = randint(1, 3)
            computer_take['text'] = computerChoice
            ammount_of_bricks -= computerChoice
            ammount['text'] = ammount_of_bricks
            update_button_state()

    def ammount_of_bricks_func():
        ammount_of_bricks = randint(12, 20)
        ammount['text'] = ammount_of_bricks
        user_take['text'] = 0
        computer_take['text'] = 0

    def restart_game():
        global computer_win
        global user_win
        ammount_of_bricks_func()
        restart_button_state()
        # Очистить метки userWin и computerWin
        if 'user_win' in globals():
            user_win.destroy()
        if 'computer_win' in globals():
            computer_win.destroy()

    def save_statistics():
        global user_win_count, computer_win_count

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT wins, games FROM users WHERE username = ?", (input_username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            total_wins, total_games = user_data
            points = calculate_points(total_wins, total_games)
        else:
            # Если данных о пользователе нет, используем нулевые значения
            total_wins, total_games, points = 0, 0, 0

        try:
            with open("statistics.txt", "w") as file:
                file.write(f"Статистика пользователя {input_username} в данной сессии: \n")
                file.write(f"Выиграно игр: {user_win_count}\n")
                file.write(f"Проиграно игр: {computer_win_count}\n")
                file.write(f"Общее количество выигранных игр: {total_wins}\n")
                file.write(f"Общее количество сыгранных игр: {total_games}\n")
                file.write(f"Очки: {points}")
        except Exception as e:
            print({e})

    def back():
        global user_win_count
        global computer_win_count
        user_win_count = 0
        computer_win_count = 0
        game.destroy()
        main_panel.deiconify()

    # Инициализация начального состояния игры
    ammount_of_bricks_func()
    update_button_state()

    # Запуск главного цикла окна
    game.mainloop()
