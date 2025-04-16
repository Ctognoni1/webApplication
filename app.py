from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Ciao! App Flask su URL personalizzato.'

if __name__ == '__main__':
    # Qui specifichi host e porta
    app.run(host='127.0.0.1', port=5000, debug=True)
