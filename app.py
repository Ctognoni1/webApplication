from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miodatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definizione del modello Utente
class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valore = db.Column(db.Integer)
    lun = db.Column(db.Integer)

# Route per la home
@app.route('/')
def home():
    return render_template("index.html", nome="database")

# Route per la pagina dell'ordine
@app.route('/order')
def order():
    # Recupera tutti gli utenti
    utenti = Utente.query.all()
    return render_template("order.html", utenti=utenti)

# Route per gestire l'invio dei dati dal form
@app.route('/submit', methods=['POST'])
def submit():
    utenti = Utente.query.all()

    for utente in utenti:
        # Ottieni i valori dal form per ogni utente
        valore = request.form.get(f"valore_{utente.id}")
        Lun = request.form.get(f"lunedi_{utente.id}")

        # Controlla e aggiorna il valore
        if valore and valore.isdigit():
            utente.valore = int(valore)

        # Controlla e aggiorna le ore lavorate il lunedì
        if Lun and Lun.isdigit():
            utente.lun = int(Lun)

    # Commit per salvare tutte le modifiche nel database
    db.session.commit()
    
    # Redirect alla pagina degli ordini
    return redirect(url_for('order'))

# Crea il database e aggiungi gli utenti se non esistono
with app.app_context():
    db.create_all()
    if not Utente.query.first():
        db.session.add_all([
            Utente(nome="Alice"),
            Utente(nome="Bob"),
            Utente(nome="Charlie")
        ])
        db.session.commit()

# Avvia l'app Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)