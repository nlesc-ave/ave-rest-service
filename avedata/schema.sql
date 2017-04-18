drop table if exists metadata;
create table metadata (
    id integer primary key autoincrement,
    species text not null,
    genome text not null,
    datatype text not null,
    filename text not null
);
