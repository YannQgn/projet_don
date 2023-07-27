import mysql.connector as mysqlpyth


def connexion():
    global bdd
    global cursor
    bdd = mysqlpyth.connect(user='root', password='example',
                            host='127.0.0.1', port="3307", database='flask_don')
    cursor = bdd.cursor(buffered=True)


def deconnexion():
    global bdd
    global cursor
    cursor.close()
    bdd.close()


def get_all_dons():
    global cursor
    connexion()
    query = "SELECT * FROM `dons`;"
    cursor.execute(query)
    dons = []
    for enregistrement in cursor:
        don = {}
        don['id'] = enregistrement[0]
        don['nom'] = enregistrement[1]
        don['prenom'] = enregistrement[2]
        don['adresse'] = enregistrement[3]
        don['email'] = enregistrement[4]
        don['somme_promise'] = enregistrement[5]
        don['date_promesse'] = enregistrement[6]
        dons.append(don)
    deconnexion()
    return dons


def get_don(id):
    global cursor
    connexion()
    query = "SELECT * FROM dons WHERE id = %s"
    cursor.execute(query, (id,))
    don = {}
    for enregistrement in cursor:
        don['id'] = enregistrement[0]
        don['nom'] = enregistrement[1]
        don['prenom'] = enregistrement[2]
        don['adresse'] = enregistrement[3]
        don['email'] = enregistrement[4]
        don['somme_promise'] = enregistrement[5]
        don['date_promesse'] = enregistrement[6]
    deconnexion()
    return don


def add_don(nom, prenom, adresse, email, somme_promise):
    global cursor
    global bdd
    connexion()
    query = 'INSERT INTO dons(nom, prenom, adresse, email, somme_promise) VALUES (%s, %s, %s, %s, %s);'
    values = (nom, prenom, adresse, email, somme_promise)
    cursor.execute(query, values)
    bdd.commit()
    deconnexion()
