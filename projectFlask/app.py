from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "your_secret_key"

def connect_to_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_gui"
        )
        if db.is_connected():
            print("Successfully connected to the Database")
            return db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

db_connection = connect_to_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_timer():
    activity_name = request.form['activity_name']
    work_time = int(request.form['work_time'])
    short_break = int(request.form['short_break'])
    long_break = int(request.form['long_break'])
    cycles = int(request.form['cycles'])

    # Simpan data ke session untuk digunakan di halaman timer
    session['activity_name'] = activity_name
    session['work_time'] = work_time
    session['short_break'] = short_break
    session['long_break'] = long_break
    session['cycles'] = cycles

    total_work_time = work_time * cycles
    total_short_break_time = short_break * (cycles - 1)
    total_long_break_time = long_break

    total_time_seconds = total_work_time + total_short_break_time + total_long_break_time
    total_time = str(timedelta(seconds=total_time_seconds))

    if db_connection:
        cursor = db_connection.cursor()
        query = "INSERT INTO history (name, date, time) VALUES (%s, %s, %s)"
        values = (activity_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_time)
        try:
            cursor.execute(query, values)
            db_connection.commit()
            flash('Pomodoro session logged successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
        finally:
            cursor.close()

    # Redirect ke halaman timer
    return redirect(url_for('timer'))

@app.route('/timer')
def timer():
    # Ambil data dari session untuk ditampilkan di halaman timer
    if 'activity_name' in session:
        activity_name = session['activity_name']
        work_time = session['work_time']
        short_break = session['short_break']
        long_break = session['long_break']
        cycles = session['cycles']
        return render_template('timer.html', activity_name=activity_name, work_time=work_time, short_break=short_break, long_break=long_break, cycles=cycles)
    else:
        return redirect(url_for('index'))

@app.route('/totals')
def show_totals():
    if db_connection:
        cursor = db_connection.cursor()
        query = "SELECT name, date, time FROM history"
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return render_template('totals.html', results=results, enumerate=enumerate)
        except mysql.connector.Error as err:
            flash(f"Error: {err}", 'danger')
            return redirect(url_for('index'))
        finally:
            cursor.close()
    else:
        flash('Database connection error', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
