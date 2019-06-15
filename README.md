# SE-BankSys
Bank system project



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

