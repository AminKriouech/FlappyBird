from flask import Flask, request, render_template, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PAROLE = ['Python', 'Flask', 'Mafia', 'Denaro', 'Pitbull']

def scegli_parole():
    return random.choice(PAROLE)

def inizializza_gioco():
    word = scegli_parole()
    session['parola'] = word
    session['tentativo'] = [ ]
    session['tentativi_rimasti'] = 6

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tentativo = request.form.get('tentativo')
        if tentativo and len(tentativo) == 1 and tentativo.isalpha:
            tentativo = tentativo.lower()
            if tentativo not in session['tentativi']:
                session['tentativi'].append(tentativo)
                if tentativo not in session['parola']:
                    session['tentativi_rimasti'] -= 1
                    if session['tentativi_rimasti'] <= 0 or all(letter in session['tentativi'] for letter in session['parole']):
                        return redirect(url_for('result'))
                    if 'parola' not in session:
                        inizializza_gioco()
                        word_display = ''.join([letter if letter in session['tentativi'] else '_' for letter in session['word']])
                        return render_template('index.html', word_display=word_display, tentativi_rimasti=session['tentativi_rimasti'], tentativi=session['tentativi'])

@app.route('/result')
def result():
    parola = session['parola']
    vittoria = all(letter in session['tentativi'] for letter in parola)
    return render_template('result.html', parola=parola, vittoria=vittoria)

@app.route('/new_game')
def new_game():
    inizializza_gioco()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
