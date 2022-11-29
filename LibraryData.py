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

def get_page_data(cur_page, data, count_query, values=None):
    # Get current ct of items in library
    count = data.execute(count_query, values)[0][0]

    # Create a page_data dict
    page_data = {'pages':[], 'current': cur_page, 'max':0}

    # Calculate the number of pages (currently 10 items per page)
    pages = count // 10
    if count % 20 != 0:
        pages += 1

    # Add numbers for use in frontend to 'pages'
    # key of page_data
    counter = 1
    while pages > 0:
        page_data['pages'].append(counter)
        counter += 1
        pages -= 1

    # Save the max pages possible for the navigation
    # below table in frontend
    page_data['max'] = len(page_data['pages'])

    return page_data

