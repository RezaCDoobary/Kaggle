import sqlite3 as sql

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sql.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn

class table:
    def __init__(self, table_name):
        self.statement = """ CREATE TABLE IF NOT EXISTS """+ table_name +""" ( """
        self.end = """); """
        
    def add_column(self, column_name, column_type, is_primary = False, is_foreign = None , is_done = False):
        assert(is_primary == True and is_foreign == None) \
        or (is_primary == False and is_foreign != None)\
        or (is_primary == False and is_foreign == None),\
        'The same column cannot be a foreign key and a primary at the same time'
        
        if is_primary:
            self.statement += column_name + """ """ +column_type + """ PRIMARY KEY, """
            
        elif is_foreign:
            table = is_foreign
            self.statement += column_name + """ """ +column_type + """ REFERENCES """ + table + """, """
        else:
            self.statement += column_name + """ """ +column_type + """, """


            
        if is_done:
            self.statement = self.statement[:-2] + self.end
            
    def get_statement(self):
        return self.statement

    def commit(self, connection):
        print("committing : ")
        print(self.statement)
        try:
            c = connection.cursor()
            c.execute(self.statement)
            c.close()
        except Error as e:
            print(e)
            
class insert:
    def __init__(self, table):
        self.table = table
        self.statement = """INSERT INTO """+self.table+"""("""

    def insert_into_table(self , values, columns_array):
        self.values = values
        question_marks = ''
        for cols in columns_array:
            question_marks+='?,'
            self.statement+=cols
            self.statement+=','
        self.statement = self.statement[:-1] + """) VALUES(""" + question_marks[:-1] + """)"""
        
    def commit_one(self, connection):
        try:
            c = connection.cursor()
            c.execute(self.statement, self.values)
            return c
        except Error as e:
            print(e)
            
    def commit_many(self, connection):
        try:
            c = connection.cursor()
            c.executemany(self.statement, self.values)
        except Error as e:
            print(e)
            
def drop_table(table, conn):
    c = conn.cursor()
    dropTableStatement = "DROP TABLE IF EXISTS "+table

    c.execute(dropTableStatement)
    c.close()
    
def select(column_array, table, conn):
    select = """SELECT """
    for c in column_array:
        select += c+','
    select = select[:-1]

    select += """ FROM """ + table +";"
    c = conn.cursor()
    c.execute(select)
    return c