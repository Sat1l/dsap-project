import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "sat"
DB_HOST = "localhost"
DB_PORT = "5432"

# Establish a connection to PostgreSQL
def create_connection(dbname, user, password, host, port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    return conn

# Create the keebs database
def create_database():
    conn = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS keebs")
    cursor.execute("CREATE DATABASE keebs")
    cursor.close()
    conn.close()

# Create tables within the keebs database
def create_tables():
    conn = create_connection("keebs", DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = conn.cursor()

    create_table_queries = [
        """
        CREATE TABLE key_arrangement (
            key_arrangement_id SERIAL PRIMARY KEY,
            name_of_arrangement VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE case_formfactor (
            case_formfactor_id SERIAL PRIMARY KEY,
            name_of_formfactor VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE manufacturer (
            manufacturer_id SERIAL PRIMARY KEY,
            manufacturer_name VARCHAR(255) NOT NULL UNIQUE,
            website VARCHAR(255),
            creation_year INT NOT NULL,
            country VARCHAR(255)
        )
        """,
        """
        CREATE TABLE keyboard (
            keyboard_id SERIAL PRIMARY KEY,
            keyboard_name VARCHAR(255) NOT NULL UNIQUE,
            key_amount INT NOT NULL,
            key_arrangement_id INT,
            case_formfactor_id INT,
            is_open_source BOOL,
            manufacturer_id INT,
            FOREIGN KEY (key_arrangement_id) REFERENCES key_arrangement (key_arrangement_id),
            FOREIGN KEY (case_formfactor_id) REFERENCES case_formfactor (case_formfactor_id),
            FOREIGN KEY (manufacturer_id) REFERENCES manufacturer (manufacturer_id)
        )
        """
    ]

    for query in create_table_queries:
        cursor.execute(query)

    cursor.close()
    conn.close()

# Main function to create the database and tables
def main():
    create_database()
    create_tables()
    print("successfully created the keebs database and tables")

if __name__ == "__main__":
    main()

