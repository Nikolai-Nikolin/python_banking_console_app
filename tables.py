import psycopg2

conn = psycopg2.connect(dbname="postgres",
                        user="postgres",
                        password="postgres",
                        host="localhost",
                        port="5432")
print("Подключение установлено")
cursor = conn.cursor()

# СОЗДАЕМ ТАБЛИЦУ С ПОЛЬЗОВАТЕЛЯМИ
sqlUsers = ("CREATE TABLE IF NOT EXISTS bank_users "
            "(id SERIAL PRIMARY KEY, "
            "user_firstname VARCHAR, "
            "user_password VARCHAR NOT NULL)")
cursor.execute(sqlUsers)
conn.commit()
print("Таблица bank_users успешно создана")

# ДОБАВЛЯЕМ В НЕЕ ДАННЫЕ О ПОЛЬЗОВАТЕЛЯХ
bank_users = [('Nikolai', 'qwerty'),
              ('Andrei', 'qwerty1'),
              ('Alexander', 'qwerty2')]
cursor.executemany('INSERT INTO bank_users (user_firstname, user_password) VALUES (%s, %s)', bank_users)
conn.commit()
print("Данные добавлены")

# СОЗДАЕМ ТАБЛИЦУ СО СЧЕТАМИ
sqlAccounts = ('CREATE TABLE IF NOT EXISTS bank_accounts '
               '(account_id SERIAL PRIMARY KEY, '
               'account_number INTEGER NOT NULL UNIQUE, '
               'balance INTEGER DEFAULT 10000,'
               'description VARCHAR(30),'
               'is_deleted BOOL DEFAULT FALSE,'
               'user_id INTEGER,'
               'FOREIGN KEY (user_id) REFERENCES bank_users (id))')
cursor.execute(sqlAccounts)
conn.commit()
print('Таблица bank_accounts успешно создана')

# ДОБАВЛЯЕМ В НЕЕ ДАННЫЕ О СЧЕТАХ
bank_accounts = [(11111, 'Рублевый счет', 1),
                 (22222, 'Счет в долларах', 1),
                 (33333, 'Счет в сомони', 1),
                 (44444, 'Рублевый счет', 2),
                 (55555, 'Счет в долларах', 2),
                 (66666, 'Счет в сомони', 2),
                 (77777, 'Рублевый счет', 3),
                 (88888, 'Счет в долларах', 3),
                 (99999, 'Счет в сомони', 3)]
cursor.executemany('INSERT INTO bank_accounts (account_number, description, user_id) '
                   'VALUES (%s, %s, %s)', bank_accounts)
conn.commit()
print("Данные добавлены")
