import psycopg2


def del_db(cur):
    cur.execute('''
        DROP TABLE IF EXISTS phone;
        DROP TABLE IF EXISTS client;
    ''')


def create_db(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS client (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(60),
            last_name VARCHAR(60),
            email VARCHAR(60) UNIQUE 
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS phone (
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            phone_number VARCHAR(15) 
        );
    ''')


def add_client(cur, first_name, last_name, email, phone=None):
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


def add_phone(cur, client_id, phone):
    cur.execute('''
        INSERT INTO phone (client_id, phone_number)
        VALUES (%s, %s);
    ''', (client_id, phone))


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    if first_name:
        cur.execute("""
            UPDATE client
            SET first_name = %s
            WHERE id = %s;
            """, (first_name, client_id))
    elif last_name:
        cur.execute("""
            UPDATE client
            SET last_name = %s
            WHERE id = %s;
            """, (last_name, client_id))
    elif email:
        cur.execute("""
            UPDATE client
            SET email = %s
            WHERE id = %s;
            """, (email, client_id))

    elif phone_number:
        cur.execute("""
             UPDATE phone
             SET phone_number = %s WHERE client_id = %s;
             """, (phone_number, client_id))


def delete_phone(cur, client_id, phone_number):
    cur.execute('''
        DELETE FROM phone 
        WHERE client_id = %s 
        AND phone_number = %s;
    ''', (client_id, phone_number))


def delete_client(cur, client_id):
    cur.execute('''
        DELETE FROM phone
        WHERE client_id = %s;     
    ''', (client_id,))

    cur.execute('''
        DELETE FROM client
        WHERE id = %s;     
    ''', (client_id,))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
        SELECT client.id, client.first_name, client.last_name, 
        client.email, phone.phone_number FROM client
        JOIN phone ON client.id = phone.client_id
        WHERE client.first_name = %s OR client.last_name = %s 
        OR client.email = %s OR phone.phone_number = %s;
    ''', (first_name, last_name, email, phone))

    print(cur.fetchone())


if __name__ == '__main__':
    with psycopg2.connect(database="my_db", user="postgres", password="python123") as conn:
        with conn.cursor() as cur:
            del_db(cur)
            create_db(cur)
            add_client(cur, 'Anatoly', 'Pakhomov', 'python@mail.ru', '89139135555')
            add_client(cur, 'Oleg', 'Buligin', 'marvel_lover@mail.ru', '89137777799')
            add_phone(cur, 1, '89134567899')
            add_phone(cur, 2, '89134567894')
            add_phone(cur, 2, '89134567898')
            find_client(cur, last_name='Pakhomov')
            find_client(cur, 'Oleg')
            change_client(cur, 1, first_name='Mark')
            find_client(cur, first_name='Mark')
            delete_phone(cur, 2, phone_number='89134567894')
            delete_client(cur, 1)
            find_client(cur, email='marvel_lover@mail.ru')

    conn.close()



