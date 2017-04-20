drop table if exists metadata;
create table metadata (
    id integer primary key autoincrement,
    species text not null,
    genome text not null,
    datatype text not null,
    filename text not null
);

CREATE TABLE IF NOT EXISTS  features (
    meta_id integer not null,
    name text not null,
    chromosome text not null,
    start integer not null,
    end integer not null
);
CREATE INDEX IF NOT EXISTS features_name_i ON features (name);
