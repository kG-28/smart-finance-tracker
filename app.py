from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def read_expenses():
    expenses = []
    if os.path.exists('expenses.csv'):
        with open('expenses.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                expenses.append(row)
    return expenses

def write_expenses(expenses):
    with open('expenses.csv', 'w', newline='') as file:
        fieldnames = ['date', 'description', 'amount', 'category']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(expense)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        data = {
            'date': request.form['date'],
            'description': request.form['description'],
            'amount': request.form['amount'],
            'category': request.form['category']
        }
        expenses = read_expenses()
        expenses.append(data)
        write_expenses(expenses)
        return redirect(url_for('history'))
    return render_template('add_expense.html')

@app.route('/history')
def history():
    expenses = read_expenses()
    query = request.args.get('query', '').lower()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    filtered = []
    for exp in expenses:
        if query in exp['description'].lower() or query in exp['category'].lower():
            if start_date and exp['date'] < start_date:
                continue
            if end_date and exp['date'] > end_date:
                continue
            filtered.append(exp)

    return render_template('history.html', expenses=filtered)

@app.route('/delete/<int:index>')
def delete_expense(index):
    expenses = read_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        write_expenses(expenses)
    return redirect(url_for('history'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_expense(index):
    expenses = read_expenses()
    if request.method == 'POST':
        expenses[index] = {
            'date': request.form['date'],
            'description': request.form['description'],
            'amount': request.form['amount'],
            'category': request.form['category']
        }
        write_expenses(expenses)
        return redirect(url_for('history'))
    return render_template('edit_expense.html', expense=expenses[index], index=index)

@app.route('/piechart')
def piechart():
    expenses = read_expenses()
    summary = defaultdict(float)
    for exp in expenses:
        summary[exp['category']] += float(exp['amount'])
    return render_template('piechart.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
