# coding=UTF-8
from flask import Flask, render_template, request, abort
import config
import numpy as np
import datetime
from db_init import db, db2
from flask_sqlalchemy import sqlalchemy
from models import Branch, Client, Sta, SavingsAccount, CheckAccount, Loan, ClientBranchSavingsAccount, ClientBranchCheckAccount, ClientContact, BranchStaff, t_loan_to_client, t_accountAccessRecord

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

cursor = db2.cursor()

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
    result_query = db.session.query(Branch)
    result = result_query.all()
    if request.method == 'GET':
        return render_template('branch.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'query':
            branch_num = request.form.get('branchNum')
            branch_name = request.form.get('name')
            branch_asset = request.form.get('estate')
            branch_city = request.form.get('city')

            if branch_num != "":
                result_query = result_query.filter(Branch.num == branch_num)
            if branch_name != "":
                result_query = result_query.filter(Branch.name == branch_name)
            if branch_asset != "":
                result_query = result_query.filter(Branch.assets == branch_asset)
            if branch_city != "":
                result_query = result_query.filter(Branch.city == branch_city)
            
            result = result_query.all()

            return render_template('branch.html', labels=labels, content=result)
            
        elif request.form.get('type') == 'update':
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
    result_query = db.session.query(Sta, BranchStaff).filter(Sta.ID == BranchStaff.staffID)
    result = result_query.all()

    if request.method == 'GET':
        return render_template('staff.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'query':
            ID = request.form.get('staffID')
            branch = request.form.get('branch')
            departNum = request.form.get('departNum')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            position = request.form.get('position')
            date = request.form.get('date')

            if ID != '':
                result_query = result_query.filter(Sta.ID == ID)
            if branch != '':
                result_query = result_query.filter(BranchStaff.branchName == branch)
            if departNum != '':
                result_query = result_query.filter(Sta.departNum == departNum)
            if name != '':
                result_query = result_query.filter(Sta.name == name)
            if phone != '':
                result_query = result_query.filter(Sta.telephone == phone)
            if address != '':
                result_query = result_query.filter(Sta.address == address)
            if position != '':
                result_query = result_query.filter(Sta.position == position)
            if date != '':
                date = date.split('-')
                date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))
                result_query = result_query.filter(BranchStaff.employDate == date)

            result = result_query.all()

            return render_template('staff.html', labels=labels, content=result)
            
        elif request.form.get('type') == 'update':
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

    content1_query = db.session.query(SavingsAccount, ClientBranchSavingsAccount, Client, Branch).filter(
        SavingsAccount.account == ClientBranchSavingsAccount.savingsAccount).filter(ClientBranchSavingsAccount.clientID == Client.ID).filter(Branch.num == ClientBranchSavingsAccount.branchNum)
    content2_query = db.session.query(CheckAccount, ClientBranchCheckAccount, Client, Branch).filter(
        CheckAccount.account == ClientBranchCheckAccount.checkAccount).filter(ClientBranchCheckAccount.clientID == Client.ID).filter(Branch.num == ClientBranchCheckAccount.branchNum)

    content1 = content1_query.all()
    content2 = content2_query.all()

    if request.method == 'GET':
        return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)
    else:
        if request.form.get('type') == 'squery':
            accNum = request.form.get('accNum')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            branchNum = request.form.get('branch')
            openDate = request.form.get('openDate')
            latestVisitDate = request.form.get('latestVisitDate')
            balance = request.form.get('balance')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')

            if accNum != "":
                content1_query = content1_query.filter(SavingsAccount.account == accNum)
            if clientID != "":
                content1_query = content1_query.filter(Client.ID == clientID)
            if clientName != "":
                content1_query = content1_query.filter(Client.name == clientName)
            if branchNum != "":
                content1_query = content1_query.filter(ClientBranchSavingsAccount.branchNum == branchNum)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content1_query = content1_query.filter(SavingsAccount.openedDate == openDate)
            if latestVisitDate != "":
                latestVisitDate = latestVisitDate.split('-')
                latestVisitDate = datetime.date(
                int(latestVisitDate[0]), int(latestVisitDate[1]), int(latestVisitDate[2]))
                content1_query = content1_query.filter(SavingsAccount.latestVisitDate == latestVisitDate)
            if balance != "":
                content1_query = content1_query.filter(SavingsAccount.balance == balance)
            if interestRate != "":
                content1_query = content1_query.filter(SavingsAccount.interestRate == interestRate)
            if currType != "":
                content1_query = content1_query.filter(SavingsAccount.currencyType == currType)
            
            content1 = content1_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)

        elif request.form.get('type') == 'cquery':
            accNum = request.form.get('accNum')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            branchNum = request.form.get('branch')
            openDate = request.form.get('openDate')
            latestVisitDate = request.form.get('latestVisitDate')
            balance = request.form.get('balance')
            accType = request.form.get('accType')
            overDraft = request.form.get('overDraft')

            if accNum != "":
                content2_query = content2_query.filter(CheckAccount.account == accNum)
            if clientID != "":
                content2_query = content2_query.filter(Client.ID == clientID)
            if clientName != "":
                content2_query = content2_query.filter(Client.name == clientName)
            if branchNum != "":
                content2_query = content2_query.filter(ClientBranchCheckAccount.branchNum == branchNum)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content2_query = content2_query.filter(CheckAccount.openedDate == openDate)
            if latestVisitDate != "":
                latestVisitDate = latestVisitDate.split('-')
                latestVisitDate = datetime.date(
                int(latestVisitDate[0]), int(latestVisitDate[1]), int(latestVisitDate[2]))
                content2_query = content2_query.filter(CheckAccount.latestVisitDate == latestVisitDate)
            if balance != "":
                content2_query = content2_query.filter(CheckAccount.balance == balance)
            if overDraft != "":
                content2_query = content2_query.filter(CheckAccount.overdraft == overDraft)
            
            content2 = content2_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)

        elif request.form.get('type') == 'addAcc':
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

            acc_temp = content1_query.filter(ClientBranchSavingsAccount.savingsAccount == oldAccount).first()
            ins = t_accountAccessRecord.insert()
            if var_balance > 0:
                db.session.execute(db.insert(t_accountAccessRecord, values={'clientID': acc_temp[2].ID, 'savingsAccount': oldAccount, 'depositDate': latestDate, 'depositAmount': var_balance}))
            elif var_balance < 0:
                db.session.execute(db.insert(t_accountAccessRecord, values={'clientID': acc_temp[2].ID, 'savingsAccount': oldAccount, 'withdrawalDate': latestDate, 'withdrawalAmount': abs(var_balance)}))

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
            acc_temp = content2_query.filter(ClientBranchCheckAccount.checkAccount == oldAccount).first()
            ins = t_accountAccessRecord.insert()
            if var_balance > 0:
                db.session.execute(db.insert(t_accountAccessRecord, values={'clientID': acc_temp[2].ID, 'checkAccount': oldAccount, 'depositDate': latestDate, 'depositAmount': var_balance}))
            elif var_balance < 0:
                db.session.execute(db.insert(t_accountAccessRecord, values={'clientID': acc_temp[2].ID, 'checkAccount': oldAccount, 'withdrawalDate': latestDate, 'withdrawalAmount': abs(var_balance)}))

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
    labels2 = ['贷款号', '客户ID', '发放日期', '发放金额']

    content_query = db.session.query(Loan)
    content = content_query.all()
    result = []

    if request.method == 'GET':
        return render_template('debt.html', labels=labels, labels2=labels2, content=content, content2=result)
    else:
        if request.form.get('type') == 'main_query':
            num = request.form.get('num')
            branch = request.form.get('branch')
            money = request.form.get('money')
            date = request.form.get('date')
            state = request.form.get('state')

            if num != '':
                content_query = content_query.filter(Loan.loanNum == num)
            if branch != '':
                content_query = content_query.filter(Loan.branchName == branch)
            if money != '':
                content_query = content_query.filter(Loan.loanAmount == money)
            if date != '':
                date = date.split('-')
                date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))
                content_query = content_query.filter(Loan.createdDate == date)
            if state != '':
                content_query = content_query.filter(Loan.status == state)

            content = content_query.all()

            return render_template('debt.html', labels=labels, labels2=labels2, content=content, content2=result)

        elif request.form.get('type') == 'update':
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
            if loan_result.status == 1:
                error_title = '删除错误'
                error_message = '不可删除状态为1的贷款信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            db.session.delete(loan_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            branch = request.form.get('branch')
            money = request.form.get('money')
            date = request.form.get('date')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))
            
            newLoan = Loan(
                branchName = branch,
                loanAmount = money,
                status = 0,
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
            cursor.callproc('dkstatus', (loanNum,))
            db2.commit()

    content = db.session.query(Loan).all()

    return render_template('debt.html', labels=labels, content=content, labels2=labels2, content2=result)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    bank_list = [['合肥', 100, 100, 100], ['成都', 250, 250, 250], ['杭州', 300, 300, 300], ['南京', 120, 120, 120]]

    bank_all = db.session.query(Branch).all()
    new_bank_list = []
    for i in bank_all:
        new_bank_list.append([i.num, i.name])

    if request.method == 'GET':
        return render_template('statistics.html', bank_list=bank_list)
    else:
        '''
            i[0]: 支行号
            i[1]: 支行名
            i[2]: 储蓄存款
            i[3]: 储蓄取款
            i[4]: 贷款总金额
            i[5]: 储蓄总人数
            i[6]: 贷款总人数
        '''
        if request.form.get('type') == 'year':
            year = request.form.get('year')
            for i in new_bank_list:
                cxck = cursor.callproc('cxckyear', (int(year), i[0], None, None))
                cxqk = cursor.callproc('cxqkyear', (int(year), i[0], None, None))
                dk = cursor.callproc('dkyear', (int(year), i[1], None, None))
                num = cursor.callproc('cxyearNum', (int(year), i[0], None))
                i.append(cxck[2])   # i[2]
                i.append(cxqk[2])   # i[3]
                i.append(dk[2])     # i[4]
                i.append(num[2])    # i[5]
                i.append(dk[3])     # i[6]

            #return str(new_bank_list)
        elif request.form.get('type') == 'season':
            year = request.form.get('year')
            season = request.form.get('season')
            for i in new_bank_list:
                cxck = cursor.callproc('cxckseason', (int(year), int(season), i[0], None, None))
                cxqk = cursor.callproc('cxqkseason', (int(year), int(season), i[0], None, None))
                dk = cursor.callproc('dkseason', (int(year), int(season), i[1], None, None))
                num = cursor.callproc('cxseasonNum', (int(year), int(season), i[0], None))
                i.append(cxck[3])   # i[2]
                i.append(cxqk[3])   # i[3]
                i.append(dk[3])     # i[4]
                i.append(num[3])    # i[5]
                i.append(dk[4])     # i[6])
            
        elif request.form.get('type') == 'month':
            year = request.form.get('year')
            month = request.form.get('month')
            for i in new_bank_list:
                cxck = cursor.callproc('cxckmonth', (int(year), int(month), i[0], None, None))
                cxqk = cursor.callproc('cxqkmonth', (int(year), int(month), i[0], None, None))
                dk = cursor.callproc('dkmonth', (int(year), int(month), i[1], None, None))
                num = cursor.callproc('cxmonthNum', (int(year), int(month), i[0], None))
                i.append(cxck[3])   # i[2]
                i.append(cxqk[3])   # i[3]
                i.append(dk[3])     # i[4]
                i.append(num[3])    # i[5]
                i.append(dk[4])     # i[6]

    
    
    #bank_list = [['合肥', 100], ['成都', 250], ['杭州', 300], ['南京', 120]]
    bank_list = new_bank_list
    #return str(bank_list)
    return render_template('statistics.html', bank_list=bank_list)


@app.route('/test', methods=['GET', 'POST'])
def test_mod():
    args = cursor.callproc('cxckseason', (2019, 3, 111, None, None))
    stri = (["".join(str(x) for x in args)][0])
    stri = str(args[3])
    return stri

@app.route('/404')
def not_found():
    
    return render_template('404.html', error_title='错误标题', error_message='错误信息')

@app.errorhandler(Exception)
def err_handle(e):
    error_message = ''
    error_title = ''
    if (type(e) == IndexError):
        error_title = '填写错误'
        error_message = '日期格式错误! (yyyy-mm-dd)'
    elif (type(e) == AssertionError):
        error_title = '删除错误'
        error_message = '删除条目仍有依赖！'
    elif (type(e) == sqlalchemy.exc.IntegrityError):
        error_title = '更新/插入错误'
        error_message = str(e._message())
    return render_template('404.html', error_title=error_title, error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
