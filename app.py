from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from LibraryData import LibraryData, get_due_date, get_page_data
from datetime import date
from time import sleep


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sentientnova'
app.config['MYSQL_PASSWORD'] = 'YTcqyLuRuqebm6'
app.config['MYSQL_DB'] = 'library'
app.secret_key = 'asecretthinghere'

mysql = MySQL(app)
data = LibraryData(mysql)

@app.route('/', methods = ['GET'])
def index():
    # Start the page chain at 1 (first page)
    # Used when getting values for page
    if request.method == 'GET':
        return redirect("/1")

@app.route('/<cur_page>', methods = ['GET'])
def page(cur_page):

    if request.method == 'GET':
        ct_query = '''SELECT COUNT(*) FROM ITEMS'''
        cur_page = int(cur_page)
        page_data = get_page_data(cur_page, data, ct_query)

        if cur_page != str(1):
            row_limit = (cur_page-1) * 10
            results = data.execute('''SELECT * FROM ITEMS LIMIT 10 OFFSET %s''', [row_limit])
        else:
            results = data.execute('''SELECT * FROM ITEMS LIMIT 10''')
        
        page_data['type'] = 'index'
        
        return render_template('index.jinja', item_data = results, page_data = page_data)

@app.route('/return', methods = ['POST'])
def return_book():
    if request.method == 'POST':
        # Get data from the form clicked.
        key = list(request.form.keys())[0]

        # Get the type and the id # of the item's form clicked
        id = request.form[key]

        data.execute('''UPDATE Items SET lendee=%s, checkoutDate=%s, dueDate=%s WHERE itemsId = %s''', ["In Library","NULL", "NULL", id])

        return redirect("/")

@app.route('/delete', methods =['POST'])
def delete():
    if request.method == 'POST':
        # Get data from the form clicked.
        key = list(request.form.keys())[0]

        # Get the type and the id # of the item's form clicked
        id = request.form[key]

        data.execute('''DELETE FROM Items WHERE itemsId=%s''', [id])

        return redirect("/")


@app.route('/add', methods = ['POST', 'GET'])
def add():

    if request.method == 'GET':
        return render_template('add.jinja')

    if request.method == 'POST':
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']
        category = request.form['category']

        data.execute(''' INSERT INTO Items (name, author, isbn, category) VALUES (%s, %s, %s, %s)''', [name, author, isbn, category])

        # Send user back to main library list
        # After adding to database
        return redirect("/")
    

@app.route('/edit', methods = ['POST', 'GET'])
def edit():

    if request.method == 'GET':

        id = request.values['edit']
        results = data.execute('''SELECT * FROM Items WHERE itemsId=%s''', [id])
        return render_template('edit.jinja', id=id, item_data = results)

    if request.method == 'POST':
        id = request.form['save']
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']
        category = request.form['category']

        data.execute('''UPDATE Items SET name=%s, author=%s, isbn=%s, category=%s WHERE itemsId=%s''', [name, author, isbn, category, id])

        return redirect('/')

@app.route('/lend', methods = ['POST', 'GET'])
def lend():

    if request.method == 'GET':
        # Get id value from request
        id = request.values['lend']

        results = data.execute('''SELECT name FROM Items WHERE itemsID=%s''', [id])
        return render_template('lend.jinja', id = id, item_data = results)

    if request.method == 'POST':
        id = request.form['save']
        lendee = request.form['lendee']
        current_date = date.today()

        due_date = get_due_date()

        data.execute('''UPDATE Items SET lendee=%s, checkoutDate=%s, dueDate=%s WHERE itemsID=%s''', [lendee, current_date, due_date, id])

        return redirect('/')

@app.route('/search', methods = ['POST'])
def search_index():
    
    key = list(request.form.keys())[0]
    value = request.form[key]
    return redirect(f"/search/{value}/1")

@app.route("/search/<s_query>/<cur_page>", methods = ["GET"])
def search(s_query, cur_page):

    print("CURRENTPAGE", cur_page)
    # Build list for the SQL query, must contain
    # One value for each %s replaced in the SQL Query
    value = ['%' + str(s_query) + '%']*5

    cur_page = int(cur_page)

    # Define query to pass to get_page_data for the count of items
    query = '''SELECT COUNT(*) FROM ITEMS WHERE name LIKE %s OR author LIKE %s OR isbn LIKE %s OR lendee LIKE %s OR category LIKE %s'''
    page_data = get_page_data(cur_page, data, query, value)

    # Define query to use for selecting data with LIMIT and OFFSET
    query = '''SELECT * FROM ITEMS WHERE name LIKE %s OR author LIKE %s OR isbn LIKE %s OR lendee LIKE %s OR category LIKE %s'''
    if cur_page != str(1):
        query += " LIMIT 10 OFFSET %s"
        value.append((cur_page-1) * 10)
        results = data.execute(query, value)
    else:
        query += " LIMIT 10"
        results = data.execute(query, value)

    page_data["type"] = "search"
    page_data["search_query"] = str(s_query)

    return render_template('index.jinja', item_data = results, page_data = page_data)


if __name__ == '__main__':
    app.run(debug=True)