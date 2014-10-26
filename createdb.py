__author__ = 'DerekHu'

import sqlite3


db_file = 'radio.db'


class CreateDB:

    @staticmethod
    def __drop_table(table_name):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS \'{}\'".format(table_name))

        conn.commit()
        conn.close()

    @staticmethod
    def __create_table(table_name, table_fields):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute("CREATE TABLE \'{0}\'({1})".format(table_name, table_fields))

        conn.commit()
        conn.close()

    @staticmethod
    def create_user_table():
        CreateDB.__drop_table('user')
        CreateDB.__create_table('user', '''
                  'id' INTEGER,
                  'username' VARCHAR UNIQUE ,
                  'created_at' TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL,
                  PRIMARY KEY (id)
                  '''
        )

    @staticmethod
    def create_favourite_station_table():
        CreateDB.__drop_table('favourite_station')
        CreateDB.__create_table('favourite_station', '''
                'id' INTEGER,
                'user_id' INTEGER,
                'sid' INTEGER
                '''
    )

    @staticmethod
    def create_favourite_category_table():
        CreateDB.__drop_table('favourite_category')
        CreateDB.__create_table('favourite_category', '''
                'id' INTEGER,
                'user_id' INTEGER,
                'cid' INTEGER
                '''
    )


if __name__ == '__main__':
    CreateDB.create_user_table()
    CreateDB.create_favourite_category_table()
    CreateDB.create_favourite_station_table()