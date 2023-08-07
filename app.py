from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import data


app = Flask(__name__)

app.secret_key = '2RR3D3sd223D'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'example'
app.config['MYSQL_DB'] = 'flask_don'
app.config['MYSQL_PORT'] = 3307
mysql = MySQL(app)


@app.route('/')
def index():
    dernier_don = data.get_dernier_don()
    return render_template('index.html', dernier_don=dernier_don)


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    msg = ''
    dernier_don = data.get_dernier_don()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('index.html', username=session['username'], dernier_don=dernier_don)
        else:
            msg = 'Nom d\'utilisateur ou mot de passe incorrect !'
    return render_template('login.html', msg=msg)


@app.route('/admin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/admin/donations', defaults={'page': 1})
@app.route('/admin/donations/<int:page>')
def admin_donations(page):
    if 'loggedin' in session:
        items_par_page = 8
        total_entries = data.get_total_dons_count()
        total_pages = (total_entries + items_par_page - 1) // items_par_page
        total = data.get_total_recolte()
        offset = (page - 1) * items_par_page
        dons = data.get_paginated_dons(offset, items_par_page)
        dernier_don = data.get_dernier_don()
        return render_template('admin_donations.html', username=session['username'], dons=dons,  total_pages=total_pages, total=total, dernier_don=dernier_don, total_entries=total_entries, items_par_page=items_par_page)
    flash("Vous ne pouvez pas accéder à cette page sans être connecté(e).")
    return redirect(url_for('login'))


@app.route('/donations', defaults={'page': 1})
@app.route('/donations/<int:page>')
def donations(page):
    items_par_page = 8
    total_entries = data.get_total_dons_count()
    total_pages = (total_entries + items_par_page - 1) // items_par_page
    total = data.get_total_recolte()
    offset = (page - 1) * items_par_page
    dons = data.get_paginated_dons(offset, items_par_page)
    dernier_don = data.get_dernier_don()
    return render_template('user_donations.html', dons=dons, total_pages=total_pages, dernier_don=dernier_don, total_entries=total_entries, items_par_page=items_par_page, total=total)


@app.route('/don/<int:don_id>')
def don(don_id):
    don = data.get_don(don_id)
    dernier_don = data.get_dernier_don()
    return render_template('donation.html', don=don, dernier_don=dernier_don)


@app.route('/new_donation')
def new_donation():
    dernier_don = data.get_dernier_don()
    return render_template('new_donation.html', dernier_don=dernier_don)


@app.route('/donation_confirmed', methods=['GET'])
def donation_confirmed():
    pseudo = request.values.get('pseudo')
    nom = request.values.get('nom')
    prenom = request.values.get('prenom')
    adresse = request.values.get('adresse')
    email = request.values.get('email')
    somme_promise = request.values.get('somme_promise')
    dernier_don = data.get_dernier_don()
    data.add_don(pseudo, nom, prenom, adresse, email, somme_promise)
    return render_template('donation_confirmed.html', email=email, dernier_don=dernier_don)


@app.route('/conditions')
def conditions():
    dernier_don = data.get_dernier_don()
    return render_template('conditions.html', dernier_don=dernier_don)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
