import psycopg2
from colorama import Fore, Back, Style
from mini_functions import progress_bar

conn = psycopg2.connect(dbname="postgres",
                        user="postgres",
                        password="Nik10185",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


# Ищу пользователя в базе данных по логину и паролю, которые он ввел на входе
def find_user(username, password):
    cursor.execute('SELECT * '
                   'FROM bank_users '
                   'WHERE user_firstname = %s AND user_password = %s', (username, password,))
    return cursor.fetchone()


# Функция регистрации нового пользователя
def registration():
    login = input('Введите ваш логин (латинские буквы): ')
    user_password = input('Придумайте пароль (мин. 7 символов): ')

    if not login or not user_password:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Логин и пароль должны быть заполнены!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False
    if len(user_password) < 7:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Пароль должен содержать не менее 7 символов!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False
    cursor.execute('SELECT DISTINCT user_firstname '
                   'FROM bank_users ')
    users = cursor.fetchall()
    for user in users:
        if user[0] == login:
            print(f'{Fore.LIGHTRED_EX}----------------------------------',
                  f'Пользователь с таким логином уже есть в системе!',
                  f'Пожалуйста, придумайте другой логин...',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
            return False
    cursor.execute('INSERT INTO bank_users (user_firstname, user_password) '
                   'VALUES (%s, %s)', (login, user_password))
    conn.commit()
    progress_bar()  # функция полоски загрузки
    print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
          f'Регистрация прошла успешно!',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)
    return True
