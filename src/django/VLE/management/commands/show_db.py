from django.core.management.base import BaseCommand
import sqlite3

class Command(BaseCommand):
    help = 'Show the user, course, assignment and journal table.'


    def create_connection(self, db_file):
        try:
            return sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return None


    def handle(self, *args, **options):
        """Show the tables.

        These are: user, course, assignment and journal table
        """
        database = 'VLE.db'
        tables = ["user", "course", "assignment", "journal"]
        conn = self.create_connection(database)
        for table in tables:
            print(table)
            cur = conn.cursor()
            cur.execute("SELECT * FROM VLE_{}".format(table))
            for row in cur.fetchall():
                print(row)
            print()
        conn.close()
