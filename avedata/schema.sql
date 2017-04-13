drop table if exists metadata;
create table metadata (
    id integer primary key autoincrement,
    species text not null,
    genome text not null,
    type text not null,
    filename text not null
);
