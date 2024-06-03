import argparse
import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "keebs"
DB_USER = "postgres"
DB_PASSWORD = "sat"
DB_HOST = "localhost"
DB_PORT = "5432"

# Establish a connection to PostgreSQL
def create_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn



def search_by_key_amount(n):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT keyboard_name FROM keyboard WHERE key_amount > %s"
        cursor.execute(query, (n,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [result[0] for result in results]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def search_by_country(country):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT keyboard.keyboard_name, manufacturer.manufacturer_name
    FROM keyboard
    JOIN manufacturer ON keyboard.manufacturer_id = manufacturer.manufacturer_id
    WHERE manufacturer.country = %s
    """
    cursor.execute(query, (country,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"название клавиатуры": result[0], "производитель": result[1]} for result in results]

def search_vintage(key_arrangement, creation_year):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT keyboard.keyboard_name, manufacturer.manufacturer_name
    FROM keyboard
    JOIN manufacturer ON keyboard.manufacturer_id = manufacturer.manufacturer_id
    JOIN key_arrangement ON keyboard.key_arrangement_id = key_arrangement.key_arrangement_id
    WHERE key_arrangement.name_of_arrangement = %s AND manufacturer.creation_year <= %s
    """
    cursor.execute(query, (key_arrangement, creation_year))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"название клавиатуры": result[0], "название производителя": result[1]} for result in results]


def search_by_case_formfactor(formfactor):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    SELECT keyboard.keyboard_name
    FROM keyboard
    JOIN case_formfactor ON keyboard.case_formfactor_id = case_formfactor.case_formfactor_id
    WHERE case_formfactor.name_of_formfactor = %s
    """
    cursor.execute(query, (formfactor,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [result[0] for result in results]

def search_open_source(isOpenSource):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keyboard_name FROM keyboard WHERE is_open_source = {}".format(isOpenSource))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [result[0] for result in results]

def main():
    parser = argparse.ArgumentParser(description="best keyboard search engine!!")
    subparsers = parser.add_subparsers(dest="command")

    parser_key_amount = subparsers.add_parser("search_key_amount")
    parser_key_amount.add_argument("n", type=int, help="Number of keys")

    parser_country = subparsers.add_parser("search_country")
    parser_country.add_argument("country", type=str, help="Manufacturer country. Available countries: China, Japan, Germany, South Korea, USA")

    parser_vintage = subparsers.add_parser("search_vintage")
    parser_vintage.add_argument("key_arrangement", type=str, help="Key layout. Available layouts: ANSI, ISO, ERGO, JIS, HHKB, STAGGERED, ORTHOLINEAR")
    parser_vintage.add_argument("creation_year", type=int, help="Creation year")

    parser_case_formfactor = subparsers.add_parser("search_case_formfactor")
    parser_case_formfactor.add_argument("formfactor", type=str, help="Case form factor. Available form factors: UNIBODY, SPLIT, MONOSPLIT")

    parser_open_source = subparsers.add_parser("search_open_source")
    parser_open_source.add_argument("isOpenSource", type=bool, help="Is open source? True or False")

    args = parser.parse_args()

    if args.command == "search_key_amount":
        results = search_by_key_amount(args.n)
        print("Keyboards with more than {} keys:".format(args.n))
        for result in results:
            print(result)

    elif args.command == "search_country":
        results = search_by_country(args.country)
        print("Keyboards from {}:".format(args.country))
        for result in results:
            print(result)

    elif args.command == "search_vintage":
        results = search_vintage(args.key_arrangement, args.creation_year)
        print("Vintage keyboards with arrangement {} and manufacturer creation year <= {}:".format(args.key_arrangement, args.creation_year))
        for result in results:
            print(result)

    elif args.command == "search_case_formfactor":
        results = search_by_case_formfactor(args.formfactor)
        print("Keyboards with case form factor {}:".format(args.formfactor))
        for result in results:
            print(result)

    elif args.command == "search_open_source":
        results = search_open_source(args.isOpenSource)
        print("Open source keyboards:")
        for result in results:
            print(result)

    elif args.command == "--help":
        parser.print_help()

    else:
        print("Invalid command")




if __name__ == "__main__":
    main()
