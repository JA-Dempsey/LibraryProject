from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from LibraryData import LibraryData, get_due_date
from datetime import date
from time import sleep


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sentientnova'
app.config['MYSQL_PASSWORD'] = 'YTcqyLuRuqebm6'
app.config['MYSQL_DB'] = 'library'


mysql = MySQL(app)
data = LibraryData(mysql)

@app.route('/', methods = ['GET'])
def index():
    if request.method == 'GET':
        results = data.execute('''SELECT * FROM ITEMS''')
        return render_template('index.jinja', item_data = results)

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
def search():
    # Get data from the form clicked.
    key = list(request.form.keys())[0]

    # Build list for the SQL query, must contain
    # One value for each %s replaced in the SQL Query
    value = ['%' + str(request.form[key]) + '%']*5

    print(value)

    results = data.execute('''SELECT * FROM ITEMS WHERE name LIKE %s OR author LIKE %s OR isbn LIKE %s OR lendee like %s OR category LIKE %s''', value)

    return render_template('index.jinja', item_data = results)


if __name__ == '__main__':
    app.run(debug=True)