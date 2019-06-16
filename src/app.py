# coding=UTF-8
from flask import Flask, render_template, request
import config
import numpy as np
import datetime
from db_init import db
from models import Branch, Client, Sta, SavingsAccount, CheckAccount, Loan, ClientBranchSavingsAccount, ClientBranchCheckAccount

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
    labels = ['支行编号', '支行名', '支行资产', '所在城市']
    result = db.session.query(Branch).all()
    if request.method == 'GET':
        return render_template('branch.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'update':
            old_num = request.form.get('key')
            branch_name = request.form.get('branch_name')
            branch_asset = request.form.get('branch_asset')
            branch_city = request.form.get('branch_city')
            branch_result = db.session.query(
                Branch).filter_by(num=old_num).first()
            branch_result.name = branch_name
            branch_result.assets = branch_asset
            branch_result.city = branch_city
            db.session.commit()

        elif request.form.get('type') == 'delete':
            old_num = request.form.get('key')
            branch_result = db.session.query(
                Branch).filter_by(name=old_num).first()
            db.session.delete(branch_result)
            db.session.commit()

    result = db.session.query(Branch).all()

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
    labels1 = ['账户号', '客户ID', '客户姓名', '开户支行',
               '开户时间', '账户余额', '最近访问时间', '利率', '货币类型']
    labels2 = ['账户号', '客户ID', '客户姓名', '开户支行', '开户时间', '账户余额', '最近访问时间', '透支额度']

    content1 = db.session.query(SavingsAccount, ClientBranchSavingsAccount, Client).filter(
        SavingsAccount.account == ClientBranchSavingsAccount.savingsAccount).filter(ClientBranchSavingsAccount.clientID == Client.ID).all()
    content2 = db.session.query(CheckAccount, ClientBranchCheckAccount, Client).filter(
        CheckAccount.account == ClientBranchCheckAccount.checkAccount).filter(ClientBranchCheckAccount.clientID == Client.ID).all()

    if request.method == 'GET':

        return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)
    else:
        if request.form.get('type') == 'addAcc':
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            branchNum = request.form.get('branch')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            accType = request.form.get('accType')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')
            overDraft = request.form.get('overDraft')

            clientNotExist = db.session.query(
                Client.ID).filter_by(ID=clientID).scalar() is None
            if clientNotExist:
                a = 0
            # 客户不存在要报错，客户添加再客户管理页面处理

            openDate = openDate.split('-')
            openDate = datetime.date(int(openDate[0]), int(openDate[1]), int(openDate[2]))
            clientID = int(clientID)
            balance = float(balance)
            interestRate = float(interestRate)
            overDraft = float(overDraft)

            if accType == 'saving':
                # client_branch_account 表中存储账户和支票账户是否存在检查
                newClientBranch = ClientBranchSavingsAccount(
                    clientID=clientID,
                    branchNum=branchNum,
                    savingsAccount=accStr
                )
            else:
                newClientBranch = ClientBranchCheckAccount(
                    clientID=clientID,
                    branchNum=branchNum,
                    checkAccount=accStr
                )
            db.session.add(newClientBranch)
            db.session.commit()
            
            if accType == 'saving':
                newAccount = SavingsAccount(
                    openDate=openDate,
                    balance=balance,
                    latestVisitDate=openDate,
                    interestRate=interestRate,
                    currencyType=currType
                )
                newAccount.account = newClientBranch.savingsAccount
                db.session.add(newAccount)
                db.session.commit()
            else:
                newAccount = CheckAccount(
                    account=accStr,
                    openedDate=openDate,
                    balance=balance,
                    latestVisitDate=openDate,
                    overdraft=overDraft
                )
                db.session.add(newAccount)
                db.session.commit()
            

            content1 = db.session.query(SavingsAccount, ClientBranchAccount, Client).filter(
                SavingsAccount.account == ClientBranchAccount.savingsAccount).filter(ClientBranchAccount.clientID == Client.ID).all()
            content2 = db.session.query(CheckAccount, ClientBranchAccount, Client).filter(
                CheckAccount.account == ClientBranchAccount.checkAccount).filter(ClientBranchAccount.clientID == Client.ID).all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)

        elif request.form.get('type') == 'supdate':
            oldAccount = request.form.get('key')
            openDate = request.form.get('sOpenDate')
            balance = request.form.get('sBalance')
            latestDate = request.form.get('sLatest')
            interestRate = request.form.get('sInterest')
            currType = request.form.get('sCType')
        elif request.form.get('type') == 'cupdate':
            oldAccount = request.form.get('key')
            openDate = request.form.get('cOpenDate')
            balance = request.form.get('cBalance')
            latestDate = request.form.get('cLatest')
            overDraft = request.form.get('cOver')
        elif request.form.get('type') == 'delete':
            oldAccount = request.form.get('key')

    return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)


@app.route('/debt', methods=['GET', 'POST'])
def debt():
    labels = ['贷款号', '支行', '贷款金额', '贷款状态', '建立日期']
    content = Loan.query.all()
    return render_template('debt.html', labels=labels, content=content)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template('statistics.html')


@app.route('/test', methods=['GET', 'POST'])
def test_mod():
    old_name = request.form.get('old_name')
    result = db.session.query(Branch).filter_by(name=old_name).first()
    stri = str(result.name)
    return stri


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
