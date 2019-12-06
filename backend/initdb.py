import sqlite3
import time
import random
if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("delete from records_curr;")
    conn.commit()