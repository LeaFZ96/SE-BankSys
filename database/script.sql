create table branch
(
    name   varchar(15)  not null,
    assets float(15, 0) not null,
    city   varchar(10)  not null,
    num    int(10) auto_increment
        primary key
);

create index name
    on branch (name);

create table check_account
(
    account         bigint(19)   not null
        primary key,
    overdraft       float(20, 3) null,
    openedDate      date         null,
    balance         float(15, 0) null,
    latestVisitDate date         null
);

create table depart
(
    departNum  int(4)      not null
        primary key,
    dapartName varchar(10) not null,
    dapartType varchar(10) null
);

create table loan
(
    loanNum     int(10) auto_increment
        primary key,
    branchName  varchar(10)      not null,
    loanAmount  float(15, 0)     not null,
    status      int(1) default 0 not null,
    createdDate date             null,
    constraint fk_loan
        foreign key (branchName) references branch (name)
            on update cascade
);

create table savings_account
(
    account         bigint(19)   not null
        primary key,
    interestRate    float(20, 3) null,
    currencyType    varchar(10)  null,
    openedDate      date         null,
    balance         float(15, 0) null,
    latestVisitDate date         null
);

create table sta
(
    ID        bigint(18)  not null
        primary key,
    departNum int(8)      null,
    name      varchar(10) not null,
    telephone varchar(15) null,
    address   varchar(30) null,
    position  varchar(10) null,
    constraint fk_departNum
        foreign key (departNum) references depart (departNum)
            on update cascade on delete cascade
);

create table branch_staff
(
    branchName varchar(15) not null,
    staffID    bigint(18)  not null,
    employDate date        null,
    primary key (branchName, staffID),
    constraint fk_branch_staff2
        foreign key (staffID) references sta (ID)
            on update cascade on delete cascade,
    constraint fk_bs
        foreign key (branchName) references branch (name)
);

create table client
(
    ID      bigint(18)  not null
        primary key,
    staffID bigint(18)  null,
    name    varchar(10) not null,
    phone   varchar(15) null,
    address varchar(30) null,
    constraint fk_dfdf
        foreign key (staffID) references sta (ID)
            on update cascade
);

create table accountAccessRecord
(
    clientID         bigint(18)   not null,
    savingsAccount   bigint(19)   null,
    checkAccount     bigint(19)   null,
    depositDate      date         null,
    depositAmount    float(15, 0) null,
    withdrawalDate   date         null,
    withdrawalAmount float(15, 0) null,
    constraint fk_aAR
        foreign key (savingsAccount) references savings_account (account)
            on delete cascade,
    constraint fk_aAR2
        foreign key (checkAccount) references check_account (account)
            on delete cascade,
    constraint fk_aARID
        foreign key (clientID) references client (ID)
            on update cascade on delete cascade
);

create index fk_aARcheck
    on accountAccessRecord (checkAccount);

create index fk_aARsavings
    on accountAccessRecord (savingsAccount);

create table clientContact
(
    clientID bigint(18)  not null
        primary key,
    name     varchar(10) not null,
    phone    bigint(11)  null,
    email    varchar(50) null,
    relation varchar(15) null comment '与客户关系',
    constraint fk_cC
        foreign key (clientID) references client (ID)
            on update cascade on delete cascade
);

create table client_branch_check_account
(
    clientID     bigint(18) not null,
    branchNum    int(10)    not null,
    checkAccount bigint(19) auto_increment,
    primary key (clientID, branchNum),
    constraint checkAccount_2
        unique (checkAccount),
    constraint fk_cbca
        foreign key (clientID) references client (ID)
            on update cascade,
    constraint fk_cbca2
        foreign key (branchNum) references branch (num)
            on delete cascade
);

create index checkAccount
    on client_branch_check_account (checkAccount);

create table client_branch_savings_account
(
    clientID       bigint(18) not null,
    branchNum      int(10)    not null,
    savingsAccount bigint(19) auto_increment,
    primary key (clientID, branchNum),
    constraint savingsAccount
        unique (savingsAccount),
    constraint fk_cbsa
        foreign key (clientID) references client (ID)
            on update cascade,
    constraint fk_cbsa2
        foreign key (branchNum) references branch (num)
            on update cascade
);

create index dd
    on client_branch_savings_account (branchNum);

create index ee
    on client_branch_savings_account (clientID);

create index qq
    on client_branch_savings_account (clientID);

create index tt
    on client_branch_savings_account (savingsAccount);

create index ww
    on client_branch_savings_account (savingsAccount);

create table loan_to_client
(
    loanNum  int(10)      not null,
    clientID bigint(18)   not null,
    date     date         null,
    amount   float(15, 0) null,
    constraint fk_loanClient
        foreign key (clientID) references client (ID)
            on update cascade,
    constraint loan_to_client_loan_loanNum_fk
        foreign key (loanNum) references loan (loanNum)
            on delete cascade
);

create index fk_loanNum
    on loan_to_client (loanNum);

create
    definer = leafz@`%` procedure cou(OUT aaa int)
BEGIN
    declare a int default 1;
    declare b int;
    set aaa = a;
END;

create
    definer = root@localhost procedure cxckmonth(IN ye int, IN mon int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;

    select sum(depositAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(depositDate) = ye
      and month(depositDate) = mon
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(depositAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(depositDate) = ye
      and month(depositDate) = mon
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(*)
    from (select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_savings_account
          where year(depositDate) = ye
            and month(depositDate) = mon
            and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
            and branchNum = Num
          union
          select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_check_account
          where year(depositDate) = ye
            and month(depositDate) = mon
            and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
            and branchNum = Num) as a
    into number;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    set money = money1 + money2;
    if number is null then
        set number = 0;
    end if;
    #Routine body goes here...
END;

create
    definer = root@localhost procedure cxckseason(IN ye int, IN se int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;

    select sum(depositAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(depositDate) = ye
      and QUARTER(depositDate) = se
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(depositAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(depositDate) = ye
      and QUARTER(depositDate) = se
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(*)
    from (select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_savings_account
          where year(depositDate) = ye
            and QUARTER(depositDate) = se
            and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
            and branchNum = Num
          union
          select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_check_account
          where year(depositDate) = ye
            and QUARTER(depositDate) = se
            and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
            and branchNum = Num) as a
    into number;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    set money = money1 + money2;
    if number is null then
        set number = 0;
    end if;
    #Routine body goes here...
END;

create
    definer = root@localhost procedure cxckyear(IN ye int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;

    select sum(depositAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(depositDate) = ye
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(depositAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(depositDate) = ye
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(*)
    from (select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_savings_account
          where year(depositDate) = ye
            and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
            and branchNum = Num
          union
          select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_check_account
          where year(depositDate) = ye
            and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
            and branchNum = Num) as a
    into number;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    if number is null then
        set number = 0;
    end if;

    set money = money1 + money2;
    #Routine body goes here...
END;

create
    definer = leafz@`%` procedure cxmonthNum(IN ye int, IN mon int, IN num int, OUT number int)
begin
    select count(*)
    from (
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(depositDate) = ye
               and month(depositDate) = mon
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(withdrawalDate) = ye
               and month(withdrawalDate) = mon
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(depositDate) = ye
               and month(depositDate) = mon
               and client_branch_check_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(withdrawalDate) = ye
               and month(withdrawalDate) = mon
               and client_branch_check_account.branchNum = num
         )
             as a
    into number;

end;

create
    definer = root@localhost procedure cxqkmonth(IN ye int, IN mon int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;

    select sum(withdrawalAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(withdrawalDate) = ye
      and month(withdrawalDate) = mon
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(withdrawalAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(withdrawalDate) = ye
      and month(withdrawalDate) = mon
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(*)
    from (select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_savings_account
          where year(withdrawalDate) = ye
            and month(withdrawalDate) = mon
            and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
            and branchNum = Num
          union
          select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_check_account
          where year(withdrawalDate) = ye
            and month(withdrawalDate) = mon
            and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
            and branchNum = Num) as a
    into number;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    set money = money1 + money2;
    #Routine body goes here...
END;

create
    definer = root@localhost procedure cxqkseason(IN ye int, IN se int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;
    declare number1 int default 0;
    declare number2 int default 0;
    select sum(withdrawalAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(withdrawalDate) = ye
      and quarter(withdrawalDate) = se
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(withdrawalAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(withdrawalDate) = ye
      and quarter(withdrawalDate) = se
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(DISTINCT accountAccessRecord.clientID)
    into number1
    from accountAccessRecord,
         client_branch_savings_account
    where year(withdrawalDate) = ye
      and quarter(withdrawalDate) = se
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select count(DISTINCT accountAccessRecord.clientID)
    into number2
    from accountAccessRecord,
         client_branch_check_account
    where year(withdrawalDate) = ye
      and quarter(withdrawalDate) = se
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    if number1 is null then
        set number1 = 0;
    end if;
    if number2 is null then
        set number2 = 0;
    end if;
    set number = number1 + number2;
    set money = money1 + money2;
    #Routine body goes here...
END;

create
    definer = root@localhost procedure cxqkyear(IN ye int, IN Num int, OUT money float, OUT number int)
BEGIN
    declare money1 float default 0;
    declare money2 float default 0;

    select sum(withdrawalAmount)
    into money1
    from accountAccessRecord,
         client_branch_savings_account
    where year(withdrawalDate) = ye
      and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
      and branchNum = Num;
    select sum(withdrawalAmount)
    into money2
    from accountAccessRecord,
         client_branch_check_account
    where year(withdrawalDate) = ye
      and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
      and branchNum = Num;

    select count(*)
    from (select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_savings_account
          where year(withdrawalDate) = ye
            and accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
            and branchNum = Num
          union
          select DISTINCT accountAccessRecord.clientID
          from accountAccessRecord,
               client_branch_check_account
          where year(withdrawalDate) = ye
            and accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
            and branchNum = Num) as a
    into number;
    if money1 is null then
        set money1 = 0;
    end if;
    if money2 is null then
        set money2 = 0;
    end if;
    set money = money1 + money2;
    #Routine body goes here...
END;

create
    definer = leafz@`%` procedure cxseasonNum(IN ye int, IN se int, IN num int, OUT number int)
begin
    select count(*)
    from (
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(depositDate) = ye
               and quarter(depositDate) = se
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(withdrawalDate) = ye
               and quarter(withdrawalDate) = se
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(depositDate) = ye
               and quarter(depositDate) = se
               and client_branch_check_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(withdrawalDate) = ye
               and quarter(withdrawalDate) = se
               and client_branch_check_account.branchNum = num
         )
             as a
    into number;

end;

create
    definer = leafz@`%` procedure cxyearNum(IN ye int, IN num int, OUT number int)
begin
    select count(*)
    from (
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(depositDate) = ye
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_savings_account
             where accountAccessRecord.savingsAccount = client_branch_savings_account.savingsAccount
               and year(withdrawalDate) = ye
               and client_branch_savings_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(depositDate) = ye
               and client_branch_check_account.branchNum = num
             union
             select distinct accountAccessRecord.clientID
             from accountAccessRecord,
                  client_branch_check_account
             where accountAccessRecord.checkAccount = client_branch_check_account.checkAccount
               and year(withdrawalDate) = ye
               and client_branch_check_account.branchNum = num
         )
             as a
    into number;

end;

create
    definer = root@localhost procedure dkmonth(IN ye int, IN mon int, IN branch varchar(15), OUT money float,
                                               OUT number int)
BEGIN
    select sum(loanAmount)
    into money
    from loan
    where year(createdDate) = ye
      and month(createdDate) = mon
      and loan.branchName = branch;
    select count(DISTINCT clientID)
    into number
    from loan_to_client,
         loan
    where year(date) = ye
      and month(date) = mon
      and loan.loanNum = loan_to_client.loanNum
      and loan.branchName = branch;
    if money is null then
        set money = 0;
    end if;
    if number is null then
        set number = 0;
    end if;
END;

create
    definer = root@localhost procedure dkseason(IN ye int, IN se int, IN branch varchar(15), OUT money float,
                                                OUT number int)
BEGIN
    select sum(loanAmount)
    into money
    from loan
    where year(createdDate) = ye
      and quarter(createdDate) = se
      and loan.branchName = branch;
    select count(DISTINCT clientID)
    into number
    from loan_to_client,
         loan
    where year(date) = ye
      and quarter(date) = se
      and loan.loanNum = loan_to_client.loanNum
      and loan.branchName = branch;
    if money is null then
        set money = 0;
    end if;
    if number is null then
        set number = 0;
    end if;
END;

create
    definer = root@localhost procedure dkstatus(IN dknum int(10))
BEGIN
    DECLARE dksum float;
    DECLARE dk float; -- dk表示贷款表里的贷款金额。1表示发放中，2表示发放完毕，3表示异常，默认是0，未发放。
    select SUM(amount)
    into dksum
    from loan_to_client a
    where a.loanNum = dknum;
    select loanAmount
    Into dk
    from loan b
    where b.loanNum = dknum;
    IF dksum < dk THEN
        UPDATE loan
        SET `status` = 1
        WHERE loan.loanNum = dknum;
    ELSEIF dksum = dk THEN
        UPDATE loan
        SET `status` = 2
        where loan.loanNum = dknum;
    ELSE
        UPDATE loan
        SET `status` = 3
        where loan.loanNum = dknum;
    END IF;#Routine body goes here...

END;

create
    definer = root@localhost procedure dkyear(IN ye int, IN branch varchar(15), OUT money float, OUT number int)
BEGIN
    select sum(loanAmount)
    into money
    from loan
    where year(createdDate) = ye
      and loan.branchName = branch;
    select count(DISTINCT clientID)
    into number
    from loan_to_client,
         loan
    where year(date) = ye
      and loan.loanNum = loan_to_client.loanNum
      and loan.branchName = branch;
    if money is null then
        set money = 0;
    end if;
    if number is null then
        set number = 0;
    end if;
END;


