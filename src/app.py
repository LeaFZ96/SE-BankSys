from flask import Flask, render_template, request
import config
from db_init import db
from models2 import Branch

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
        city = request.form.get('city')

    #newUser = Article(username=username, age=password)
    newUser = Branch(name=username, assets=password, city=city)
    db.session.add(newUser)
    db.session.commit()

    return render_template('bio_form.html')

@app.route('/branch_test', methods=['GET', 'POST'])
def branch_test():
    labels = ['id', 'username', 'password']
    result = User.query.all()
    return render_template('branch.html', labels=labels, content=result)

@app.route('/branch', methods=['GET', 'POST'])
def branch():
    labels = ['支行名', '支行资产', '所在城市']
    result = Branch.query.all()
    return render_template('branch.html', labels=labels, content=result)

@app.route('/test')
def test_mod():
    result = db.session.query(Branch).filter_by(name='合肥分行').first()
    result.name = '北京分行'
    db.session.commit()
    return 'Hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)