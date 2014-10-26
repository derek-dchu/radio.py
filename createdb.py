__author__ = 'DerekHu'

import sqlite3


class CreateDB:
    def __init__(self, db='radio.db'):
        self.db = db

    def __drop_table(self, table_name):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS \'{}\'".format(table_name))

        conn.commit()
        conn.close()

    def __create_table(self, table_name, table_fields):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        c.execute("CREATE TABLE \'{0}\'({1})".format(table_name, table_fields))

        conn.commit()
        conn.close()

    def create_user_table(self):
        self.__drop_table('user')
        self.__create_table('user', '''
                  'id' INTEGER,
                  'name' VARCHAR ,
                  'created_at' TIME DEFAULT CURRENT_TIME NOT NULL,
                  'favourite_station_list_id' INTEGER,
                  'favourite_category_list_id' INTEGER,
                  PRIMARY KEY (id)
                  '''
        )

    def create_favourite_station_table(self):
        self.__create_table('favourite_station', '''
                'id' INTEGER,
                'user_id' INTEGER,
                'sid' INTEGER
                '''
    )

    def create_favourite_category_table(self):
        self.__create_table('favourite_category', '''
                'id' INTEGER,
                'user_id' INTEGER,
                'cid' INTEGER
                '''
    )


if __name__ == '__main__':
    create_db = CreateDB()
    create_db.create_user_table()
    create_db.create_favourite_category_table()
    create_db.create_favourite_station_table()