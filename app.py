from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import yaml

app = Flask(__name__)
Bootstrap(app)

# Configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     return request.form['password']
        # return 'Successfully registered'
    cursor = mysql.connection.cursor()
    if cursor.execute("INSERT INTO user(user_name) VALUES('Ben')"):
        mysql.connection.commit()
        return 'success', 201
    # cursor.execute('INSERT INTO user VALUES(%s)', ['Mike'])
    # mysql.connection.commit()
    # result_value = cursor.execute('SELECT * FROM user')
    # if result_value > 0:
    #     users = cursor.fetchall()
    #     print(users)
        # return users[0]
    # fruits = ['Apple', 'Orange']
    return render_template('index.html')
    # , fruits=fruits)
    # return redirect(url_for('about'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/css')
def css():
    return render_template('css.html')

@app.errorhandler(404)
def page_not_found(e):
    return 'This Page was not found'

if __name__ == '__main__':
    app.run(debug=True, port=3000)