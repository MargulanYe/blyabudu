import psycopg2
import csv
import os
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()

# Соединение с PostgreSQL
def connect_db():
    try:
        db_url = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Создание таблицы (если не существует)
def create_table():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS phonebook (
            username TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            phone TEXT
        );''')
        conn.commit()
        cur.close()
        conn.close()

# Функция для сброса таблицы (удаления и пересоздания)
def reset_table():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS phonebook")
        conn.commit()
        print("Table 'phonebook' dropped successfully.")
        # Пересоздаём таблицу
        create_table()
        print("Table 'phonebook' created successfully.")
        cur.close()
        conn.close()

# Вставка данных из CSV
def insert_from_csv(file_path):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Пропуск заголовка
                for row in csv_reader:
                    username, first_name, last_name, phone = row
                    cur.execute("INSERT INTO phonebook (username, first_name, last_name, phone) VALUES (%s, %s, %s, %s)",
                                (username, first_name, last_name, phone))
                conn.commit()
                print(f"Data from {file_path} inserted successfully.")
        except Exception as e:
            print(f"Error reading the CSV file: {e}")
        cur.close()
        conn.close()

# Вставка данных из консоли
def insert_from_console():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        username = input("Enter username: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        phone = input("Enter phone number: ")
        cur.execute("INSERT INTO phonebook (username, first_name, last_name, phone) VALUES (%s, %s, %s, %s)",
                    (username, first_name, last_name, phone))
        conn.commit()
        print(f"Data for {username} inserted successfully.")
        cur.close()
        conn.close()

# Обновление данных
def update_data():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        username = input("Enter the username to update: ")
        print("Update options: 1. First Name  2. Last Name  3. Phone Number")
        option = input("Enter the option number you want to update: ")
        
        if option == "1":
            new_first_name = input("Enter new first name: ")
            cur.execute("UPDATE phonebook SET first_name = %s WHERE username = %s", (new_first_name, username))
        elif option == "2":
            new_last_name = input("Enter new last name: ")
            cur.execute("UPDATE phonebook SET last_name = %s WHERE username = %s", (new_last_name, username))
        elif option == "3":
            new_phone = input("Enter new phone number: ")
            cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, username))
        else:
            print("Invalid option.")
            return
        
        conn.commit()
        print(f"Data for {username} updated successfully.")
        cur.close()
        conn.close()

# Запрос данных
def query_data():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        filter_type = input("Enter filter type (all/username/phone): ")
        
        if filter_type == "all":
            cur.execute("SELECT * FROM phonebook")
        elif filter_type == "username":
            username = input("Enter username: ")
            cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))
        elif filter_type == "phone":
            phone = input("Enter phone number: ")
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
        else:
            print("Invalid filter type.")
            return
        
        rows = cur.fetchall()
        for row in rows:
            print(f"Username: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Phone: {row[3]}")
        
        cur.close()
        conn.close()

# Удаление данных
def delete_data():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        username = input("Enter the username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))
        conn.commit()
        print(f"Data for {username} deleted successfully.")
        cur.close()
        conn.close()

# Главное меню
def main():
    create_table()  # Создание таблицы

    while True:
        print("PhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Data")
        print("4. Query Data")
        print("5. Delete Data")
        print("6. Reset Table (Drop and Recreate)")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            continue

        if choice == 1:
            file_path = input("Enter the CSV file path: ")
            insert_from_csv(file_path)
        elif choice == 2:
            insert_from_console()
        elif choice == 3:
            update_data()
        elif choice == 4:
            query_data()
        elif choice == 5:
            delete_data()
        elif choice == 6:
            reset_table()  # Сброс таблицы
        elif choice == 7:
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
