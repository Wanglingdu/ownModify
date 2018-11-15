drop database if exists deepbc;
create database if not exists deepbc;
use deepbc
-- create table users
-- (
-- 	id int not null auto_increment,
-- 	username varchar(20) not null, #设定默认值
-- 	password_hash varchar(128) not null,
-- 	primary key (id)
-- );
-- create index index_id on users(id);
create table bc_detect_info
(
	id int not null auto_increment,
	username varchar(32) not null DEFAULT 'milab',
	upload_path varchar(128) not null,
	upload_date DATETIME not null,
	model_result varchar(1024) not null,
	doctor_result varchar(1024) DEFAULT null,
  report_path varchar(128) not null,
	primary key (id)
);
