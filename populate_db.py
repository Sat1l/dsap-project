import psycopg2
import random

DB_NAME = "keebs"
DB_USER = "postgres"
DB_PASSWORD = "sat"
DB_HOST = "localhost"
DB_PORT = "5432"

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

adjectives = [
    "happy", "bright", "quick", "silly", "calm",
    "brave", "proud", "eager", "kind", "clever",
    "gentle", "lively", "nice", "polite", "quiet",
    "shy", "smart", "sweet", "tall", "warm"
]

nouns = [
    "tiger", "mountain", "river", "eagle", "tree",
    "lion", "ocean", "star", "flower", "forest",
    "desert", "laptop", "bunny", "dog", "cloud",
    "moon", "sun", "bird", "book", "cake"
]

gamer_words = [
    "Apex",
    "Nexus",
    "Valor",
    "Rift",
    "Havoc",
    "Zenith",
    "Vortex",
    "Titan",
    "Echo",
    "Blitz",
    "Phantom",
    "Striker",
    "Surge",
    "Quantum",
    "Havoc"
]

gamer_adjectives = [
    "Fierce",
    "Epic",
    "Savage",
    "Legendary",
    "Dynamic",
    "Intrepid",
    "Valiant",
    "Fearless",
    "Relentless",
    "Supreme",
    "Invincible",
    "Agile",
    "Mighty",
    "Resilient",
    "Thunderous"
]



def create_manufacturers():
    companies = []
    for i in range(150):
        company_name = random.choice(adjectives) + " " + random.choice(nouns)
        companies.append((company_name, 
                          "https://www." + company_name.replace(" ", "-") + ".com",
                          random.randint(1900, 2021), 
                          random.choice(["USA", "China", "Germany", "Japan", "South Korea"])))
    return companies

def create_keyboards():
    keyboards = []
    for i in range(200):
        key_amount = random.randint(1, 150)
        keyboard_name = random.choice(gamer_words) + " " + random.choice(gamer_adjectives) + " " + str(key_amount)
        keyboards.append((keyboard_name, 
                          str(key_amount),
                          str(random.randint(1, 7)), 
                          str(random.randint(1, 3)),
                          str(random.choice([True, False])),
                          str(random.randint(1, 150))))
    return keyboards



def populate_tables():
    conn = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    cursor = conn.cursor()

    key_arrangement_data = [
        ("ANSI",),
        ("ISO",),
        ("ERGO",),
        ("JIS",),
        ("HHKB",),
        ("STAGGERED",),
        ("ORTHOLINEAR",)
    ]

    cursor.executemany(
        "INSERT INTO key_arrangement (name_of_arrangement) VALUES (%s)",
        key_arrangement_data
    )

    case_formfactor_data = [
        ("UNIBODY",),
        ("SPLIT",),
        ("MONOSPLIT",)
        ]

    cursor.executemany(
        "INSERT INTO case_formfactor (name_of_formfactor) VALUES (%s)",
        case_formfactor_data
    )

    manufacturer_data = create_manufacturers()

    cursor.executemany(
        """INSERT INTO manufacturer (manufacturer_name, website, creation_year, country)
        VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING""",
        manufacturer_data
    )


    keyboard_data = create_keyboards()

    for keyboard in keyboard_data:
        try:
            cursor.execute(
                    """INSERT INTO keyboard (keyboard_name, key_amount, key_arrangement_id, case_formfactor_id, is_open_source, manufacturer_id)"""
                    """VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                    keyboard
                )
        except psycopg2.Error as e:
            if e.pgcode == "23503":
                continue
    cursor.close()
    conn.close()

if __name__ == "__main__":
    populate_tables()
    print("Tables populated successfully!")
