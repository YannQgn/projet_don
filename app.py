from flask import Flask, render_template, request
import data

app = Flask(__name__)


@app.route('/')
def index():
    dons = data.get_all_dons()
    return render_template('index.html', dons=dons)


@app.route('/don/<int:don_id>')
def don(don_id):
    don = data.get_don(don_id)
    return render_template('donation.html', don=don)


@app.route('/new_donation')
def new_donation():
    return render_template('new_donation.html')


@app.route('/donation_confirmed', methods=['GET'])
def donation_confirmed():
    nom = request.values.get('nom')
    prenom = request.values.get('prenom')
    adresse = request.values.get('adresse')
    email = request.values.get('email')
    somme_promise = request.values.get('somme_promise')
    data.add_don(nom, prenom, adresse, email, somme_promise)
    return render_template('donation_confirmed.html')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
