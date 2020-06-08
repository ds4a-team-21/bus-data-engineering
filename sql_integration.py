import sqlite3
import os

class SqlIntegration:

    @staticmethod
    def create_sqlite_table(dataframe, table_name):
        """Create or replace a SQL table in local file bus.db from a DataFrame pandas object"""

        if not os.path.exists('database'):
            os.mkdir('database')

        sqlite_connection = sqlite3.connect('database/bus.db')
        cursor = sqlite_connection.cursor()

        dataframe.to_sql(table_name, con=sqlite_connection, if_exists='replace', index=False)

        # Prints a confirmation that the table was created.
        cursor.execute('SELECT * FROM ' + table_name + ' LIMIT 5')
        record = cursor.fetchall()
        print(record)

    @staticmethod
    def update_sqlite_table(dataframe, table_name):
        """Creates or appends more data to a table in local file bus.db from a DataFrame pandas object."""

        sqlite_connection = sqlite3.connect('database/bus.db')
        cursor = sqlite_connection.cursor()

        dataframe.to_sql(table_name, con=sqlite_connection, if_exists='append')

        cursor.execute('SELECT * FROM ' + table_name + ' LIMIT 5')
        record = cursor.fetchall()
        print(record)



