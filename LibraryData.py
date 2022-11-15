class LibraryData:
    """Class for pulling data from a database."""

    def __init__(self, mysql):
        self.mysql = mysql
        self.last = None

    def execute(self, statement, vars=None):
        cursor = self.mysql.connection.cursor()

        if vars is None:
            cursor.execute(statement)
        else:
            cursor.execute(statement, vars)

        self.mysql.connection.commit()
        results = cursor.fetchall()
        cursor.close

        # Save the data for the last query.
        self.last = results

        return results