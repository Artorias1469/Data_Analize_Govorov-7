#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import psycopg2
import typing as t

def create_db() -> None:
    """
    Создать базу данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id SERIAL PRIMARY KEY,
            destination TEXT NOT NULL,
            flight_number TEXT NOT NULL,
            aircraft_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_flight(destination: str, flight_number: str, aircraft_type: str) -> None:
    """
    Добавить данные о рейсе в базу данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (destination, flight_number, aircraft_type)
        VALUES (%s, %s, %s)
    ''', (destination, flight_number, aircraft_type))
    conn.commit()
    conn.close()

def print_flights() -> None:
    """
    Отобразить список рейсов.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM flights
    ''')
    flights = cursor.fetchall()
    conn.close()

    if flights:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print('| {:^30} | {:^20} | {:^15} |'.format(
            "Название пункта назначения",
            "Номер рейса",
            "Тип самолета"
        ))
        print(line)

        for flight in flights:
            print('| {:<30} | {:<20} | {:<15} |'.format(
                flight[1], flight[2], flight[3]
            ))

        print(line)
    else:
        print("Список рейсов пуст.")

def search_flights_by_aircraft_type(search_aircraft_type: str) -> None:
    """
    Выбрать рейсы по типу самолета из базы данных PostgreSQL.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM flights WHERE aircraft_type = %s
    ''', (search_aircraft_type,))
    matching_flights = cursor.fetchall()
    conn.close()

    if matching_flights:
        print("\nРейсы, обслуживаемые самолетом типа {}: ".format(search_aircraft_type))
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print('| {:^30} | {:^20} | {:^15} |'.format(
            "Название пункта назначения",
            "Номер рейса",
            "Тип самолета"
        ))
        print(line)

        for flight in matching_flights:
            print('| {:<30} | {:<20} | {:<15} |'.format(
                flight[1], flight[2], flight[3]
            ))

        print(line)
    else:
        print(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")

def main():
    parser = argparse.ArgumentParser(description="Flight Information Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-p", "--print-flights", action="store_true", help="Print the list of flights")
    parser.add_argument("-s", "--search-by-type", help="Search flights by aircraft type")
    args = parser.parse_args()

    create_db()

    if args.add_flight:
        destination = input("Введите название пункта назначения: ")
        flight_number = input("Введите номер рейса: ")
        aircraft_type = input("Введите тип самолета: ")
        add_flight(destination, flight_number, aircraft_type)

    elif args.print_flights:
        print_flights()

    elif args.search_by_type:
        search_flights_by_aircraft_type(args.search_by_type)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
