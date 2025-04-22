import psycopg2

# Подключение к базе данных
def get_connection():
    return psycopg2.connect(
        dbname="neondb",
        user="neondb_owner",
        password="npg_rvHlTaj8n5wF",
        host="ep-cool-credit-a5lc7eqy-pooler.us-east-2.aws.neon.tech",
        port="5432"
    )

# Функция для получения записей по шаблону
def get_record(pattern):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT first_name, last_name, phone_number 
                    FROM phonebookplus  -- Используется правильное имя таблицы
                    WHERE first_name LIKE %s OR last_name LIKE %s OR phone_number LIKE %s
                """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
                result = cur.fetchall()
                return result
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при получении данных:", error)

# Функция для вставки или обновления записи
def upsert(first_name, last_name, phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Используем запрос на вставку или обновление данных в таблице
                cur.execute("""
                    INSERT INTO phonebookplus (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone_number)
                    DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name
                """, (first_name, last_name, phone_number))
        print("Успешно добавлено или обновлено!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при вставке данных:", error)

# Функция для удаления записи по имени и фамилии
def delete_by_name(first_name, last_name):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebookplus WHERE first_name = %s AND last_name = %s", (first_name, last_name))
                print("Успешно удалено!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при удалении данных:", error)

# Функция для удаления записи по номеру телефона
def delete_by_phone(phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebookplus WHERE phone_number = %s", (phone_number,))
                print("Успешно удалено!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при удалении данных:", error)

# Основная часть программы
if __name__ == "__main__":
    choose_box = '''
    1. Вставка данных
    2. Поиск данных
    3. Удаление данных
    '''
    print(choose_box)
    n = int(input("Введите номер запроса: "))
    if n == 1:
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        phone_number = input("Введите номер телефона: ")
        upsert(first_name, last_name, phone_number)
    elif n == 2:
        pattern = input("Введите шаблон для поиска: ")
        records = get_record(pattern)
        for record in records:
            print(record)
    elif n == 3:
        choose_box_del = '''
        1. Удалить по имени и фамилии
        2. Удалить по номеру телефона
        '''
        print(choose_box_del)
        
        q = int(input("Введите номер запроса: "))
        
        if q == 1:
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            delete_by_name(first_name, last_name)
        elif q == 2:
            phone_number = input("Введите номер телефона: ")
            delete_by_phone(phone_number)
    else:
        print("Неверный ввод!")
