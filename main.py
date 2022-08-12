import psycopg2


def del_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            DROP TABLE IF EXISTS phone;
            DROP TABLE IF EXISTS client;
        ''')

        conn.commit()


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) NOT NULL UNIQUE 
            );
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS phone (
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES client(id),
                phone_number VARCHAR(15) 
            );
        ''')

        conn.commit()


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO client (first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id;
        ''', (first_name, last_name, email))

        client_id = cur.fetchone()

        cur.execute('''
            INSERT INTO phone (client_id, phone_number)
            VALUES (%s, %s);
        ''', (client_id, phone))

        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO phone (client_id, phone_number)
            VALUES (%s, %s);
        ''', (client_id, phone))

        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client
            SET first_name = %s WHERE id = %s;
            """, (first_name, client_id))

        cur.execute("""
            UPDATE client
            SET last_name = %s WHERE id = %s;
            """, (last_name, client_id))

        cur.execute("""
            UPDATE client
            SET email = %s WHERE id = %s;
            """, (email, client_id))

        cur.execute("""
             UPDATE phone
             SET phone_number = %s WHERE client_id = %s;
             """, (phone_number, client_id))

        conn.commit()


def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phone 
            WHERE client_id = %s 
            AND phone_number = %s;
        ''', (client_id, phone_number))

        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phone
            WHERE client_id = %s;     
        ''', (client_id,))

        cur.execute('''
            DELETE FROM client
            WHERE id = %s;     
        ''', (client_id,))

        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT client.id, client.first_name, client.last_name, 
            client.email, phone.phone_number FROM client
            JOIN phone ON client.id = phone.client_id
            WHERE client.first_name = %s OR client.last_name = %s 
            OR client.email = %s OR phone.phone_number = %s;
        ''', (first_name, last_name, email, phone))

        print(cur.fetchone())


with psycopg2.connect(database="my_db", user="postgres", password="python123") as conn:
    del_db(conn)
    create_db(conn)
    add_client(conn, 'Anatoly', 'Pakhomov', 'python@mail.ru', '89139135555')
    add_client(conn, 'Oleg', 'Buligin', 'marvel_lover@mail.ru', '89137777799')
    add_phone(conn, 1, '89134567899')
    add_phone(conn, 2, '89134567894')
    add_phone(conn, 2, '89134567898')
    find_client(conn, last_name='Pakhomov')
    find_client(conn, 'Oleg')
    change_client(conn, 1, 'Vin', 'Diesel', 'cr7@mail.ru', '89134567893')
    find_client(conn, phone='89134567893')
    delete_phone(conn, 2, phone_number='89134567894')
    delete_client(conn, 1)
    find_client(conn, email='marvel_lover@mail.ru')

conn.close()



