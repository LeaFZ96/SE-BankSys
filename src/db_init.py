from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

db2 = mysql.connector.connect(
    host='localhost',
    user='leafz',
    passwd='zhanglifu',
    database='bank'
)