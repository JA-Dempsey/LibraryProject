import requests
from datetime import datetime, timedelta

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

def get_due_date():
    response = requests.post(
        'http://localhost:47774/checkout',
        data='{"allowed_days_checkout":"5"}',
        headers={'Content-Type': 'application/json'})

    result = response.json()
    print(result)
    date = (datetime(2022,1,1) - timedelta(days=1)) + timedelta(days=result['date_due'])
    
    return date
    

