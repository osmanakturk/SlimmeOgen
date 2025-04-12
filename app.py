from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/functie/<naam>')
def functie(naam):
    return render_template('result.html', functie=naam)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
