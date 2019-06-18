# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


t_accountAccessRecord = db.Table(
    'accountAccessRecord',
    db.Column('clientID', db.ForeignKey('client.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True),
    db.Column('savingsAccount', db.ForeignKey('savings_account.account', ondelete='CASCADE'), index=True),
    db.Column('checkAccount', db.ForeignKey('check_account.account', ondelete='CASCADE'), index=True),
    db.Column('depositDate', db.Date),
    db.Column('depositAmount', db.Float(15)),
    db.Column('withdrawalDate', db.Date),
    db.Column('withdrawalAmount', db.Float(15))
)


class Branch(db.Model):
    __tablename__ = 'branch'

    name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False, index=True)
    assets = db.Column(db.Float(15), nullable=False)
    city = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), nullable=False)
    num = db.Column(db.Integer, primary_key=True)


class BranchStaff(db.Model):
    __tablename__ = 'branch_staff'

    branchName = db.Column(db.ForeignKey('branch.name'), primary_key=True, nullable=False)
    staffID = db.Column(db.ForeignKey('sta.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    employDate = db.Column(db.Date)

    branch = db.relationship('Branch', primaryjoin='BranchStaff.branchName == Branch.name', backref='branch_staffs')
    sta = db.relationship('Sta', primaryjoin='BranchStaff.staffID == Sta.ID', backref='branch_staffs')


class CheckAccount(db.Model):
    __tablename__ = 'check_account'

    account = db.Column(db.BigInteger, primary_key=True)
    overdraft = db.Column(db.Float(20))
    openedDate = db.Column(db.Date)
    balance = db.Column(db.Float(15))
    latestVisitDate = db.Column(db.Date)


class Client(db.Model):
    __tablename__ = 'client'

    ID = db.Column(db.BigInteger, primary_key=True)
    staffID = db.Column(db.ForeignKey('sta.ID', ondelete='RESTRICT', onupdate='CASCADE'), index=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), nullable=False)
    phone = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    address = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'))

    sta = db.relationship('Sta', primaryjoin='Client.staffID == Sta.ID', backref='clients')


class ClientContact(db.Model):
    __tablename__ = 'clientContact'

    clientID = db.Column(db.ForeignKey('client.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), nullable=False)
    phone = db.Column(db.BigInteger)
    email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
    relation = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))

    contact = db.relationship('Client', primaryjoin='ClientContact.clientID == Client.ID', backref='contacts')


class ClientBranchCheckAccount(db.Model):
    __tablename__ = 'client_branch_check_account'

    clientID = db.Column(db.ForeignKey('client.ID', onupdate='CASCADE'), primary_key=True, nullable=False)
    branchNum = db.Column(db.ForeignKey('branch.num', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    checkAccount = db.Column(db.BigInteger, nullable=False, unique=True)

    branch = db.relationship('Branch', primaryjoin='ClientBranchCheckAccount.branchNum == Branch.num', backref='client_branch_check_accounts')
    client = db.relationship('Client', primaryjoin='ClientBranchCheckAccount.clientID == Client.ID', backref='client_branch_check_accounts')


class ClientBranchSavingsAccount(db.Model):
    __tablename__ = 'client_branch_savings_account'

    clientID = db.Column(db.ForeignKey('client.ID', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    branchNum = db.Column(db.ForeignKey('branch.num', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    savingsAccount = db.Column(db.BigInteger, nullable=False, unique=True)

    branch = db.relationship('Branch', primaryjoin='ClientBranchSavingsAccount.branchNum == Branch.num', backref='client_branch_savings_accounts')
    client = db.relationship('Client', primaryjoin='ClientBranchSavingsAccount.clientID == Client.ID', backref='client_branch_savings_accounts')


class Depart(db.Model):
    __tablename__ = 'depart'

    departNum = db.Column(db.Integer, primary_key=True)
    dapartName = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), nullable=False)
    dapartType = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))


class Loan(db.Model):
    __tablename__ = 'loan'

    loanNum = db.Column(db.Integer, primary_key=True)
    branchName = db.Column(db.ForeignKey('branch.name', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    loanAmount = db.Column(db.Float(15), nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    createdDate = db.Column(db.Date)

    branch = db.relationship('Branch', primaryjoin='Loan.branchName == Branch.name', backref='loans')


t_loan_to_client = db.Table(
    'loan_to_client',
    db.Column('loanNum', db.ForeignKey('loan.loanNum'), nullable=False, index=True),
    db.Column('clientID', db.ForeignKey('client.ID', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True),
    db.Column('date', db.Date),
    db.Column('amount', db.Float(15))
)


class SavingsAccount(db.Model):
    __tablename__ = 'savings_account'

    account = db.Column(db.BigInteger, primary_key=True)
    interestRate = db.Column(db.Float(20))
    currencyType = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
    openedDate = db.Column(db.Date)
    balance = db.Column(db.Float(15))
    latestVisitDate = db.Column(db.Date)


class Sta(db.Model):
    __tablename__ = 'sta'

    ID = db.Column(db.BigInteger, primary_key=True)
    departNum = db.Column(db.ForeignKey('depart.departNum', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), nullable=False)
    telephone = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    address = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'))
    position = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))

    depart = db.relationship('Depart', primaryjoin='Sta.departNum == Depart.departNum', backref='stas')
