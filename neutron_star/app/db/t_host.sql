create table t_host(
    id serial primary key,
    uuid text not null ,
    ip text not null ,
    port int not null ,
    root_password text not null ,
    username text not null,
    nickname text not null
);
