from flask import Flask, request, url_for, redirect, render_template
import sqlite3

app = Flask(__name__)

conn = None

def get_conn():
    global conn
    if conn is None:
        conn = sqlite3.connect("lab.db")
        conn.row_factory = sqlite3.Row
    return conn

def disconn():
    global conn
    if conn != None:
        conn.close()
        conn = None

def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query,args)
    r = cur.fetchall()
    cur.close()
    return( r[0] if r else None) if one else r

def add_task(cat, prior, descrip):
    query_db("insert into tasks(category, priority, description) values(?,?,?)", (cat,prior,descrip))
    get_conn().commit();

@app.route('/', methods = ['GET', 'POST'])
def tasks():
    if request.method == 'POST' :
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        try:
            if int(priority) >100 or int(priority) < 0:
                raise Exception
        except:
            return "invalid priority"
        add_task(category,priority, description)
        return redirect(url_for('tasks'))
    elif request.method == 'GET':
        tasks = query_db('SELECT * FROM tasks ORDER BY priority DESC')
        return render_template('main.html', tasks=tasks)

if __name__ == "__main__":
    app.debug = True
    app.run()

