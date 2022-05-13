"""
flash() -  на стороне сервера
get_flash_messeges() - в шаблоне 

flash() -> session -> get_flash_messeges() -> шаблон
"""
from flask import Flask, render_template, url_for, request, flash, abort, session, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjhgidfbgiedbg234g'
users = [
    {'username': 'Patrokhin', 'password': '12345', 'is_admin': True},
    {'username': 'Student', 'password': '1060', 'is_admin': False},
]


@app.route('/')
def begin():
    return f"""
ссылка на <a href="/base">базовую</a> страницу<br>
ссылка на <a href="/start">стартовую</a> страницу<br>
ссылка на <a href={url_for('index')}>index</a> страницу<br>
ссылка на <a href={url_for('form')}>страницу с формой</a><br>
ссылка на <a href={url_for('login')}>страницу с авторизацией</a>
"""


@app.route('/dase/index')
def index():
    username = 'Patrokhin'
    return render_template('index.html', username=username)


@app.route('/day-<num>')
def day(num):
    return render_template(f'day-{num}.html')


@app.route('/photo-<num>')
def photo(num):
    return render_template(f'photo-{num}.html')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/start')
def start():
    return render_template(f'start.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('profile', username=session['logged_in']))

    if request.method == 'POST':
        for user in users:
            if request.form['username'] == user['username']:
                if request.form['password'] == user['password']:
                    session['logged_in'] = user['username']
                    return redirect(url_for('profile', username=user['username']))
                else:
                    flash('Неправильный пароль', category='error')
                    return render_template('login.html')
            else:
                flash('Такого пользователя не существует', category='error')

    return render_template('login.html')


@app.route('/form', methods={'GET', 'POST'})
def form():
    if request.method == 'POST':
        if len(request.form['fullname']) < 5 and not request.form['fullname'].isalpha():
            flash('Ошибка в имени. сообщение не отправлено!')
    else:
      flash('сообщение принято!')
      for iten in request.form:
        print(item, request.form[item])
    return render_template('form.html')


@app.route('/profile/<username>')
def profile(username):
    for user in users:
        if user['username'] == username:
            if 'logged_in' in session:
                if session['logged_in'] == username:
                    return render_template('profile.html', username=username)
        flash('Вам туда нельзя. Залогинтесь', category='error')
        return redirect(url_for('login'))

        abort(404)


if __name__ == '__main__':
    app.run(debug=True)



