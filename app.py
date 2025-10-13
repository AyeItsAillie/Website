from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
app.secret_key = 'top-secret-game-key-ooga-booga'

@app.route('/')
def index():
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])


def game():
    if request.method == 'POST':
        game_name = request.form.get('game_name', '').strip()
        platform = request.form.get('platform', '').strip()
        comments = request.form.get('comments', '').strip()
        multiplayer = request.form.get('multiplayer') == "yes" # True if checked
    # Validation
        if not game_name or not platform:
            error = "Please fill in all required fields"
            return render_template('gameForm.html', error=error)
        return render_template(
'gameSuccess.html',
game_name=game_name,
platform=platform,
comments=comments,
multiplayer=multiplayer
)
    return render_template('gameForm.html')
