create schema project4;
use project4;

create table users(
	id integer not null unique auto_increment,
    username varchar(255) not null unique,
    pass varchar(255) not null,
    userRole integer not null,
    primary key (id)
);

create table product(
	id integer not null unique auto_increment,
    prodName varchar(255) not null,
    price decimal(10,2) not null,
    primary key (id)
);

create table sale(
	saleID integer not null unique auto_increment,
    prodID integer not null,
    userID integer not null,
    qty integer not null,
    total decimal(10,2) not null,
    primary key (saleID),
    foreign key (prodID) references product(id),
    foreign key (userID) references users(id)
);

insert into users (username, pass, userRole) VALUES ("admin", "admin", 1);