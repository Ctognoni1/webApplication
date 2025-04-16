from flask import Flask, render_template,request,redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'numeri.db'



@app.route('/')
def home():
   return render_template("index.html", nome="Mondo")

@app.route('/order')
def order():
    # Recupera il numero passato dalla query string
    numero = request.args.get('numero')
    return render_template("order.html", numero=numero)

@app.route('/submit', methods=['POST'])
def submit():
    numero = request.form.get('numero')


    # Redirect alla pagina /order, passando il numero come parte della query string
    return redirect(url_for('order', numero=numero))
if __name__ == '__main__':
    # Qui specifichi host e porta
    app.run(host='127.0.0.1', port=5000, debug=True)


