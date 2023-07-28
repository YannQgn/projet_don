import mysql.connector as mysqlpyth


def connexion():
    global bdd
    global cursor
    bdd = mysqlpyth.connect(user='root', password='example',
                            host='localhost', port="3307", database='flask_don')
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
        don['pseudo'] = enregistrement[1]
        don['nom'] = enregistrement[2]
        don['prenom'] = enregistrement[3]
        don['adresse'] = enregistrement[4]
        don['email'] = enregistrement[5]
        don['somme_promise'] = enregistrement[6]
        don['date_promesse'] = enregistrement[7]
        dons.append(don)
    deconnexion()
    return dons


def get_paginated_dons(offset, items_par_page):
    global cursor
    connexion()
    query = "SELECT * FROM dons ORDER BY date_promesse DESC LIMIT %s, %s;"
    cursor.execute(query, (offset, items_par_page))
    dons = []
    for enregistrement in cursor:
        don = {}
        don['id'] = enregistrement[0]
        don['pseudo'] = enregistrement[1]
        don['nom'] = enregistrement[2]
        don['prenom'] = enregistrement[3]
        don['adresse'] = enregistrement[4]
        don['email'] = enregistrement[5]
        don['somme_promise'] = enregistrement[6]
        don['date_promesse'] = enregistrement[7]
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
        don['pseudo'] = enregistrement[1]
        don['nom'] = enregistrement[2]
        don['prenom'] = enregistrement[3]
        don['adresse'] = enregistrement[4]
        don['email'] = enregistrement[5]
        don['somme_promise'] = enregistrement[6]
        don['date_promesse'] = enregistrement[7]
    deconnexion()
    return don


def get_dernier_don():
    global cursor
    connexion()
    query = "SELECT * FROM dons ORDER BY date_promesse DESC LIMIT 1"
    cursor.execute(query)
    dernier_don = {}
    for enregistrement in cursor:
        dernier_don['id'] = enregistrement[0]
        dernier_don['pseudo'] = enregistrement[1]
        dernier_don['nom'] = enregistrement[2]
        dernier_don['prenom'] = enregistrement[3]
        dernier_don['adresse'] = enregistrement[4]
        dernier_don['email'] = enregistrement[5]
        dernier_don['somme_promise'] = enregistrement[6]
        dernier_don['date_promesse'] = enregistrement[7]
    deconnexion()
    return dernier_don


def add_don(pseudo, nom, prenom, adresse, email, somme_promise):
    global cursor
    global bdd
    connexion()
    query = 'INSERT INTO dons(pseudo, nom, prenom, adresse, email, somme_promise) VALUES (%s,%s, %s, %s, %s, %s);'
    values = (pseudo, nom, prenom, adresse, email, somme_promise)
    cursor.execute(query, values)
    bdd.commit()
    deconnexion()


def get_total_recolte():
    global cursor
    connexion()
    query = "SELECT SUM(somme_promise) FROM dons;"
    cursor.execute(query)
    total_recolte = cursor.fetchone()[0]
    deconnexion()
    return total_recolte


def get_total_dons_count():
    global cursor
    connexion()
    query = "SELECT COUNT(*) FROM dons"
    cursor.execute(query)
    total_count = cursor.fetchone()[0]
    deconnexion()
    return total_count
