from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database helper functions
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()

@app.route('/')
def home():
    return render_template('index.html')

# Create
@app.route('/add-task/', methods=['POST'])
def add_task():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO tasks (name, description) VALUES (?, ?)", (name, description))
                con.commit()
                msg = "Task successfully added."
        except Exception as e:
            con.rollback()
            msg = "Error occurred: " + str(e)
        finally:
            return redirect(url_for('list_tasks'))

# Read
@app.route('/list-tasks/')
def list_tasks():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    return render_template('list_tasks.html', rows=rows)

# Update
@app.route('/edit-task/<int:task_id>/', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE tasks SET name = ?, description = ? WHERE id = ?", (name, description, task_id))
                con.commit()
                msg = "Task successfully updated."
        except Exception as e:
            con.rollback()
            msg = "Error occurred: " + str(e)
        finally:
            return redirect(url_for('list_tasks'))
    else:
        con = sqlite3.connect('database.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        return render_template('edit_task.html', row=row)

# Delete
@app.route('/delete-task/<int:task_id>/')
def delete_task(task_id):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            con.commit()
            msg = "Task successfully deleted."
    except Exception as e:
        con.rollback()
        msg = "Error occurred: " + str(e)
    finally:
        return redirect(url_for('list_tasks'))

if __name__ == "__main__":
    app.run(debug=True)
