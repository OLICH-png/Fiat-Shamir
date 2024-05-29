from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from forms import LoginForm, RegistrationForm
from fiat_shamir import FiatShamirAuth
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NIR'
auth_system = FiatShamirAuth()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['username'] = username
        session['round'] = 0
        session['y'] = None
        if auth_system.start_auth(username, password):
            return render_template('auth_round.html')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/start_auth', methods=['POST'])
def start_auth():
    username = session.get('username')
    if not username:
        return jsonify({'status': 'failed', 'message': 'User not logged in'})

    v = auth_system.get_v(username)
    r = random.randint(1, auth_system.n - 1)
    session['y'] = r
    x = pow(r, 2, auth_system.n)
    return jsonify({'status': 'continue', 'v': v, 'x': x})

@app.route('/auth_round', methods=['POST'])
def auth_round():
    username = session.get('username')
    if not username:
        return jsonify({'status': 'failed', 'message': 'User not logged in'})

    round_num = session['round']
    if round_num >= 16:
        flash('Login successful!', 'success')
        return jsonify({'status': 'success', 'message': 'Login successful'})

    e = int(request.json.get('e'))
    y = session.get('y')
    if y is None:
        return jsonify({'status': 'failed', 'message': 'No y value in session'})

    if auth_system.verify(username, y, e):
        session['round'] += 1
        if session['round'] >= 16:
            print(f"Round {round_num + 1}: Success")
            return jsonify({'status': 'success', 'message': 'Login successful'})
        else:
            print(f"Round {round_num + 1}: Success")
    else:
        print(f"Round {round_num + 1}: Failed")
        return jsonify({'status': 'failed', 'message': 'Invalid username or password'})

    v = auth_system.get_v(username)
    r = random.randint(1, auth_system.n - 1)
    session['y'] = r
    x = pow(r, 2, auth_system.n)

    return jsonify({'status': 'continue', 'v': v, 'x': x})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            auth_system.register(username, password)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
