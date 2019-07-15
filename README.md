# SE-BankSys
## 环境

- mysql 8.0
- python 3.5+

python 包：

- flask
- flask-sqlalchemy

- flask-sqlacodegen
- numpy
- mysql-connector
- pymysql

下载方式：

```
pip install xxxx
```



### 生成models.py

```shell
flask-sqlacodegen 'mysql+pymysql://root:root@localhost:3306/bank' --flask > models.py
```



### 运行

```
python app.py
```



Bank system project
Based on Flask and MySQL

![](img/index.png)


```mermaid
graph LR;
用户--查询/更新/插入/删除--> 前端;
用户 --业务统计--> 前端;
前端 --Table--> 用户
前端 --HTTP POST/GET--> MYSQL;
MYSQL --JSON--> 前端;
MYSQL --Query--> 后端;
后端 --结果--> MYSQL;

```

