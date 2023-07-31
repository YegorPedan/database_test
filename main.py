import sqlite3
import os


def is_database_exists(db_name: str) -> bool:
    return os.path.isfile(db_name)


def create_database(db_name: str) -> bool:
    status = True
    if is_database_exists(db_name):
        print(f"database {db_name} already exsists")
        status = False
    else:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Hotels (
                           id INTEGER PRIMARY KEY,
                           name TEXT NOT NULL,
                           description TEXT NOT NULL,
                           stars INTEGER NOT NULL,
                           minimal_price INTEGR NOT NULL
                           )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Rooms (
                           id INTEGER PRIMARY KEY,
                           hotel_id INTEGER NOT NULL,
                           count_of_person INTEGER NOT NULL,
                           price INTEGER NOT NULL,
                           FOREIGN KEY (hotel_id) REFERENCES Hotels (id)
                           )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Client (
                           id INTEGER PRIMARY KEY,
                           room_id INTEGER NOT NULL,
                           full_name TEXT NOT NULL,
                           phone_number VARCHAR(50),
                           date_start VARCHAR(30) NOT NULL,
                           date_end VARCHAR(30) NOT NULL,
                           FOREIGN KEY (room_id) REFERENCES Rooms (id)
                           )
                       """)

        connection.commit()
        connection.close()
        print(f"database {db_name} successfully created")
    return status


def insert_data(db_name):
    hotels_data = [
        (1, 'Hotel A', 'Luxury hotel', 5, 200),
        (2, 'Hotel B', 'Budget hotel', 3, 80),
    ]

    rooms_data = [
        (1, 1, 1, 150),
        (2, 1, 2, 200),
        (3, 1, 1, 90),
        (4, 2, 1, 1200),
        (5, 2, 1, 75),
        (6, 2, 1, 110),
    ]

    clients_data = [
        (1, 1, 'John Doe', '+123456781', '2023-08-01', '2023-08-05'),
        (2, 2, 'Jane Smith', '+987654322', '2023-09-10', '2023-09-15'),
        (3, 2, 'Ben Clark', '+987654323', '2023-09-10', '2023-09-15'),
        (4, 3, 'Vasa Petrov', '+987654324', '2023-01-10', '2023-09-15'),
        (5, 4, 'Nikita Ivanov', '+987654325', '2023-07-11', '2023-09-15'),
        (6, 5, 'Sasha Sidorva', '+987654326', '2023-10-10', '2023-10-15'),
        (7, 6, 'Denis Smirnov', '+987654327', '2023-08-07', '2023-09-15'),
    ]

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    try:
        cursor.executemany("""
                           INSERT INTO Hotels (id, name, description, stars, minimal_price)
                           VALUES (?, ?, ?, ?, ?)
                           """, hotels_data)
    except sqlite3.IntegrityError:
        print("Hotels already inserted")

    try:
        cursor.executemany("""
                           INSERT INTO Rooms (id, hotel_id, count_of_person, price)
                           VALUES (?, ?, ?, ?)
                           """, rooms_data)
    except sqlite3.IntegrityError:
        print("rooms already inserted")

    try:
        cursor.executemany("""
                           INSERT INTO Client (id, room_id, full_name, phone_number, date_start, date_end)
                           VALUES (?, ?, ?, ?, ?, ?)
                           """, clients_data)
    except sqlite3.IntegrityError:
        print("Clients already inserted")

    connection.commit()
    connection.close()


def get_cheapest_room(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    result = cursor.execute("""SELECT Hotels.name, Rooms.price
    FROM Hotels INNER JOIN Rooms
    ON Hotels.id = Rooms.hotel_id
    ORDER BY Rooms.price LIMIT 1""").fetchone()
    print(f"The cheapest room costs {result[1]} and its cost is {result[1]}$")
    connection.close()


def sort_hotels(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    result = cursor.execute("""
    SELECT Hotels.name FROM Hotels
    ORDER BY minimal_price DESC
                            """).fetchall()
    print("Sorted hotels list by minimal_price")
    for hotel in result:
        print(hotel[0])
    connection.close()


def sort_client_by_price(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    result = cursor.execute("""
    SELECT Hotels.name, Client.full_name, Client.phone_number, Client.date_start, Client.date_end
    FROM Client JOIN Rooms ON Client.room_id = Rooms.id
    JOIN Hotels ON Rooms.hotel_id = Hotels.id
     ORDER BY Rooms.price ASC
                            """).fetchall()
    for client in result:
        print(client)
    print(result)
    connection.close()


def get_hotel_first_client(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    result = cursor.execute("""
    SELECT Hotels.name, Client.full_name, MIN(date_start)
    FROM Client JOIN Rooms
    ON Client.room_id = Rooms.id
    JOIN Hotels ON Rooms.hotel_id = Hotels.id
    GROUP BY Hotels.name
                   """).fetchall()
    print(result)
    connection.close()


def get_richest_phone_number(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    result = cursor.execute("""
    SELECT Hotels.name, Client.phone_number
    FROM Client
    JOIN Rooms r1 ON r1.id = Client.room_id
    JOIN Hotels ON Hotels.id = r1.hotel_id
    WHERE r1.price = (
    SELECT MAX(price)
    FROM Rooms r2
    WHERE r1.hotel_id = r2.hotel_id
        )
    GROUP BY Hotels.name
                            """).fetchall()
    print(result)
    connection.close()


def delete_database(db_name: str):
    os.remove(db_name)


if __name__ == "__main__":
    create_database("Services")
    insert_data("Services")
    print()
    get_cheapest_room("Services")
    print()
    sort_hotels("Services")
    print()
    sort_client_by_price("Services")
    print()
    get_hotel_first_client("Services")
    print()
    get_richest_phone_number("Services")
