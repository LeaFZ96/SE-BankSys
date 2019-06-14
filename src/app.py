from flask import Flask, render_template, request
import config
from db_init import db
from models import User, Article

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/AddUser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('bio_form.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password') 

    newUser = Article(username=username, age=password)
    print(newUser.username)
    a = 储蓄账户()
    db.session.add(newUser)
    db.session.commit()

    return render_template('bio_form.html')

@app.route('/branch', methods=['GET', 'POST'])
def branch():
    labels = ['id', 'username', 'password']
    result = User.query.all()
    return render_template('branch.html', labels=labels, content=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)