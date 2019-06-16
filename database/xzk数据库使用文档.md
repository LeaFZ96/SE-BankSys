# xzk数据库使用文档

1. 支行管理

   在branch表直接操作即可，注意，若branch_staff, accountAccessRecord, 和loan表中有相关branchName则branch主表中的信息不可删除；三个表都设置为级联修改，直接在branch改名可以把三个表的branchName全部更改。

2. 员工管理

   sta表，增加员工信息时，要先在sta表增加一行信息，然后在branch_staff表增加对应的信息(不加branch_staff不会报错，但会信息缺失)；删除表时，client表中有对sta的外键，若在client表中有对应员工信息则不允许被删除；修改，设置为级联修改，在sta中直接修改即可。

3. 客户管理

   client表，增加client信息时，先在client表加信息，然后在clientContact表加信息(不加不会报错，但是要求必须加一个联系人)；删除时，若accountAccessRecord和loan_to_client表中有数据，则无法删除；修改，设置为级联修改，直接改ID即可。

4. 账户管理

   client_branch_account表，增加时，先在client_branch_account表加信息，然后在对应的支票或储蓄账户表加信息；删除，要先在checkAcount和savingsAccount表删除信息，然后在client_branch_account表删除；修改，无法修改。

   每次存取记录写在accountAccessRecord表里，一定要有对应的客户ID和账户号。

   **注意savingsAccount和checkAccount是varchar类型，一定要加双引号。(不然006会变成6)**

5. 贷款管理

   loan表，增加，先在Loan表加对应信息，根据发放给客户的情况，在loan_to_client表里添加，**注意loanNum是varchar类型，要加双引号**；删除，如果在loan_to_client表里有对应记录则无法删除；修改，若loan_to_client表里有对应loan表的信息则无法修改，loan_to_client里可以修改。

   贷款状态，默认0，表示未发放，发放中是1，发放完毕是2，超出发放金额是3，表示异常。每次在loan_to_client表里添加记录，需要执行一次存储过程dkstatus(int dknum)来修改存储状态。

6. 存储过程

   dkstatus(int dknum)是修改贷款状态的；其余均为业务统计函数，cxck表示储蓄存款，cxqk表示储蓄取款，dk表示贷款。

   示例：cxckmonth(in ye int, in mon int, in branch varchar(15), out money float, out number int)

   ye表示年份，mon表示月份，branch表示分行，money表示输出的统计金额，number表示用户人数。

   ```
   call dkmonth(2014,6,"合肥分行",@a,@b);
   select @a;
   select @b;
   ```

   