drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text unique not null,
    password blob not null,
    display text,
    permissions integer not null
);

drop table if exists boards;
create table boards (
    id integer primary key autoincrement,
    uid integer not null,
    create_time timestamp default current_timestamp,
    problem text not null,
    solution text not null,
    block_width integer not null,
    block_height integer not null
);

