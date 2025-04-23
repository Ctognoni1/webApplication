import io
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///miodatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modello Utente
class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valore = db.Column(db.Integer, default=0)
    lun = db.Column(db.Integer, default=0)

# Home
@app.route('/')
def home():
    return render_template("index.html", nome="database")

# Pagina ordine
@app.route('/order')
def order():
    utenti = Utente.query.all()
    return render_template("order.html", utenti=utenti)

# Gestione form
@app.route('/submit', methods=['POST'])
def submit():
    utenti = Utente.query.all()

    for utente in utenti:
        valore = request.form.get(f"valore_{utente.id}")
        lun = request.form.get(f"lunedi_{utente.id}")

        if valore and valore.isdigit():
            utente.valore = int(valore)

        if lun and lun.isdigit():
            utente.lun = int(lun)
            utente.valore += utente.lun

    db.session.commit()
    return redirect(url_for('order'))

# Genera grafico
def generate_plot_png():
    utenti = Utente.query.all()
    nomi = [u.nome for u in utenti]
    valori = [u.valore or 0 for u in utenti]

    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(nomi, valori)
    ax.set_xlabel('Nome Utente')
    ax.set_ylabel('Valore')
    ax.set_title('Valori Utenti')

    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)
    return buf

# Route del grafico
@app.route('/plot.png')
def plot_png():
    buf = generate_plot_png()
    return Response(buf.getvalue(), mimetype='image/png')

# Inizializza DB
with app.app_context():
    db.create_all()
    if not Utente.query.first():
        db.session.add_all([
            Utente(nome="Alice"),
            Utente(nome="Bob"),
            Utente(nome="Charlie")
        ])
        db.session.commit()

# Avvio app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
