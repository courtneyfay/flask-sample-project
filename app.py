from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

# Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        age = form['age']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
        mysql.connection.commit()
    return render_template('index.html')

@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cursor.fetchall()
        session['username'] = employees[0]['name']
        return render_template('employees.html', employees=employees)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # if request.method == 'POST':
#     #     return request.form['password']
#         # return 'Successfully registered'
#     cursor = mysql.connection.cursor()
#     if cursor.execute("INSERT INTO user(user_name) VALUES('Ben')"):
#         mysql.connection.commit()
#         return 'success', 201
#     # cursor.execute('INSERT INTO user VALUES(%s)', ['Mike'])
#     # mysql.connection.commit()
#     # result_value = cursor.execute('SELECT * FROM user')
#     # if result_value > 0:
#     #     users = cursor.fetchall()
#     #     print(users)
#         # return users[0]
#     # fruits = ['Apple', 'Orange']
#     return render_template('index.html')
#     # , fruits=fruits)
#     # return redirect(url_for('about'))
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
# @app.route('/css')
# def css():
#     return render_template('css.html')
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return 'This Page was not found'

if __name__ == '__main__':
    app.run(debug=True, port=3000)