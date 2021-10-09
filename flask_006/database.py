import psycopg2


class Table:
    name = 'table_name'
    values = '(table_values)'

    def __str__(self):
        return self.name


class Users(Table):
    name = 'users'
    values = "(default, %s, %s, %s)"


def db_decorator(func):
    def wrapper(self, *args, **kwargs):
        self.connect()
        temp = func(self, *args, **kwargs)
        self.disconnect()
        return temp
    return wrapper


class FlaskDataBase:
    def __init__(self, db_name, user, password):
        self.db_name = db_name
        self.user = user
        self.password = password

        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect("dbname={0} user={1} password={2}".format(self.db_name, self.user, self.password))
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_db(self):
        """ Не работает """
        with open('db_schema.sql', mode='r') as sql_file:
            self.cur.exeсute(sql_file.read())

    @db_decorator
    def insert_one(self, table: Table, obj):
        self.cur.execute(
            "INSERT INTO {0} VALUES {1}".format(table.name, table.values), (obj.get_values())
        )

    @db_decorator
    def insert_many(self, table: Table, objs):
        args_str = ','.join(self.cur.mogrify("{0}".format(table.values), (obj.email, obj.password, obj.created_at)) for obj in objs)
        self.cur.execute("INSERT INTO {0} VALUES ".format(table.name) + args_str)

    @db_decorator
    def get_one(self, table, **kwargs):
        args_str = ' and '.join("{0} = '{1}'".format(key, value) for key, value in kwargs.items() if value is not None)

        self.cur.execute(
            "SELECT * from {0} where ".format(table.name) + args_str)
        return self.cur.fetchone()

    @db_decorator
    def get_all(self, table):
        self.cur.execute(
            "SELECT * from {0}".format(table.name))
        return self.cur.fetchall()
