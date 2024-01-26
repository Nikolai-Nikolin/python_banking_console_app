import psycopg2
from mini_functions import *
from colorama import Fore, Back, Style

conn = psycopg2.connect(dbname="postgres",
                        user="postgres",
                        password="Nik10185",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


# Показываю пользователю информацию по его счетам (команда №1)
def show_user_accounts(bank_user_id):
    cursor.execute("SELECT user_firstname, account_number, balance, description, is_deleted "
                   "FROM bank_users "
                   "JOIN bank_accounts ON bank_users.id = bank_accounts.user_id "
                   "WHERE bank_users.id = %s "
                   "AND is_deleted != True "
                   "ORDER BY balance", (bank_user_id,))
    account_of_user = cursor.fetchall()
    if account_of_user:
        print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
              f'------ Список ваших счетов ------',
              f'                                             ', sep='\n')
        for account in account_of_user:
            print(f'{Fore.LIGHTGREEN_EX}Счет № {account[1]}, баланс: {account[2]}, {account[3]}',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
    else:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Счета не найдены',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)


# Снимаем деньги со своего счета (команда №2)
def withdraw_money(bank_user_id):
    account_number = input('Введите номер счета: ')
    amount = input('Введите сумму снятия: ')
    if not account_number or not amount:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Номер счета и сумма снятия должны быть заполнены!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if not account_number.isdigit() or not amount.isdigit():
        print(f'{Fore.LIGHTYELLOW_EX}----------------------------------',
              f'Я вас не поняла, попробуйте вводить только цифры!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    cursor.execute('SELECT * FROM bank_accounts '
                   'WHERE account_number = %s '
                   'AND user_id = %s '
                   'AND is_deleted != True', (account_number, bank_user_id))
    account = cursor.fetchone()
    if account:
        if account[2] >= int(amount):
            cursor.execute('UPDATE bank_accounts '
                           'SET balance = balance - %s '
                           'WHERE account_number = %s', (int(amount), account_number))
            print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
                  f'Вы сняли со счета {account_number} сумму в размере {amount}',
                  f'Баланс счета {account_number} теперь равен {account[2] - int(amount)}',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
        else:
            print(f'{Fore.LIGHTRED_EX}----------------------------------',
                  f'На счете {account_number} недостаточно средств',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
    else:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Счет не найден',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
    conn.commit()


# Вносим деньги себе на счет (команда #3)
def deposit_money(bank_user_id):
    account_number = input('Введите номер счета: ')
    amount = input('Введите сумму пополнения: ')
    if not account_number or not amount:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Номер счета и сумма пополнения должны быть заполнены!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if not account_number.isdigit() or not amount.isdigit():
        print(f'{Fore.LIGHTYELLOW_EX}----------------------------------',
              f'Я вас не поняла, попробуйте вводить только цифры!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    cursor.execute('SELECT * FROM bank_accounts '
                   'WHERE account_number = %s '
                   'AND user_id = %s '
                   'AND is_deleted != True', (account_number, bank_user_id))
    account = cursor.fetchone()
    if account:
        cursor.execute('UPDATE bank_accounts '
                       'SET balance = balance + %s '
                       'WHERE account_number = %s', (int(amount), account_number))
        progress_bar()  # функция полоски загрузки
        print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
              f'Вы внесли на счет {account_number} сумму в размере {amount}',
              f'Баланс счета {account_number} теперь равен {account[2] + int(amount)}',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        conn.commit()
        return
    print(f'{Fore.LIGHTRED_EX}----------------------------------',
          f'Счет не найден! Пожалуйста, проверьте правильность ввода номера счета',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)


# Переводим деньги на свой/чужой счет (команда №4)
def transfer_money(bank_user_id):
    from_account = input('Введите номер счета для списания средств: ')
    to_account = input('Введите номер счета для зачисления средств: ')
    amount = input('Введите сумму перевода: ')
    if not from_account or not to_account or not amount:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Номера счетов и сумма перевода должны быть заполнены!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if not from_account.isdigit() or not to_account.isdigit() or not amount.isdigit():
        print(f'{Fore.LIGHTYELLOW_EX}----------------------------------',
              f'Я вас не поняла, попробуйте вводить только цифры!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    cursor.execute('SELECT balance '
                   'FROM bank_accounts '
                   'WHERE account_number = %s', (from_account,))
    balance = cursor.fetchone()[0]
    if balance < int(amount):
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              'Недостаточно средств на счете',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False

    cursor.execute('WITH first_account AS (SELECT account_number FROM bank_accounts WHERE account_number = %s), '
                   'second_account AS (SELECT account_number FROM bank_accounts WHERE account_number = %s), '
                   'amount AS (SELECT %s)'
                   'UPDATE bank_accounts '
                   'SET balance = (CASE WHEN account_number IN (SELECT account_number FROM first_account) '
                   'THEN balance - (SELECT * FROM amount) '
                   'WHEN account_number IN (SELECT account_number FROM second_account) '
                   'THEN balance + (SELECT * FROM amount) END) '
                   'WHERE account_number IN (SELECT account_number FROM first_account UNION '
                   'SELECT account_number FROM second_account)', (from_account, to_account, int(amount)))

    cursor.execute('SELECT COUNT(*) '
                   'FROM bank_accounts '
                   'WHERE account_number = %s '
                   'OR account_number = %s ', (from_account, to_account))
    count = cursor.fetchone()[0]
    if count < 2:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Один или оба счета введены неверно. Пожалуйста, проверьте правильность ввода и повторите перевод',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False
    conn.commit()
    progress_bar()  # функция полоски загрузки
    print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
          f'Со счета №{from_account} переведена сумма {amount} на счет №{to_account}',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)


# Открываем новый счет (команда №5)
def create_account(bank_user_id):
    new_balance = 0
    new_description = 'Мой новый счет'
    cursor.execute('WITH new_num AS '
                   '(SELECT MAX(account_number) + 1 AS new_acc_num '
                   'FROM bank_accounts) '
                   'INSERT INTO bank_accounts (user_id, account_number, balance, description) '
                   'SELECT id, new_acc_num,  %s, %s'
                   'FROM bank_users, new_num '
                   'WHERE bank_users.id = %s', (new_balance, new_description, bank_user_id,))
    progress_bar()  # функция полоски загрузки
    print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
          f'Поздравляем! Вы только что открыли новый счет в нашем Банке!',
          f'Посмотреть обновленный список счетов Вы можете, нажав клавишу №1 в главном меню',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)
    conn.commit()


# Закрываем счета - soft-delete (команда №6)
def delete_account(bank_user_id):
    del_account = input('Введите номер счета: ')
    if not del_account:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Номер счета должен быть заполнен!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if not del_account.isdigit():
        print(f'{Fore.LIGHTYELLOW_EX}----------------------------------',
              f'Я вас не поняла, попробуйте вводить только цифры!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return

    cursor.execute('SELECT * FROM bank_accounts '
                   'WHERE account_number = %s '
                   'AND user_id = %s '
                   'AND is_deleted != True', (del_account, bank_user_id))
    account = cursor.fetchone()

    question = input(f'Вы уверены, что хотите закрыть счет №{del_account}? ')
    answer = ['Yes', 'yes', 'YES', 'Да', 'да', 'ДА']
    for i in answer:
        if i == question:
            if account:
                if account[2] == 0:
                    cursor.execute('UPDATE bank_accounts '
                                   'SET is_deleted = True '
                                   'WHERE account_number = %s ', (del_account,))
                    progress_bar()  # функция полоски загрузки
                    print(f'----------------------------------',
                          f'Ваш счет №{del_account} закрыт',
                          f'----------------------------------', sep='\n')
                elif account[2] >= 0:
                    print(f'{Fore.LIGHTRED_EX}--------------------------------',
                          f'На счете есть деньги! Для закрытия счета его баланс должен быть равен 0.',
                          f'Для обнуления счета Вы можете воспользоваться одной из команд Главного меню',
                          f'----------------------------------', sep='\n')
                    print(Style.RESET_ALL)
                conn.commit()
                return
            print(f'{Fore.LIGHTRED_EX}----------------------------------',
                  f'Счет не найден! Пожалуйста, проверьте правильность ввода номера счета',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
            return
    print(f'{Fore.LIGHTRED_EX}----------------------------------',
          'Операция прервана!',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)


# Кастомное описание счета пользователя (команда №7)
def update_description(bank_user_id):
    acc_disc_update = input('Введите номер счета для изменения его описания: ')
    new_description = input('Введите новое описание счета (максимум 30 символов): ')
    if not acc_disc_update:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Номер счета должен быть заполнен!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if not acc_disc_update.isdigit():
        print(f'{Fore.LIGHTYELLOW_EX}----------------------------------',
              f'Я вас не поняла, попробуйте вводить только цифры!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return
    if len(new_description) > 30:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'Описание не должно превышать 30 символов!',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False
    cursor.execute('SELECT * FROM bank_accounts '
                   'WHERE account_number = %s '
                   'AND user_id = %s '
                   'AND is_deleted != True', (acc_disc_update, bank_user_id))
    account = cursor.fetchone()
    if not account:
        print(f'{Fore.LIGHTRED_EX}----------------------------------',
              f'У вас нет такого счета! Пожалуйста, проверьте правильность ввода номера счета...',
              f'----------------------------------', sep='\n')
        print(Style.RESET_ALL)
        return False
    cursor.execute('UPDATE bank_accounts '
                   'SET description = %s '
                   'WHERE account_number = %s', (new_description, acc_disc_update))
    progress_bar()  # функция полоски загрузки
    print(f'{Fore.LIGHTGREEN_EX}----------------------------------',
          f'Новое описание применено применено для счета №{acc_disc_update}',
          f'----------------------------------', sep='\n')
    print(Style.RESET_ALL)
    conn.commit()
