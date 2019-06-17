# coding=UTF-8
from flask import Flask, render_template, request
import config
import numpy as np
import datetime
from db_init import db
from models import Branch, Client, Sta, SavingsAccount, CheckAccount, Loan, ClientBranchSavingsAccount, ClientBranchCheckAccount, ClientContact, BranchStaff, t_loan_to_client

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
                Branch).filter_by(num=old_num).first()
            db.session.delete(branch_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            branch_name = request.form.get('name')
            branch_asset = request.form.get('estate')
            branch_city = request.form.get('city')

            newBranch = Branch(
                name = branch_name,
                assets = branch_asset,
                city = branch_city
            )

            db.session.add(newBranch)
            db.session.commit()

    result = db.session.query(Branch).all()

    return render_template('branch.html', labels=labels, content=result)


@app.route('/client', methods=['GET', 'POST'])
def client():
    labels = ['客户ID', '客户姓名', '客户电话', '客户地址', '负责员工ID', '联系人姓名', '联系人手机', '联系人邮箱', '与客户关系']
    result_query = db.session.query(Client, ClientContact).filter(Client.ID == ClientContact.clientID)
    result = result_query.all()

    if request.method == 'GET':
        return render_template('client.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'query':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            staffID = request.form.get('staffID')
            cname = request.form.get('cname')
            cphone = request.form.get('cphone')
            cemail = request.form.get('cemail')
            crelation = request.form.get('crelation')

            if clientID != '':
                result_query = result_query.filter(Client.ID == clientID)
            if clientName != '':
                result_query = result_query.filter(Client.name == clientName)
            if clientPhone != '':
                result_query = result_query.filter(Client.phone == clientPhone)
            if clientAddress != '':
                result_query = result_query.filter(Client.address == clientAddress)
            if staffID != '':
                result_query = result_query.filter(Client.staffID == staffID)
            if cname != '':
                result_query = result_query.filter(ClientContact.name == cname)
            if cphone != '':
                result_query = result_query.filter(ClientContact.phone == cphone)
            if cemail != '':
                result_query = result_query.filter(ClientContact.email == cemail)
            if crelation != '':
                result_query = result_query.filter(ClientContact.relation == crelation)

            result = result_query.all()

            return render_template('client.html', labels=labels, content=result)

        elif request.form.get('type') == 'update':
            clientID = request.form.get('key')
            # 更新还没做
        elif request.form.get('type') == 'delete':
            clientID = request.form.get('key')
            client_result = db.session.query(Client).filter_by(ID=clientID).first()
            clientContact_result = db.session.query(ClientContact).filter_by(clientID=clientID).first()

            db.session.delete(clientContact_result)
            db.session.delete(client_result)
            db.session.commit()
            # 删除无效

        elif request.form.get('type') == 'insert':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            staffID = request.form.get('staffID')
            cname = request.form.get('cname')
            cphone = request.form.get('cphone')
            cemail = request.form.get('cemail')
            crelation = request.form.get('crelation')
            
            newClient = Client(
                ID = clientID,
                staffID = staffID,
                name = clientName,
                phone = clientPhone,
                address = clientAddress
            )

            newContact = ClientContact(
                clientID = clientID,
                name = cname,
                phone = cphone,
                email = cemail,
                relation = crelation
            )

            db.session.add(newClient)
            db.session.add(newContact)
            db.session.commit()


    result = db.session.query(Client, ClientContact).filter(Client.ID == ClientContact.clientID).all()
    
    return render_template('client.html', labels=labels, content=result)


@app.route('/staff', methods=['GET', 'POST'])
def staff():
    labels = ['员工ID', '所在支行', '部门号', '员工姓名', '员工电话', '员工地址', '员工职位', '雇佣日期']
    result = db.session.query(Sta, BranchStaff).filter(Sta.ID == BranchStaff.staffID).all()

    if request.method == 'GET':
        return render_template('staff.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'update':
            oldID = request.form.get('key')
            departNum = request.form.get('departNum')
            phone = request.form.get('phone')
            address = request.form.get('address')
            position = request.form.get('position')

            staff_result = db.session.query(Sta).filter_by(ID=oldID).first()

            staff_result.departNum = departNum
            staff_result.telephone = phone
            staff_result.address = address
            staff_result.position = position

            db.session.commit()

        elif request.form.get('type') == 'delete':
            oldID = request.form.get('key')

            staff_result = db.session.query(Sta).filter_by(ID=oldID).first()
            branchStaff_result = db.session.query(BranchStaff).filter_by(staffID=oldID).first()

            db.session.delete(branchStaff_result)
            db.session.delete(staff_result)
            db.session.commit()
        
        elif request.form.get('type') == 'insert':
            ID = request.form.get('staffID')
            branch = request.form.get('branch')
            departNum = request.form.get('departNum')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            position = request.form.get('position')
            date = request.form.get('date')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            newStaff = Sta(
                ID = ID,
                departNum = departNum,
                name = name,
                telephone = phone,
                address = address,
                position = position
            )

            newStaffBranch = BranchStaff(
                branchName = branch,
                staffID = ID,
                employDate = date
            )

            db.session.add(newStaff)
            db.session.add(newStaffBranch)
            db.session.commit()
        
    result = db.session.query(Sta, BranchStaff).filter(Sta.ID == BranchStaff.staffID).all()

    return render_template('staff.html', labels=labels, content=result)


@app.route('/account', methods=['GET', 'POST'])
def account():
    labels1 = ['账户号', '客户ID', '客户姓名', '开户支行号', '开户支行名',
               '开户时间', '账户余额', '最近访问时间', '利率', '货币类型']
    labels2 = ['账户号', '客户ID', '客户姓名', '开户支行号',
               '开户支行名', '开户时间', '账户余额', '最近访问时间', '透支额度']

    content1 = db.session.query(SavingsAccount, ClientBranchSavingsAccount, Client, Branch).filter(
        SavingsAccount.account == ClientBranchSavingsAccount.savingsAccount).filter(ClientBranchSavingsAccount.clientID == Client.ID).filter(Branch.num == ClientBranchSavingsAccount.branchNum).all()
    content2 = db.session.query(CheckAccount, ClientBranchCheckAccount, Client, Branch).filter(
        CheckAccount.account == ClientBranchCheckAccount.checkAccount).filter(ClientBranchCheckAccount.clientID == Client.ID).filter(Branch.num == ClientBranchCheckAccount.branchNum).all()

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
            openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))
            clientID = int(clientID)
            balance = float(balance)
            interestRate = float(interestRate)
            overDraft = float(overDraft)

            if accType == 'saving':
                # client_branch_account 表中存储账户和支票账户是否存在检查
                newClientBranch = ClientBranchSavingsAccount(
                    clientID=clientID,
                    branchNum=branchNum
                )
            else:
                newClientBranch = ClientBranchCheckAccount(
                    clientID=clientID,
                    branchNum=branchNum
                )
            db.session.add(newClientBranch)
            db.session.commit()

            if accType == 'saving':
                newAccount = SavingsAccount(
                    openedDate=openDate,
                    balance=balance,
                    latestVisitDate=openDate,
                    interestRate=interestRate,
                    currencyType=currType
                )
                newAccount.account = newClientBranch.savingsAccount

            else:
                newAccount = CheckAccount(
                    openedDate=openDate,
                    balance=balance,
                    latestVisitDate=openDate,
                    overdraft=overDraft
                )
                newAccount.account = newClientBranch.checkAccount

            db.session.add(newAccount)
            db.session.commit()

        elif request.form.get('type') == 'supdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('sBalance')
            latestDate = request.form.get('sLatest')
            interestRate = request.form.get('sInterest')
            currType = request.form.get('sCType')

            account_result = db.session.query(
                SavingsAccount).filter_by(account=oldAccount).first()

            latestDate = latestDate.split('-')
            latestDate = datetime.date(
                int(latestDate[0]), int(latestDate[1]), int(latestDate[2]))
            # 交易记录表
            var_balance = float(balance) - account_result.balance
            account_result.balance = balance
            account_result.latestVisitDate = latestDate
            account_result.interestRate = interestRate
            account_result.currencyType = currType
            db.session.commit()

        elif request.form.get('type') == 'cupdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('cBalance')
            latestDate = request.form.get('cLatest')
            overDraft = request.form.get('cOver')

            account_result = db.session.query(
                CheckAccount).filter_by(account=oldAccount).first()

            latestDate = latestDate.split('-')
            latestDate = datetime.date(
                int(latestDate[0]), int(latestDate[1]), int(latestDate[2]))

            # 交易记录表
            var_balance = float(balance) - account_result.balance
            account_result.balance = balance
            account_result.latestVisitDate = latestDate
            account_result.overdraft = overDraft
            db.session.commit()

        elif request.form.get('type') == 'delete':
            oldAccount = request.form.get('key')
            accType = request.form.get('accType')

            if accType == 'saving':
                account_result = db.session.query(
                    SavingsAccount).filter_by(account=oldAccount).first()
                accountClient_result = db.session.query(
                    ClientBranchSavingsAccount).filter_by(savingsAccount=oldAccount).first()
                db.session.delete(account_result)
                db.session.delete(accountClient_result)
                db.session.commit()

            else:
                account_result = db.session.query(
                    CheckAccount).filter_by(account=oldAccount).first()
                accountClient_result = db.session.query(
                    ClientBranchCheckAccount).filter_by(checkAccount=oldAccount).first()
                db.session.delete(account_result)
                db.session.delete(accountClient_result)
                db.session.commit()

    content1 = db.session.query(SavingsAccount, ClientBranchSavingsAccount, Client, Branch).filter(
        SavingsAccount.account == ClientBranchSavingsAccount.savingsAccount).filter(ClientBranchSavingsAccount.clientID == Client.ID).filter(Branch.num == ClientBranchSavingsAccount.branchNum).all()
    content2 = db.session.query(CheckAccount, ClientBranchCheckAccount, Client, Branch).filter(
        CheckAccount.account == ClientBranchCheckAccount.checkAccount).filter(ClientBranchCheckAccount.clientID == Client.ID).filter(Branch.num == ClientBranchCheckAccount.branchNum).all()

    return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)


@app.route('/debt', methods=['GET', 'POST'])
def debt():
    labels = ['贷款号', '发放支行', '贷款金额', '贷款状态', '建立日期']
    content = db.session.query(Loan).all()
    labels2 = ['贷款号', '客户ID', '发放日期', '发放金额']
    result = []
    #db.session.query(t_loan_to_client).filter_by(loanNum=i.loanNum).all()

    if request.method == 'GET':
        return render_template('debt.html', labels=labels, labels2=labels2, content=content, content2=result)
    else:
        if request.form.get('type') == 'update':
            oldNum = request.form.get('key')
            money = request.form.get('money')
            state = request.form.get('state')

            loan_result = db.session.query(Loan).filter_by(loanNum=oldNum).first()

            loan_result.loanAmount = money
            loan_result.status = state

            db.session.commit()

        elif request.form.get('type') == 'delete':
            oldNum = request.form.get('key')
            
            loan_result = db.session.query(Loan).filter_by(loanNum=oldNum).first()
            db.session.delete(loan_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            branch = request.form.get('branch')
            money = request.form.get('money')
            date = request.form.get('date')
            state = request.form.get('state')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))
            
            newLoan = Loan(
                branchName = branch,
                loanAmount = money,
                status = state,
                createdDate = date
            )

            db.session.add(newLoan)
            db.session.commit()
        
        elif request.form.get('type') == 'query':
            loanNum = request.form.get('loanNum')
            
            result = db.session.query(t_loan_to_client).filter_by(loanNum=loanNum).all()

        elif request.form.get('type') == 'give':
            loanNum = request.form.get('loanNum')
            clientID = request.form.get('clientID')
            date = request.form.get('date')
            money = request.form.get('money')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            ins = t_loan_to_client.insert()
            db.session.execute(db.insert(t_loan_to_client, values={'loanNum': loanNum, 'clientID': clientID, 'date': date, 'amount': money}))
            db.session.commit()

    content = db.session.query(Loan).all()

    return render_template('debt.html', labels=labels, content=content, labels2=labels2, content2=result)


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
