from colorama import Fore, Back, Style
from bank_users_service import find_user, registration
from bank_accounts_service import (show_user_accounts,
                                   withdraw_money,
                                   deposit_money,
                                   create_account,
                                   delete_account,
                                   transfer_money,
                                   update_description)


def main_menu(bank_user_id):
    while True:
        print('\n\n=== Главное меню ===',
              '1. Показать список моих счетов',
              '2. Снять деньги со счета',
              '3. Внести деньги на свой счет',
              '4. Перевод денег на свой/чужой счет',
              '5. Открыть новый счет',
              '6. Закрыть счет',
              '7. Изменить описание счета',
              '0. Выход',
              sep='\n')
        comand = input('----- Пожалуйста, введите номер команды: ---> ')
        if comand == '0':
            print('===== Всего доброго, приходите еще! =====')
            enter_menu()
        elif comand == '1':
            show_user_accounts(bank_user_id)
        elif comand == '2':
            withdraw_money(bank_user_id)
        elif comand == '3':
            deposit_money(bank_user_id)
        elif comand == '4':
            transfer_money(bank_user_id)
        elif comand == '5':
            create_account(bank_user_id)
        elif comand == '6':
            delete_account(bank_user_id)
        elif comand == '7':
            update_description(bank_user_id)
        else:
            print(f'{Fore.RED}----------------------------------',
                  f'Вы ввели несуществующую команду!',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)


print("===== Добро пожаловать в наш Банк! =====")


def enter():
    while True:
        username = input("Введите ваш логин: ")
        password = input("Введите ваш пароль: ")

        found_user = find_user(username, password)
        if found_user is not None:
            print(f'Здравствуйте, {found_user[1]}!')
            some_bank_user_id = found_user[0]
            main_menu(some_bank_user_id)
        else:
            print(f'{Fore.RED}----------------------------------',
                  f'Пользователь не найден! Попробуйте ввести логин и пароль еще раз.....',
                  f'----------------------------------', sep='\n')
            print(Style.RESET_ALL)
            enter_menu()


def enter_menu():
    while True:
        print(f'===================',
              f'1. Регистрация',
              f'2. Вход',
              f'0. Выход',
              f'===================', sep='\n')
        cmd = input('----- Пожалуйста, введите номер команды: ---> ')
        if cmd == '0':
            print('===== Всего доброго, приходите еще! =====')
        elif cmd == '1':
            registration()
        elif cmd == '2':
            enter()


enter_menu()
