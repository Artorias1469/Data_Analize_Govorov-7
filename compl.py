#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import psycopg2
import typing as t

def create_db() -> None:
    """
    Создать базу данных.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="pwsi6tg3",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    # Создать таблицу с информацией о рейсах.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flights (
            flight_id SERIAL PRIMARY KEY,
            destination TEXT NOT NULL,
            flight_number TEXT NOT NULL,
            aircraft_type TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def add_flight(destination: str, flight_number: str, aircraft_type: str) -> None:
    """
    Добавить информацию о рейсе в базу данных.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="pwsi6tg3",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO flights (destination, flight_number, aircraft_type) VALUES (%s, %s, %s)
        """,
        (destination, flight_number, aircraft_type),
    )
    conn.commit()
    conn.close()

def print_flights() -> None:
    """
    Вывести список всех рейсов из базы данных.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="pwsi6tg3",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM flights
        """
    )
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nСписок всех рейсов:")
        for row in rows:
            print("Название пункта назначения:", row[1])
            print("Номер рейса:", row[2])
            print("Тип самолета:", row[3])
            print("--------------------------")
    else:
        print("\nСписок рейсов пуст.")

def main():
    parser = argparse.ArgumentParser(description="Flight Information Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-p", "--print-flights", action="store_true", help="Print the list of flights")
    parser.add_argument("destination", nargs='?', help="Destination of the flight")
    parser.add_argument("flight_number", nargs='?', help="Flight number")
    parser.add_argument("aircraft_type", nargs='?', help="Type of the aircraft")
    args = parser.parse_args()

    create_db()

    if args.add_flight:
        if not all([args.destination, args.flight_number, args.aircraft_type]):
            print("Необходимо указать название пункта назначения, номер рейса и тип самолета.")
        else:
            add_flight(args.destination, args.flight_number, args.aircraft_type)
            print("Информация о рейсе успешно добавлена в базу данных.")

    elif args.print_flights:
        print_flights()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
