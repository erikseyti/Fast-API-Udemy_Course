drop table if exists users;

create table users (
id SERIAL,
email varchar(200) default null,
username varchar(45) default null,
first_name varchar(45) default null,
last_name varchar(45) default null,
hashed_password varchar(200) default null,
is_active boolean default null,
primary key (id)
);

drop table if exists todos;

create table todos(
id SERIAL,
title varchar(200) default null,
description varchar(200) default null,
priority integer default null,
complete boolean default null,
owner_id integer default null,
primary key (id),
foreign key (owner_id) references users(id)
);