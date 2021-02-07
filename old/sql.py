import datetime
import sqlite3

def init_sqlite():
    conn = sqlite3.connect(dbfolder + dbname)
    c = conn.cursor()
    c.execute('''CREATE TABLE data (date date, )''')

def sqlite_connect():
    global conn
    conn = sqlite3.connect(dbfolder + dbname, check_same_thread=False)

def sqlite_load_all():
    sqlite_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM data ORDER BY date DESC LIMIT 1')
    rows = c.fetchall()
    conn.close()
    return rows

def sanford_load():
    global comments_me_count
    global comments_processed_count
    global goodbot_count
    global badbot_count
    global deleted_count
    global sanford_dict
    if bool(sanford_dict):
        sanford_dict.clear()
    for row in sqlite_load_all():
        sanford_dict=(row[0],row[1], row[2], row[3], row[4],row[5])
    comments_me_count = sanford_dict[1]
    comments_processed_count = sanford_dict[2]
    goodbot_count = sanford_dict[3]
    badbot_count = sanford_dict[4]
    deleted_count = sanford_dict[5]


def sqlite_write(comments_made,comments_read,good,bad,deleted):
    sqlite_connect()
    c = conn.cursor()
    x = datetime.datetime.now()
    q = [(x), (comments_made), (comments_read), (good), (bad), (deleted)]
    c.execute('''INSERT INTO stats('date') VALUES(?)''', q)
    conn.commit()
    conn.close()

try:
    init_sqlite()
except sqlite3.OperationalError:
    pass
