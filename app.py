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

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':

        results = data.execute('''SELECT * FROM ITEMS''')

        return render_template('index.jinja', item_data = results)

    if request.method == 'POST':
        for key in request.form.keys():
            if key == 'edit':
                id = request.form[key]

                results = data.execute('''SELECT * FROM Items WHERE itemsId=%s''', [id])


                return render_template('edit.jinja', id=id, item_data = results)

            if key == 'delete':
                id = request.form[key]

                data.execute('''DELETE FROM Items WHERE itemsId=%s''', [id])

                return redirect("/")

            if key == 'lend':
                id = request.form[key]
                results = data.execute('''SELECT name FROM Items WHERE itemsID=%s''', [id])

                return render_template('lend.jinja', id = id, item_data = results)

            if key == 'return':
                id = request.form[key]

                data.execute('''UPDATE Items SET lendee=%s, checkoutDate=%s, dueDate=%s WHERE itemsId = %s''', ["In Library","NULL", "NULL", id])

        return redirect("/")


@app.route('/add', methods = ['POST', 'GET'])
def add():

    if request.method == 'GET':
        return render_template('add.jinja')

    if request.method == 'POST':
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']

        data.execute(''' INSERT INTO Items (name, author, isbn) VALUES (%s, %s, %s)''', [name, author, isbn])

        # Send user back to main library list
        # After adding to database
        return redirect("/")
    

@app.route('/edit', methods = ['POST', 'GET'])
def edit():

    if request.method == 'GET':
        return render_template('edit.jinja')

    if request.method == 'POST':
        id = request.form['save']
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']

        data.execute('''UPDATE Items SET name=%s, author=%s, isbn=%s WHERE itemsId=%s''', [name, author, isbn, id])

        return redirect('/')

@app.route('/lend', methods = ['POST', 'GET'])
def lend():

    if request.method == 'GET':
        return render_template('lend.jinja')

    if request.method == 'POST':
        id = request.form['save']
        lendee = request.form['lendee']
        current_date = date.today()

        due_date = get_due_date()

        data.execute('''UPDATE Items SET lendee=%s, checkoutDate=%s, dueDate=%s WHERE itemsID=%s''', [lendee, current_date, due_date, id])

        return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)