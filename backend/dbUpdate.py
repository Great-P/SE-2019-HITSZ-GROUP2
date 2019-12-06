import sqlite3
import time
import random
if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("delete from records_curr;")
    conn.commit()

    with open('main_records.sql',encoding='utf-8') as sql:
        for instruction in sql.readlines():
            c.execute(instruction.replace('INSERT INTO records', 'INSERT INTO records_curr'))
    conn.commit()
    counter = 0
    with open('records_after.sql',encoding='utf-8') as sql:
        iter_num = random.randint(10,20)
        for instruction in sql.readlines():
            c.execute(instruction.replace('INSERT INTO records', 'INSERT INTO records_curr'))
            counter = counter + 1
            if counter == iter_num:
                iter_num = random.randint(10,20)
                cur_date = str(instruction.split(',')[27].split("'"))
                print("progress: " + cur_date )
                conn.commit()
                time.sleep(2)
                counter = 0
    conn.commit()
