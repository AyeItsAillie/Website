from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app.secret_key = 'top-secret-game-key-ooga-booga'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamelist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text)
    multiplayer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

with app.app_context():
    db.create_all()


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

        # Create new profile in database
        try:
            new_profile = Game(
                game_name=game_name,
                platform=platform,
                comments=comments,
                multiplayer=multiplayer
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occurred while saving your profile. Please try again."
            return render_template('gameForm.html', error=error)


        return render_template(
            'gameSuccess.html',
                game_name=game_name,
                platform=platform,
                comments=comments,
                multiplayer=multiplayer
        )

    return render_template('gameForm.html')

@app.route('/admin/game')
def admin_game():
    games = Game.query.all()
    return render_template('admin_profiles.html', games=games)

#only shows multiplayer games
@app.route('/admin/game/multiplayer')
def admin_game_multiplayer():
    games = Game.query.filter_by(multiplayer=True).all()
    return render_template('admin_profiles.html', games=games)

#only shows multiplayer games only on steam
#@app.route('/admin/game/multiplayer_and_steam')
#def admin_game_multiplayer_on_steam():
#    games = Game.query.filter_by(multiplayer=True, platform="Steam").all()
#    return render_template('admin_profiles.html', games=games)


