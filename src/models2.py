# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, Float, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


t_accountAccessRecord = db.Table(
    'accountAccessRecord',
    db.Column('clientID', db.ForeignKey('client.ID', ondelete='CASCADE', onupdate='CASCADE'), index=True),
    db.Column('savingsAccount', db.ForeignKey('client_branch_account.savingsAccount', ondelete='RESTRICT', onupdate='RESTRICT'), index=True),
    db.Column('checkAccount', db.ForeignKey('client_branch_account.checkAccount', ondelete='RESTRICT', onupdate='RESTRICT'), index=True),
    db.Column('depositDate', db.Date),
    db.Column('depositAmount', db.Float(15)),
    db.Column('withdrawalDate', db.Date),
    db.Column('withdrawalAmount', db.Float(15))
)


class Branch(db.Model):
    __tablename__ = 'branch'

    name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True)
    assets = db.Column(db.Float(15))
    city = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))


class BranchStaff(db.Model):
    __tablename__ = 'branch_staff'

    branchName = db.Column(db.ForeignKey('branch.name', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    staffID = db.Column(db.ForeignKey('sta.ID', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    employDate = db.Column(db.Date)

    branch = db.relationship('Branch', primaryjoin='BranchStaff.branchName == Branch.name', backref='branch_staffs')
    sta = db.relationship('Sta', primaryjoin='BranchStaff.staffID == Sta.ID', backref='branch_staffs')


class Client(db.Model):
    __tablename__ = 'client'

    ID = db.Column(db.BigInteger, primary_key=True)
    staffID = db.Column(db.ForeignKey('sta.ID'), index=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
    phone = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    address = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'))

    sta = db.relationship('Sta', primaryjoin='Client.staffID == Sta.ID', backref='clients')


class ClientContact(Client):
    __tablename__ = 'clientContact'

    clientID = db.Column(db.ForeignKey('client.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
    phone = db.Column(db.BigInteger)
    email = db.Column(db.String(50, 'utf8mb4_0900_ai_ci'))
    relation = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))


class ClientBranchAccount(db.Model):
    __tablename__ = 'client_branch_account'
    __table_args__ = (
        db.Index('tt', 'savingsAccount', 'checkAccount'),
        db.Index('ee', 'clientID', 'checkAccount')
    )

    clientID = db.Column(db.BigInteger, primary_key=True, nullable=False, index=True)
    branchName = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), primary_key=True, nullable=False, index=True)
    savingsAccount = db.Column(db.String(19, 'utf8mb4_0900_ai_ci'), index=True)
    checkAccount = db.Column(db.String(19, 'utf8mb4_0900_ai_ci'), index=True)


class SavingsAccount(ClientBranchAccount):
    __tablename__ = 'savingsAccount'

    account = db.Column(db.ForeignKey('client_branch_account.savingsAccount'), primary_key=True)
    openDate = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Float(20), nullable=False)
    latestVisitDate = db.Column(db.Date)
    interestRate = db.Column(db.Float(20))
    currencyType = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))


class CheckAccount(ClientBranchAccount):
    __tablename__ = 'checkAccount'

    account = db.Column(db.ForeignKey('client_branch_account.checkAccount'), primary_key=True)
    openedDate = db.Column(db.Date)
    balance = db.Column(db.Float(20))
    latestVisitDate = db.Column(db.Date)
    overdraft = db.Column(db.Float(20))


class Depart(db.Model):
    __tablename__ = 'depart'

    departNum = db.Column(db.Integer, primary_key=True)
    dapartName = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
    dapartType = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))


class Loan(db.Model):
    __tablename__ = 'loan'

    loanNum = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'), primary_key=True)
    branchName = db.Column(db.ForeignKey('branch.name', ondelete='RESTRICT', onupdate='CASCADE'), index=True)
    loanAmount = db.Column(db.Float(15))
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    createdDate = db.Column(db.Date)

    branch = db.relationship('Branch', primaryjoin='Loan.branchName == Branch.name', backref='loans')


t_loan_to_client = db.Table(
    'loan_to_client',
    db.Column('loanNum', db.ForeignKey('loan.loanNum'), nullable=False, index=True),
    db.Column('clientID', db.ForeignKey('client.ID', ondelete='RESTRICT', onupdate='CASCADE'), index=True),
    db.Column('date', db.Date),
    db.Column('amount', db.Float(15))
)


class Sta(db.Model):
    __tablename__ = 'sta'

    ID = db.Column(db.BigInteger, primary_key=True)
    departNum = db.Column(db.ForeignKey('depart.departNum', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    name = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))
    telephone = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    address = db.Column(db.String(30, 'utf8mb4_0900_ai_ci'))
    position = db.Column(db.String(10, 'utf8mb4_0900_ai_ci'))

    depart = db.relationship('Depart', primaryjoin='Sta.departNum == Depart.departNum', backref='stas')
