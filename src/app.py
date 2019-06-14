from flask import Flask, render_template, request
import config
from db_init import db
from models2 import Branch, Client, Sta, SavingsAccount, CheckAccount, Loan

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

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

@app.route('/branch', methods=['GET', 'POST'])
def branch():
    labels = ['支行名', '支行资产', '所在城市']
    result = Branch.query.all()
    return render_template('branch.html', labels=labels, content=result)

@app.route('/client', methods=['GET', 'POST'])
def client():
    labels = ['客户ID', '客户姓名', '客户电话', '客户地址', '负责员工ID']
    result = Client.query.all()
    return render_template('client.html', labels=labels, content=result)

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    labels = ['员工ID', '部门号', '员工姓名', '员工电话', '员工地址', '员工职位']
    result = Sta.query.all()
    return render_template('staff.html', labels=labels, content=result)

@app.route('/account', methods=['GET', 'POST'])
def account():
    labels1 = ['账户号', '开户时间', '余额', '最近访问时间', '利率', '货币类型']
    labels2 = ['账户号', '开户时间', '余额', '最近访问时间', '透支额度']
    content1 = SavingsAccount.query.all()
    content2 = CheckAccount.query.all()
    return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)

@app.route('/debt', methods=['GET', 'POST'])
def debt():
    labels = ['贷款号', '支行', '贷款金额', '贷款状态', '建立日期']
    content = Loan.query.all()
    return render_template('debt.html', labels=labels, content=content)

@app.route('/test')
def test_mod():
    result = db.session.query(Branch).filter_by(name='合肥分行').first()
    result.name = '北京分行'
    db.session.commit()
    return 'Hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)