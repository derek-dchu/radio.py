__author__ = 'DerekHu'


import sqlite3


## Load database file name
from createdb import db_file


class Model:
    def __init__(self, *arg, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    @staticmethod
    def __get_column_names(cursor):
        return tuple(map(lambda x:x[0], cursor.description))


    def save(self):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        ## Get column names
        c.execute('SELECT * FROM {};'.format(self.__class__.__name__))
        col_names = Model.__get_column_names(c)

        values = []
        for col_name in col_names:
            if hasattr(self, col_name):
                values.append(self.__dict__[col_name])
            else:
                values.append(None)

        try:
            c.execute('''INSERT OR REPLACE INTO {0} ({1}) VALUES ({2})'''.format(self.__class__.__name__, (','.join(col_names)), ','.join('?'*len(col_names))), values)
            return True
        except:
            return False
        finally:
            conn.commit()
            conn.close()


    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(*args, **kwargs)
        if obj.save() is True:
            return obj
        else:
            return None

    @classmethod
    def get(cls, **condition):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        if condition is {}:
            c.execute('SELECT * FROM {} LIMIT 1;'.format(cls.__name__))
        else:
            query_str = 'SELECT * FROM {} WHERE '.format(cls.__name__)
            for key in condition:
                if isinstance(condition[key], str):
                    query_str += '{} IS \'{}\' AND'.format(key, condition[key])
                else:
                    query_str += '{} IS {} AND'.format(key, condition[key])

            ## eliminate last 'AND'
            query_str = query_str[:-4]

            ## limit return row to 1
            query_str += ' LIMIT 1'
            c.execute(query_str)

        ## Get column names
        col_names = Model.__get_column_names(c)

        data = c.fetchone()
        conn.close()

        if data is None:
            return None
        else:
            obj = object.__new__(cls)
            for idx, col_name in enumerate(col_names):
                setattr(obj, col_name, data[idx])
            return obj

    @classmethod
    def delete(cls, **condition):
        if condition is {} or 'id' not in condition:
            print('Invalid input')
            return

        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        try:
            c.execute('''DELETE FROM {0} WHERE id IS (?)'''.format(cls.__name__), (condition['id'], ))
            return True
        except:
            return False
        finally:
            conn.commit()
            conn.close()


class User(Model):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return "username: {}, created at: {}".format(self.username, self.created_at)



if __name__ == '__main__':
    user = User.create(username='derek')
    user = User.get(username='derek')
    print(user)