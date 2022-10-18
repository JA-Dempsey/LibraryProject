from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sentientnova'
app.config['MYSQL_PASSWORD'] = 'YTcqyLuRuqebm6'
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM Items''')
        mysql.connection.commit()
        results = cursor.fetchall()
        cursor.close

        print(results)

        return render_template('index.jinja', item_data = results)

    if request.method == 'POST':
        for key in request.form.keys():
            if key == 'edit':
                id = request.form[key]

                cursor = mysql.connection.cursor()
                cursor.execute('''SELECT * FROM Items WHERE itemsId=%s''', id)
                mysql.connection.commit()
                results = cursor.fetchall()
                cursor.close

                return render_template('edit.jinja', id=id, item_data = results)

            if key == 'delete':
                id = request.form[key]
                cursor = mysql.connection.cursor()
                cursor.execute('''DELETE FROM Items WHERE itemsId=%s''', id)
                mysql.connection.commit()
                cursor.close()

                return redirect("/")

        return redirect("/")


@app.route('/add', methods = ['POST', 'GET'])
def add():

    if request.method == 'GET':
        return render_template('add.jinja')

    if request.method == 'POST':
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO Items (name, author, isbn) VALUES (%s, %s, %s)''', (name, author, isbn))
        mysql.connection.commit()
        cursor.close()

        # Send user back to main library list
        # After adding to database
        return render_template('index.jinja')

@app.route('/edit', methods = ['POST', 'GET'])
def edit():

    if request.method == 'GET':
        return render_template('edit.jinja')

    if request.method == 'POST':
        id = request.form['save']
        name = request.form['itemname']
        author = request.form['author']
        isbn = request.form['isbn']

        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Items SET name=%s, author=%s, isbn=%s WHERE itemsId=%s''', (name, author, isbn, id))
        mysql.connection.commit()
        cursor.close()

        return redirect('/')
    